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

  // ── site_content pages, tours, blog are now purely static JSON (fallback used) ──

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

  // ── users is now purely static JSON ──

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

  // ── site_content, tours, blog are now purely static JSON (fallback used) ──

  // ── testimonials ──
  if (ds === 'testimonials') {
    const list = parsed?.testimonials || parsed?.testimonios || (Array.isArray(parsed) ? parsed : [parsed]);
    const d = await _d1('POST', '/api/testimonios', list);
    return { ok: true, sha: 'd1:testimonials:' + Date.now() };
  }

  // ── departures — batch upsert ──
  if (ds === 'departures') {
    const list = parsed?.salidas || (Array.isArray(parsed) ? parsed : [parsed]);
    await _d1('PUT', '/api/salidas', list);
    return { ok: true, sha: 'd1:salidas:' + Date.now() };
  }

  // ── users is now purely static JSON ──

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

  // ── blog post (static fallback) ──

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

  // ── tour (static fallback) ──

  // ── user (static fallback) ──

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
