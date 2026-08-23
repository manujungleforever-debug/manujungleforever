var API = window.API || '/api/cms';
var MEDIA_API = window.MEDIA_API || '/api/media';

function getAuthHeader() {
    const token = sessionStorage.getItem('cms_token');
    return { 'Authorization': `Bearer ${token}` };
}

async function ghGet(path) {
    const token = sessionStorage.getItem('cms_token');
    if (!token) throw new Error('No autorizado');
    const r = await fetch(`${API}/file?path=${encodeURIComponent(path)}`, { headers: { Authorization: `Bearer ${token}` } });
    if (r.status === 401) { sessionStorage.clear(); window.location.href = 'index.html'; }
    if (r.status === 404) { return { files: [] }; }
    if (!r.ok) { const e = await r.json().catch(()=>({})); throw new Error(e.error || 'Error al cargar'); }
    return r.json();
}

async function ghPut(path, content, sha, msg) {
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
