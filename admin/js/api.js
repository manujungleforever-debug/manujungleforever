/**
 * api.js — Admin CMS Layer
 * Single source of truth: Cloudflare D1 via Hono API routes.
 *
 * Endpoint map:
 *   site_content  → GET/PUT /api/content/:key   (home, about, contact, global)
 *   tours         → GET /api/tours   POST /api/tours   DELETE /api/tours/:id
 *   blog_posts    → GET /api/blog    POST /api/blog    DELETE /api/blog/:id
 *   testimonials  → GET /api/testimonios  POST /api/testimonios  PUT/DELETE /api/testimonios/:id
 *   departures    → GET /api/salidas  POST /api/salidas  PUT /api/salidas/:id  DELETE /api/salidas/:id
 *   passengers    → POST /api/salidas/:depId/passengers  PUT/DELETE /api/salidas/:depId/passengers/:paxId
 *   reclamos      → GET /api/reclamos  PUT /api/reclamos/:id/responder
 *   users         → GET /api/users  POST /api/users  PUT /api/users/:id  DELETE /api/users/:id
 *   media (R2)    → GET/POST/DELETE /api/media
 */

var API = window.API || '/api/cms';
var MEDIA_API = window.MEDIA_API || '/api/media';

// ── Auth ──────────────────────────────────────────────────────────────────────
function getAuthHeader() {
  const token = sessionStorage.getItem('cms_token');
  return { 'Authorization': 'Bearer ' + token };
}

function _checkAuth() {
  const token = sessionStorage.getItem('cms_token');
  if (!token) { window.location.href = '/admin/index.html'; throw new Error('No autenticado'); }
  return token;
}

function _redirect401() {
  sessionStorage.clear();
  window.location.href = '/admin/index.html';
}

// ── Path classifier ───────────────────────────────────────────────────────────
/**
 * Returns a dataset key based on the file path string.
 * This allows all panels (which still use path strings) to route to D1.
 */
function _classify(path) {
  const p = (path || '').toLowerCase();
  if (p.includes('/home.json')       || p.endsWith('home.json'))        return 'content:home';
  if (p.includes('/about.json')      || p.endsWith('about.json'))       return 'content:about';
  if (p.includes('/contact.json')    || p.endsWith('contact.json'))     return 'content:contact';
  if (p.includes('/global.json')     || p.endsWith('global.json'))      return 'content:global';
  if (p.includes('/tours.json')      || p.endsWith('tours.json'))       return 'tours';
  if (p.includes('posts-index.json') || p.endsWith('posts-index.json')) return 'blog:index';
  if (p.includes('/posts/')  && p.endsWith('.md'))                      return 'blog:post';
  if (p.includes('post-template.html'))                                 return 'file';
  if (p.includes('tour-template.html'))                                 return 'file';
  if (p.includes('testimonials.json')|| p.endsWith('testimonials.json'))return 'testimonials';
  if (p.includes('departures.json')  || p.endsWith('departures.json')) return 'departures';
  if (p.includes('reclamos.json'))                                      return 'reclamos';
  if (p.includes('/posts') && !p.includes('.'))                         return 'blog:list';
  if (p.includes('/users.json')      || p.endsWith('users.json'))       return 'users';
  return 'file';
}

// ── Generic D1 fetch helper ───────────────────────────────────────────────────
async function _d1(method, url, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  if (r.status === 401) { _redirect401(); return {}; }
  if (!r.ok) {
    const e = await r.json().catch(() => ({}));
    throw new Error(e.error || 'Error D1 ' + method + ' ' + url);
  }
  return r.json().catch(() => ({}));
}

