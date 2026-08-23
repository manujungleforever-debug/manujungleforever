// ── Universal D1/Hono API Client for Manu Jungle Forever Admin ──
window.API = window.API || '/api/cms';
window.MEDIA_API = window.MEDIA_API || '/api/media';
var API = window.API;
var MEDIA_API = window.MEDIA_API;

function getAuthHeader() {
  const token = sessionStorage.getItem('cms_token');
  return { 'Authorization': `Bearer ${token}` };
}

// Helper: Normalize path to identify dataset
function identifyDataset(path) {
  const p = (path || '').toLowerCase();
  if (p.includes('tours.json')) return 'tours';
  if (p.includes('posts-index.json') || p.includes('/posts/') || p.endsWith('.md')) return 'blog';
  if (p.includes('testimonials.json')) return 'testimonials';
  if (p.includes('departures.json')) return 'departures';
  if (p.includes('about.json')) return 'content_about';
  if (p.includes('home.json')) return 'content_home';
  if (p.includes('contact.json')) return 'content_contact';
  if (p.includes('global.json')) return 'content_global';
  if (p.includes('reclamos.json')) return 'reclamos';
  return 'file';
}

async function ghGet(path) {
  const dataset = identifyDataset(path);

  try {
    if (dataset === 'tours') {
      const r = await fetch('/api/tours');
      if (!r.ok) throw new Error('Error al cargar tours de base de datos');
      const d = await r.json();
      return { content: JSON.stringify({ tours: d.tours || [] }, null, 2), sha: 'd1_tours' };
    }

    if (dataset === 'blog') {
      const r = await fetch('/api/blog');
      if (!r.ok) throw new Error('Error al cargar artículos del blog');
      const d = await r.json();
      return { content: JSON.stringify({ posts: d.posts || [] }, null, 2), sha: 'd1_blog', files: (d.posts || []).map(p => ({ name: `${p.slug}.md`, path: `www.manujungleforever.com/posts/${p.slug}.md`, sha: 'd1_' + p.slug })) };
    }

    if (dataset === 'testimonials') {
      const r = await fetch('/api/testimonios');
      if (!r.ok) throw new Error('Error al cargar testimonios');
      const d = await r.json();
      return { content: JSON.stringify({ testimonials: d.testimonials || d.testimonios || [] }, null, 2), sha: 'd1_testimonials' };
    }

    if (dataset === 'departures') {
      const r = await fetch('/api/salidas');
      if (!r.ok) throw new Error('Error al cargar salidas');
      const d = await r.json();
      return { content: JSON.stringify({ salidas: d.salidas || [] }, null, 2), sha: 'd1_salidas' };
    }

    if (dataset.startsWith('content_')) {
      const key = dataset.replace('content_', '');
      const r = await fetch(`/api/content/${key}`);
      if (!r.ok) throw new Error(`Error al cargar contenido de ${key}`);
      const d = await r.json();
      return { content: JSON.stringify(d.data || {}, null, 2), sha: 'd1_' + key };
    }

    if (dataset === 'reclamos') {
      const r = await fetch('/api/reclamos');
      if (!r.ok) throw new Error('Error al cargar reclamos');
      const d = await r.json();
      return { content: JSON.stringify({ reclamos: d.reclamos || [] }, null, 2), sha: 'd1_reclamos' };
    }
  } catch (err) {
    console.warn(`Fallback to GitHub for ${path} due to:`, err.message);
  }

  // Fallback to GitHub file proxy
  const token = sessionStorage.getItem('cms_token');
  const r = await fetch(`${API}/file?path=${encodeURIComponent(path)}`, { headers: { Authorization: `Bearer ${token}` } });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; }
  if (r.status === 404) { return { files: [] }; }
  if (!r.ok) { const e = await r.json().catch(()=>({})); throw new Error(e.error || 'Error al cargar'); }
  return r.json();
}

async function ghPut(path, content, sha, msg) {
  const dataset = identifyDataset(path);
  let parsedContent;
  try { parsedContent = typeof content === 'string' ? JSON.parse(content) : content; } catch { parsedContent = content; }

  if (dataset === 'tours') {
    const r = await fetch('/api/tours', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsedContent)
    });
    if (!r.ok) { const e = await r.json().catch(()=>({})); throw new Error(e.error || 'Error al guardar tours en base de datos'); }
    return { ok: true, sha: 'd1_tours_' + Date.now() };
  }

  if (dataset === 'blog') {
    const postList = parsedContent?.posts || (Array.isArray(parsedContent) ? parsedContent : [parsedContent]);
    for (const post of postList) {
      await fetch('/api/blog', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(post)
      });
    }
    return { ok: true, sha: 'd1_blog_' + Date.now() };
  }

  if (dataset === 'testimonials') {
    const testList = parsedContent?.testimonials || parsedContent?.testimonios || (Array.isArray(parsedContent) ? parsedContent : [parsedContent]);
    for (const t of testList) {
      await fetch('/api/testimonios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(t)
      });
    }
    return { ok: true, sha: 'd1_testimonials_' + Date.now() };
  }

  if (dataset.startsWith('content_')) {
    const key = dataset.replace('content_', '');
    const r = await fetch(`/api/content/${key}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsedContent)
    });
    if (!r.ok) { const e = await r.json().catch(()=>({})); throw new Error(e.error || `Error al guardar ${key}`); }
    return { ok: true, sha: 'd1_' + key + '_' + Date.now() };
  }

  // Fallback to GitHub file proxy for HTML templates or unknown files
  const token = sessionStorage.getItem('cms_token');
  if (!token) throw new Error('No autorizado');
  const r = await fetch(`${API}/file`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, content, sha, message: msg || `update: ${path}` })
  });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; }
  const d = await r.json();
  if (!r.ok) throw new Error(d.error || 'Error al guardar');
  return d;
}

async function ghDelete(path, sha, msg) {
  const dataset = identifyDataset(path);

  if (dataset === 'blog' && path.includes('.md')) {
    const slug = path.split('/').pop().replace('.md', '');
    const r = await fetch(`/api/blog/${encodeURIComponent(slug)}`, { method: 'DELETE' });
    if (r.ok) return { ok: true };
  }

  // Fallback to GitHub file proxy
  const token = sessionStorage.getItem('cms_token');
  if (!token) throw new Error('No autorizado');
  const r = await fetch(`${API}/file`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, sha, message: msg || `delete: ${path}` })
  });
  if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; }
  const d = await r.json();
  if (!r.ok) throw new Error(d.error || 'Error al eliminar');
  return d;
}
