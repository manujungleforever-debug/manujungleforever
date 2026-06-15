export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}

// ── GET: Listar archivos en R2 ────────────────────────────────────────────────
export async function onRequestGet(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  if (!env.MEDIA_BUCKET) {
    return json({ error: 'R2 MEDIA_BUCKET no configurado' }, 500);
  }

  try {
    const list = await env.MEDIA_BUCKET.list({ limit: 1000 });
    const files = list.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded,
      url: `/media/${obj.key}`
    })).sort((a, b) => new Date(b.uploaded) - new Date(a.uploaded));

    return json({ files });
  } catch (e) {
    return json({ error: 'Error listando bucket: ' + e.message }, 500);
  }
}

// ── POST: Subir archivo a R2 ──────────────────────────────────────────────────
export async function onRequestPost(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  if (!env.MEDIA_BUCKET) return json({ error: 'R2 MEDIA_BUCKET no configurado' }, 500);

  try {
    const { name, base64, contentType } = await request.json();
    if (!name || !base64) return json({ error: 'name y base64 requeridos' }, 400);

    // Limpiar nombre de archivo (slugify simple manteniendo extensión)
    const ext = name.split('.').pop().toLowerCase();
    const slug = name.slice(0, -(ext.length + 1)).replace(/[^a-z0-9]/gi, '-').toLowerCase() + '.' + ext;
    const finalName = `${Date.now()}-${slug}`;

    const binary = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
    
    await env.MEDIA_BUCKET.put(finalName, binary, {
      httpMetadata: { contentType: contentType || getMimeType(ext) }
    });

    return json({ 
      ok: true, 
      file: { key: finalName, url: `/media/${finalName}` }
    });
  } catch (e) {
    return json({ error: 'Error subiendo archivo: ' + e.message }, 500);
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function getMimeType(ext) {
  const types = {
    jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', 
    gif: 'image/gif', webp: 'image/webp', svg: 'image/svg+xml',
    mp4: 'video/mp4', webm: 'video/webm'
  };
  return types[ext] || 'application/octet-stream';
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
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  };
}
