/**
 * GET  /api/cms/file?path=<repo-path>   → lee un archivo o directorio del repo
 * PUT  /api/cms/file                    → escribe un archivo en el repo
 *
 * Variables de entorno requeridas:
 *   GITHUB_TOKEN  — Personal Access Token con scope `repo`
 *   CMS_SECRET    — misma clave usada en login.js para verificar el token
 */

const REPO  = 'hiddenjunglecusco/hiddenjunglecusco';
const BRANCH = 'master';
const GH    = 'https://api.github.com';

// ── CORS preflight ────────────────────────────────────────────────────────────
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

  const ghUrl = `${GH}/repos/${REPO}/contents/${path}?ref=${BRANCH}`;
  const ghRes = await ghFetch(ghUrl, env.GITHUB_TOKEN);

  if (!ghRes.ok) {
    const err = await ghRes.json().catch(() => ({}));
    return json({ error: err.message || 'GitHub error' }, ghRes.status);
  }

  const data = await ghRes.json();

  // Si es un directorio, devuelve listado
  if (Array.isArray(data)) {
    return json({ files: data.map(f => ({ name: f.name, path: f.path, type: f.type, sha: f.sha })) });
  }

  // Si es un archivo, decodifica el contenido correctamente como UTF-8
  const bytes = Uint8Array.from(atob(data.content.replace(/\n/g, '')), c => c.charCodeAt(0));
  const content = new TextDecoder('utf-8').decode(bytes);
  return json({ content, sha: data.sha, path: data.path });
}

// ── PUT ───────────────────────────────────────────────────────────────────────
export async function onRequestPut(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  const { path, content, sha, message } = await request.json();
  if (!path || content === undefined) return json({ error: 'path y content requeridos' }, 400);

  // Codifica el contenido como UTF-8 → base64
  const bytes = new TextEncoder().encode(content);
  const encoded = btoa(String.fromCharCode(...bytes));

  const body = { message: message || `update: ${path}`, content: encoded, branch: BRANCH };
  if (sha) body.sha = sha;

  const ghUrl = `${GH}/repos/${REPO}/contents/${path}`;
  const ghRes = await ghFetch(ghUrl, env.GITHUB_TOKEN, 'PUT', body);

  if (!ghRes.ok) {
    const err = await ghRes.json().catch(() => ({}));
    return json({ error: err.message || 'Error escribiendo en GitHub' }, ghRes.status);
  }

  const result = await ghRes.json();
  return json({ sha: result.content?.sha, path });
}

// ── helpers ───────────────────────────────────────────────────────────────────
function ghFetch(url, token, method = 'GET', body = null) {
  const opts = {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'HJC-CMS/1.0',
      ...(body ? { 'Content-Type': 'application/json' } : {})
    },
    ...(body ? { body: JSON.stringify(body) } : {})
  };
  return fetch(url, opts);
}

async function verifyToken(request, env) {
  const auth = request.headers.get('Authorization') || '';
  const token = auth.replace('Bearer ', '').trim();

  if (!token) return json({ error: 'No autenticado' }, 401);

  try {
    const [payload, sig] = token.split('.');
    const expected = await hmac(payload, env.CMS_SECRET);
    if (sig !== expected) return json({ error: 'Token inválido' }, 401);

    const { exp } = JSON.parse(atob(payload));
    if (Date.now() > exp) return json({ error: 'Sesión expirada' }, 401);

    return null; // ok
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
    'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  };
}
