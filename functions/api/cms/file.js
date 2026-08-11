/**
 * GET  /api/cms/file?path=<repo-path>   → lee un archivo o directorio del repo
 * PUT  /api/cms/file                    → escribe un archivo (texto o binario) en el repo
 *
 * Para binarios (imágenes), enviar { path, base64, sha?, message }
 * Para texto, enviar { path, content, sha?, message }
 *
 * Variables de entorno:
 *   GITHUB_TOKEN  — Personal Access Token con scope `repo`
 *   CMS_SECRET    — clave para verificar tokens de sesión
 */

const REPO   = 'manujungleforever-debug/manujungleforever';
const BRANCH = 'main';
const GH     = 'https://api.github.com';
const IMAGE_EXTS = ['jpg','jpeg','png','gif','webp','svg','ico','avif'];

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}

// ── GET ───────────────────────────────────────────────────────────────────────
export async function onRequestGet(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  const url  = new URL(request.url);
  const path = url.searchParams.get('path');
  if (!path) return json({ error: 'path requerido' }, 400);

  const token = env.GH_TOKEN || env.GITHUB_TOKEN;
  const ghUrl = `${GH}/repos/${REPO}/contents/${encodeURIComponent(path).replace(/%2F/g,'/')}?ref=${BRANCH}`;
  const ghRes = await ghFetch(ghUrl, token);

  if (!ghRes.ok) {
    const err = await ghRes.json().catch(() => ({}));
    return json({ error: err.message || 'GitHub error' }, ghRes.status === 401 ? 502 : ghRes.status);
  }

  const data = await ghRes.json();

  // Directorio → listado
  if (Array.isArray(data)) {
    return json({ files: data.map(f => ({ name: f.name, path: f.path, type: f.type, sha: f.sha })) });
  }

  // Imagen → devuelve base64 tal cual (para preview)
  const ext = path.split('.').pop().toLowerCase();
  if (IMAGE_EXTS.includes(ext)) {
    return json({ base64: data.content.replace(/\n/g,''), sha: data.sha, path: data.path, isImage: true });
  }

  // Texto → decodifica correctamente como UTF-8
  const bytes = Uint8Array.from(atob(data.content.replace(/\n/g, '')), c => c.charCodeAt(0));
  const content = new TextDecoder('utf-8').decode(bytes);
  return json({ content, sha: data.sha, path: data.path });
}

// ── PUT ───────────────────────────────────────────────────────────────────────
export async function onRequestPut(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  const body = await request.json();
  const { path, sha, message } = body;
  if (!path) return json({ error: 'path requerido' }, 400);

  let encoded;

  if (body.base64 !== undefined) {
    // Archivo binario: ya viene en base64 del navegador
    encoded = body.base64;
  } else if (body.content !== undefined) {
    // Texto: codificar UTF-8 → base64
    const bytes = new TextEncoder().encode(body.content);
    // Manejo de buffers grandes con reduce
    const CHUNK = 8192;
    let binary = '';
    for (let i = 0; i < bytes.length; i += CHUNK) {
      binary += String.fromCharCode(...bytes.subarray(i, i + CHUNK));
    }
    encoded = btoa(binary);
  } else {
    return json({ error: 'content o base64 requerido' }, 400);
  }

  const ghBody = { message: message || `update: ${path}`, content: encoded, branch: BRANCH };
  if (sha) ghBody.sha = sha;

  const token = env.GH_TOKEN || env.GITHUB_TOKEN;
  const ghUrl = `${GH}/repos/${REPO}/contents/${encodeURIComponent(path).replace(/%2F/g,'/')}`;
  const ghRes = await ghFetch(ghUrl, token, 'PUT', ghBody);

  if (!ghRes.ok) {
    const err = await ghRes.json().catch(() => ({}));
    return json({ error: err.message || 'Error escribiendo en GitHub' }, ghRes.status === 401 ? 502 : ghRes.status);
  }

  const result = await ghRes.json();
  return json({ sha: result.content?.sha, path });
}

// ── DELETE ────────────────────────────────────────────────────────────────────
export async function onRequestDelete(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  const { path, sha, message } = await request.json();
  if (!path || !sha) return json({ error: 'path y sha requeridos' }, 400);

  const ghBody = { message: message || `delete: ${path}`, sha, branch: BRANCH };
  const token = env.GH_TOKEN || env.GITHUB_TOKEN;
  const ghUrl = `${GH}/repos/${REPO}/contents/${encodeURIComponent(path).replace(/%2F/g,'/')}`;
  const ghRes = await ghFetch(ghUrl, token, 'DELETE', ghBody);

  if (!ghRes.ok) {
    const err = await ghRes.json().catch(() => ({}));
    return json({ error: err.message || 'Error eliminando archivo' }, ghRes.status === 401 ? 502 : ghRes.status);
  }

  return json({ ok: true });
}

// ── helpers ───────────────────────────────────────────────────────────────────
function ghFetch(url, token, method = 'GET', body = null) {
  return fetch(url, {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'HJC-CMS/1.0',
      ...(body ? { 'Content-Type': 'application/json' } : {})
    },
    ...(body ? { body: JSON.stringify(body) } : {})
  });
}

async function verifyToken(request, env) {
  const auth = request.headers.get('Authorization') || '';
  const token = auth.replace('Bearer ', '').trim();
  if (!token) return json({ error: 'No autenticado' }, 401);
  const secret = env.CMS_SECRET || 'mjf-cms-secret-2026-manujungleforever';
  try {
    const [payload, sig] = token.split('.');
    const expected = await hmac(payload, secret);
    if (sig !== expected) return json({ error: 'Token inválido' }, 401);
    const { exp } = JSON.parse(atob(payload));
    if (Date.now() > exp) return json({ error: 'Sesión expirada' }, 401);
    return null;
  } catch {
    return json({ error: 'Token inválido' }, 401);
  }
}

async function hmac(data, secret) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2,'0')).join('');
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status, headers: { 'Content-Type': 'application/json', ...cors() }
  });
}

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  };
}