// ── ghGet ─────────────────────────────────────────────────────────────────────
async function ghGet(path) {
  const ds = _classify(path);

  // ── site_content pages ──
  if (ds.startsWith('content:')) {
    const key = ds.split(':')[1];
    const d = await _d1('GET', '/api/content/' + key);
    // d = { key, data, ...spread, updatedAt }  — return data object directly
    const content = d.data || d;
    // strip meta fields injected by the API
    const { key: _k, updatedAt: _u, ...clean } = content;
    return {
      content: JSON.stringify(clean, null, 2),
      sha: 'd1:' + key   // used by panels to track version; irrelevant for D1 but kept for compat
    };
  }

  // ── tours ──
  if (ds === 'tours') {
    const d = await _d1('GET', '/api/tours');
    return { content: JSON.stringify({ tours: d.tours || [] }, null, 2), sha: 'd1:tours' };
  }

  // ── blog index / list ──
  if (ds === 'blog:index' || ds === 'blog:list') {
    const d = await _d1('GET', '/api/blog');
    const posts = (d.posts || []).map(p => ({
      slug:       p.slug,
      title:      p.titulo,
      titulo:     p.titulo,
      autor:      p.autor,
      date:       p.fecha,
      fecha:      p.fecha,
      category:   p.categoria,
      categoria:  p.categoria,
      excerpt:    p.extracto,
      extracto:   p.extracto,
      image:      p.imagen_hero,
      imagen_hero:p.imagen_hero,
      estado:     p.estado,
      id:         p.id
    }));
    return {
      content: JSON.stringify({ posts }, null, 2),
      sha: 'd1:blog',
      files: posts.map(p => ({
        name: p.slug + '.md',
        path: 'www.manujungleforever.com/posts/' + p.slug + '.md',
        sha:  'd1:' + p.id
      }))
    };
  }

  // ── single blog post (markdown path) ──
  if (ds === 'blog:post') {
    const slug = path.split('/').pop().replace('.md', '');
    const d = await _d1('GET', '/api/blog/' + encodeURIComponent(slug));
    const p = d.post || {};
    // Build a markdown-like content string the panel can parse
    const fm = [
      '---',
      'title: ' + (p.titulo || ''),
      'author: ' + (p.autor || 'Manu Jungle Forever'),
      'date: ' + (p.fecha || ''),
      'category: ' + (p.categoria || ''),
      'excerpt: ' + (p.extracto || ''),
      'image: ' + (p.imagen_hero || ''),
      'status: ' + (p.estado || 'publicado'),
      'id: ' + (p.id || ''),
      '---',
      p.contenido || ''
    ].join('\n');
    return { content: fm, sha: 'd1:' + (p.id || slug) };
  }

  // ── testimonials ──
  if (ds === 'testimonials') {
    const d = await _d1('GET', '/api/testimonios');
    const list = d.testimonios || d.testimonials || [];
    return { content: JSON.stringify({ testimonials: list }, null, 2), sha: 'd1:testimonials' };
  }

  // ── departures ──
  if (ds === 'departures') {
    const d = await _d1('GET', '/api/salidas');
    return { content: JSON.stringify({ salidas: d.salidas || [] }, null, 2), sha: 'd1:salidas' };
  }

  // ── reclamos ──
  if (ds === 'reclamos') {
    const d = await _d1('GET', '/api/reclamos');
    return { content: JSON.stringify({ reclamos: d.reclamos || [] }, null, 2), sha: 'd1:reclamos' };
  }

  // ── users ──
  if (ds === 'users') {
    const d = await _d1('GET', '/api/users');
    // Map D1 fields to panel-expected fields
    const users = (d.users || []).map(u => ({
      id:            u.id,
      email:         u.email,
      name:          u.name,
      role:          u.role === 'admin' ? 'superuser' : (u.role || 'normal'),
      foto:          u.foto || u.avatar || '',
      activo:        true,
      password_hash: '(stored in D1)',
      created_at:    u.createdAt || u.created_at || '',
      updated_at:    u.updatedAt || u.updated_at || ''
    }));
    return { content: JSON.stringify({ users }, null, 2), sha: 'd1:users' };
  }

  // ── Fallback: static files via GitHub proxy (HTML templates) ──
  _checkAuth();
  const token = sessionStorage.getItem('cms_token');
  const r = await fetch(API + '/file?path=' + encodeURIComponent(path), {
    headers: { Authorization: 'Bearer ' + token }
  });
  if (r.status === 401) { _redirect401(); return {}; }
  if (r.status === 404) return { content: '', sha: null, files: [] };
  if (!r.ok) { const e = await r.json().catch(() => ({})); throw new Error(e.error || 'Error al cargar'); }
  return r.json();
}

