export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  if (!env.MEDIA_BUCKET) return json({ error: 'R2 MEDIA_BUCKET no configurado' }, 500);

  try {
    const { paths, destination } = await request.json();
    if (!Array.isArray(paths) || paths.length === 0 || typeof destination !== 'string') {
      return json({ error: 'Parámetros "paths" y "destination" requeridos' }, 400);
    }
    
    const dest = destination.replace(/^\/+|\/+$/g, ''); // strip leading/trailing slashes

    for (const oldKey of paths) {
      const fileName = oldKey.split('/').pop();
      const newKey = dest ? `${dest}/${fileName}` : fileName;
      
      if (oldKey === newKey) continue;

      const object = await env.MEDIA_BUCKET.get(oldKey);
      if (!object) continue; 
      
      await env.MEDIA_BUCKET.put(newKey, object.body, {
        httpMetadata: object.httpMetadata,
        customMetadata: object.customMetadata
      });
      
      await env.MEDIA_BUCKET.delete(oldKey);
    }
    
    return json({ ok: true, moved: paths.length });
  } catch (e) {
    return json({ error: 'Error en bulk move: ' + e.message }, 500);
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
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
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  };
}
