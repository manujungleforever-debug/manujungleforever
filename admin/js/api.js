/**
 * api.js — Admin CMS Client
 * 
 * Single source of truth: D1 database via Hono API.
 * 
 * - Content (home, about, contact, global) → /api/content/:key  (GET/PUT)
 * - Tours    → /api/tours                  (GET/POST)
 * - Blog     → /api/blog                   (GET/POST/DELETE)
 * - Testimonials → /api/testimonios        (GET/POST)
 * - Departures   → /api/salidas            (GET/POST/PUT/DELETE)
 * - Reclamos     → /api/reclamos           (GET)
 * - Files (HTML templates) → /api/cms/file (GET/PUT/DELETE via GitHub proxy)
 */

var API      = window.API      || '/api/cms';
var MEDIA_API = window.MEDIA_API || '/api/media';

function getAuthHeader() {
  const token = sessionStorage.getItem('cms_token');
  return { 'Authorization': 'Bearer ' + token };
}

// ── Identify what kind of path this is ───────────────────────────────────────
function identifyDataset(path) {
  const p = (path || '').toLowerCase();
  if (p.includes('/home.json'))    return 'content:home';
  if (p.includes('/about.json'))   return 'content:about';
  if (p.includes('/contact.json')) return 'content:contact';
  if (p.includes('/global.json'))  return 'content:global';
  if (p.includes('/tours.json') || p.includes('tours.json')) return 'tours';
  if (p.includes('posts-index.json') || p.includes('/posts/') || p.endsWith('.md')) return 'blog';
  if (p.includes('testimonials.json')) return 'testimonials';
  if (p.includes('departures.json'))   return 'departures';
  if (p.includes('reclamos.json'))     return 'reclamos';
  return 'file';
}

// ── ghGet: Read data ──────────────────────────────────────────────────────────
async function ghGet(path) {
  const dataset = identifyDataset(path);

  // Content pages: read from D1
  if (dataset.startsWith('content:')) {
    const key = dataset.split(':')[1];
    const r = await fetch('/api/content/' + key);
    if (!r.ok) throw new Error('Error al cargar contenido de ' + key);
    const d = await r.json();
    // API returns { key, data, ...spreadData, updatedAt }
    const content = d.data || d;
    return { content: JSON.stringify(content, null, 2), sha: 'd1:' + key };
  }

  if (dataset === 'tours') {
    const r = await fetch('/api/tours');
    if (!r.ok) throw new Error('Error al cargar tours');
    const d = await r.json();
    return { content: JSON.stringify({ tours: d.tours || [] }, null, 2), sha: 'd1:tours' };
  }

  if (dataset === 'blog') {
    const r = await fetch('/api/blog');
    if (!r.ok) throw new Error('Error al cargar blog');
    const d = await r.json();
    return {
      content: JSON.stringify({ posts: d.posts || [] }, null, 2),
      sha: 'd1:blog',
      files: (d.posts || []).map(p => ({
        name: p.slug + '.md',
        path: 'www.manujungleforever.com/posts/' + p.slug + '.md',
        sha: 'd1:' + p.slug
      }))
    };
  }

  if (dataset === 'testimonials') {
    const r = await fetch('/api/testimonios');
    if (!r.ok) throw new Error('Error al cargar testimonios');
    const d = await r.json();
    return { content: JSON.stringify({ testimonials: d.testimonials || d.testimonios || [] }, null, 2), sha: 'd1:testimonials' };
  }

  if (dataset === 'departures') {
    const r = await fetch('/api/salidas');
    if (!r.ok) throw new Error('Error al cargar salidas');
    const d = await r.json();
    return { content: JSON.stringify({ salidas: d.salidas || [] }, null, 2), sha: 'd1:salidas' };
  }

  if (dataset === 'reclamos') {
    const r = await fetch('/api/reclamos');
    if (!r.ok) throw new Error('Error al cargar reclamos');
    const d = await r.json();
    return { content: JSON.stringify({ reclamos: d.reclamos || [] }, null, 2), sha: 'd1:reclamos' };
  }

  // Fallback: GitHub file proxy (HTML templates, etc.)
  const token = sessionStorage.getItem('cms_token');
  const r = await fetch(API + '/file?path=' + encodeURIComponent(path), {
    headers: { Authorization: 'Bearer ' + token }
  });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; return; }
  if (r.status === 404) return { files: [] };
  if (!r.ok) { const e = await r.json().catch(() => ({})); throw new Error(e.error || 'Error al cargar'); }
  return r.json();
}