// ── ghPut ─────────────────────────────────────────────────────────────────────
async function ghPut(path, content, sha, msg) {
  const ds = _classify(path);

  // parse content
  let parsed;
  try { parsed = typeof content === 'string' ? JSON.parse(content) : content; }
  catch { parsed = { _raw: content }; }

  // ── site_content pages ──
  if (ds.startsWith('content:')) {
    const key = ds.split(':')[1];
    const d = await _d1('PUT', '/api/content/' + key, parsed);
    return { ok: true, sha: 'd1:' + key + ':' + Date.now() };
  }

  // ── tours ──
  if (ds === 'tours') {
    const d = await _d1('POST', '/api/tours', parsed);
    return { ok: true, sha: 'd1:tours:' + Date.now() };
  }

  // ── blog index (update = batch upsert) ──
  if (ds === 'blog:index') {
    const posts = parsed?.posts || [];
    for (const p of posts) {
      await _d1('POST', '/api/blog', {
        id:         p.id,
        slug:       p.slug,
        titulo:     p.title || p.titulo,
        autor:      p.autor || p.author || 'Manu Jungle Forever',
        fecha:      p.date || p.fecha,
        categoria:  p.category || p.categoria,
        extracto:   p.excerpt || p.extracto,
        contenido:  p.contenido || p.content || '',
        imagen_hero:p.image || p.imagen_hero,
        estado:     p.estado || 'publicado'
      });
    }
    return { ok: true, sha: 'd1:blog:' + Date.now() };
  }

  // ── single blog post (markdown) ──
  if (ds === 'blog:post') {
    // content is a markdown string with frontmatter
    const slug = path.split('/').pop().replace('.md', '');
    const raw = typeof content === 'string' ? content : JSON.stringify(content);
    // Parse frontmatter
    const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
    let post = { slug, contenido: raw };
    if (fmMatch) {
      const fmLines = fmMatch[1].split('\n');
      const fm = {};
      fmLines.forEach(l => {
        const idx = l.indexOf(':');
        if (idx > -1) fm[l.substring(0, idx).trim()] = l.substring(idx + 1).trim();
      });
      post = {
        id:         fm.id || sha?.replace('d1:', '') || undefined,
        slug,
        titulo:     fm.title || fm.titulo || slug,
        autor:      fm.author || fm.autor || 'Manu Jungle Forever',
        fecha:      fm.date || fm.fecha,
        categoria:  fm.category || fm.categoria,
        extracto:   fm.excerpt || fm.extracto,
        imagen_hero:fm.image || fm.imagen_hero,
        estado:     fm.status || fm.estado || 'publicado',
        contenido:  fmMatch[2] || ''
      };
    }
    const d = await _d1('POST', '/api/blog', post);
    return { ok: true, sha: 'd1:blog:' + (d.id || slug) };
  }

  // ── testimonials ──
  if (ds === 'testimonials') {
    const list = parsed?.testimonials || parsed?.testimonios || (Array.isArray(parsed) ? parsed : [parsed]);
    const d = await _d1('POST', '/api/testimonios', list);
    return { ok: true, sha: 'd1:testimonials:' + Date.now() };
  }

  // ── departures — full replace (save entire salidas array) ──
  if (ds === 'departures') {
    const list = parsed?.salidas || (Array.isArray(parsed) ? parsed : [parsed]);
    // Upsert each departure
    for (const dep of list) {
      if (!dep || !dep.id) continue;
      // Try PUT first, if 404/405 do POST
      try {
        const r = await fetch('/api/salidas/' + encodeURIComponent(dep.id), {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dep)
        });
        if (r.status === 404 || r.status === 405) {
          await _d1('POST', '/api/salidas', dep);
        }
      } catch {
        await _d1('POST', '/api/salidas', dep);
      }
    }
    return { ok: true, sha: 'd1:salidas:' + Date.now() };
  }

  // ── users — batch upsert from panel ──
  if (ds === 'users') {
    const list = parsed?.users || (Array.isArray(parsed) ? parsed : [parsed]);
    for (const u of list) {
      if (!u || !u.email) continue;
      const payload = {
        name:  u.name,
        email: u.email,
        role:  u.role === 'superuser' ? 'admin' : 'editor',
        foto:  u.foto || ''
      };
      // Only set password if it's a real hash (not the placeholder)
      if (u.password_hash && u.password_hash !== '(stored in D1)') {
        payload.password_hash = u.password_hash;
      }
      if (u.id && !u.id.startsWith('usr_new')) {
        // Try update first
        const r = await fetch('/api/users/' + encodeURIComponent(u.id), {
          method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        });
        if (r.status === 404) await _d1('POST', '/api/users', { ...payload, password: '123456aytana' });
      } else {
        await _d1('POST', '/api/users', { ...payload, password: u._new_password || '123456aytana' });
      }
    }
    return { ok: true, sha: 'd1:users:' + Date.now() };
  }

  // ── Fallback: GitHub proxy for HTML templates ──
  _checkAuth();
  const token = sessionStorage.getItem('cms_token');
  const body = { path, content: typeof content === 'string' ? content : JSON.stringify(content, null, 2), sha, message: msg || 'update: ' + path };
  const r = await fetch(API + '/file', {
    method: 'PUT',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (r.status === 401) { _redirect401(); return {}; }
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || 'Error al guardar');
  return d;
}

