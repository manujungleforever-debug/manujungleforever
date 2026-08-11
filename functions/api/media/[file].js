export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}

// ── DELETE: Eliminar archivo en R2 ────────────────────────────────────────────
export async function onRequestDelete(context) {
  const { request, env, params } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  if (!env.MEDIA_BUCKET) return json({ error: 'R2 MEDIA_BUCKET no configurado' }, 500);

  const fileKey = params.file;
  if (!fileKey) return json({ error: 'Nombre de archivo requerido' }, 400);

  try {
    await env.MEDIA_BUCKET.delete(fileKey);
    return json({ ok: true });
  } catch (e) {
    return json({ error: 'Error eliminando archivo: ' + e.message }, 500);
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
    'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
  };
}