// ── ghPut: Write data ─────────────────────────────────────────────────────────
async function ghPut(path, content, sha, msg) {
  const dataset = identifyDataset(path);
  let parsed;
  try { parsed = typeof content === 'string' ? JSON.parse(content) : content; }
  catch { parsed = content; }

  // Content pages: write to D1
  if (dataset.startsWith('content:')) {
    const key = dataset.split(':')[1];
    const r = await fetch('/api/content/' + key, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsed)
    });
    if (!r.ok) { const e = await r.json().catch(() => ({})); throw new Error(e.error || 'Error al guardar contenido en D1'); }
    return { ok: true, sha: 'd1:' + key + ':' + Date.now() };
  }

  if (dataset === 'tours') {
    const r = await fetch('/api/tours', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsed)
    });
    if (!r.ok) { const e = await r.json().catch(() => ({})); throw new Error(e.error || 'Error al guardar tours'); }
    return { ok: true, sha: 'd1:tours:' + Date.now() };
  }

  if (dataset === 'blog') {
    const postList = parsed?.posts || (Array.isArray(parsed) ? parsed : [parsed]);
    for (const post of postList) {
      await fetch('/api/blog', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(post)
      });
    }
    return { ok: true, sha: 'd1:blog:' + Date.now() };
  }

  if (dataset === 'testimonials') {
    const testList = parsed?.testimonials || parsed?.testimonios || (Array.isArray(parsed) ? parsed : [parsed]);
    const r = await fetch('/api/testimonios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(testList)
    });
    if (!r.ok) { const e = await r.json().catch(() => ({})); throw new Error(e.error || 'Error al guardar testimonios'); }
    return { ok: true, sha: 'd1:testimonials:' + Date.now() };
  }

  if (dataset === 'departures') {
    // For departures, path contains one departure at a time from editDep
    const dep = parsed?.salidas ? parsed.salidas[0] : parsed;
    if (dep && dep.id) {
      const r = await fetch('/api/salidas/' + encodeURIComponent(dep.id), {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dep)
      });
      // If 404 (new), try POST
      if (r.status === 404 || r.status === 405) {
        await fetch('/api/salidas', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dep)
        });
      }
    }
    return { ok: true, sha: 'd1:salidas:' + Date.now() };
  }

  // Fallback: GitHub file proxy
  const token = sessionStorage.getItem('cms_token');
  if (!token) throw new Error('No autorizado');
  const r = await fetch(API + '/file', {
    method: 'PUT',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, content: typeof content === 'string' ? content : JSON.stringify(content, null, 2), sha, message: msg || 'update: ' + path })
  });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; return; }
  const d = await r.json();
  if (!r.ok) throw new Error(d.error || 'Error al guardar');
  return d;
}

// ── ghDelete: Delete data ─────────────────────────────────────────────────────
async function ghDelete(path, sha, msg) {
  const dataset = identifyDataset(path);

  if (dataset === 'blog' && path.includes('.md')) {
    const slug = path.split('/').pop().replace('.md', '');
    const r = await fetch('/api/blog/' + encodeURIComponent(slug), { method: 'DELETE' });
    if (r.ok) return { ok: true };
  }

  if (dataset === 'departures') {
    const id = path; // In salidas, path is used as the id sometimes
    const r = await fetch('/api/salidas/' + encodeURIComponent(id), { method: 'DELETE' });
    if (r.ok) return { ok: true };
  }

  // Fallback: GitHub file proxy
  const token = sessionStorage.getItem('cms_token');
  if (!token) throw new Error('No autorizado');
  const r = await fetch(API + '/file', {
    method: 'DELETE',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, sha, message: msg || 'delete: ' + path })
  });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; return; }
  const d = await r.json();
  if (!r.ok) throw new Error(d.error || 'Error al eliminar');
  return d;
}