// ── ghDelete ──────────────────────────────────────────────────────────────────
async function ghDelete(path, sha, msg) {
  const ds = _classify(path);

  // ── blog post ──
  if (ds === 'blog:post') {
    const slug = path.split('/').pop().replace('.md', '');
    // Find post id from sha or slug
    const id = sha?.replace('d1:', '') || slug;
    await _d1('DELETE', '/api/blog/' + encodeURIComponent(id));
    return { ok: true };
  }

  // ── departure ──
  if (ds === 'departures') {
    // path is used as id in some contexts
    const id = path;
    await _d1('DELETE', '/api/salidas/' + encodeURIComponent(id));
    return { ok: true };
  }

  // ── testimonial ──
  if (ds === 'testimonials') {
    await _d1('DELETE', '/api/testimonios/' + encodeURIComponent(path));
    return { ok: true };
  }

  // ── tour ──
  if (ds === 'tours') {
    await _d1('DELETE', '/api/tours/' + encodeURIComponent(path));
    return { ok: true };
  }

  // ── user ──
  if (ds === 'users') {
    await _d1('DELETE', '/api/users/' + encodeURIComponent(path));
    return { ok: true };
  }

  // ── Fallback: GitHub proxy ──
  _checkAuth();
  const token = sessionStorage.getItem('cms_token');
  const r = await fetch(API + '/file', {
    method: 'DELETE',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, sha, message: msg || 'delete: ' + path })
  });
  if (r.status === 401) { _redirect401(); return {}; }
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || 'Error al eliminar');
  return d;
}

// ── Passenger helpers (used directly by gestionar-salidas.html) ───────────────
async function apiAddPassenger(departureId, paxData) {
  return _d1('POST', '/api/salidas/' + encodeURIComponent(departureId) + '/passengers', paxData);
}

async function apiUpdatePassenger(departureId, paxId, paxData) {
  return _d1('PUT', '/api/salidas/' + encodeURIComponent(departureId) + '/passengers/' + encodeURIComponent(paxId), paxData);
}

async function apiDeletePassenger(departureId, paxId) {
  return _d1('DELETE', '/api/salidas/' + encodeURIComponent(departureId) + '/passengers/' + encodeURIComponent(paxId));
}

// ── Reclamos helpers ──────────────────────────────────────────────────────────
async function apiGetReclamos() {
  return _d1('GET', '/api/reclamos');
}

async function apiResponderReclamo(id, detalle) {
  return _d1('PUT', '/api/reclamos/' + encodeURIComponent(id) + '/responder', { detalle_respuesta: detalle });
}

// ── Users helpers ─────────────────────────────────────────────────────────────
async function apiGetUsers() {
  return _d1('GET', '/api/users');
}

async function apiCreateUser(data) {
  return _d1('POST', '/api/users', data);
}

async function apiUpdateUser(id, data) {
  return _d1('PUT', '/api/users/' + encodeURIComponent(id), data);
}

async function apiDeleteUser(id) {
  return _d1('DELETE', '/api/users/' + encodeURIComponent(id));
}
