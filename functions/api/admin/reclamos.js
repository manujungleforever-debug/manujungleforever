const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json;charset=UTF-8',
};

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
const error = (msg, status = 400) => json({ ok: false, error: msg }, status);

async function verifyToken(request, env) {
  const auth = request.headers.get('Authorization') || '';
  const token = auth.replace('Bearer ', '').trim();
  if (!token) return { error: 'No autenticado', status: 401 };
  const secret = env.CMS_SECRET || 'mjf-cms-secret-2026-manujungleforever';
  try {
    const [payload, sig] = token.split('.');
    const expected = await hmac(payload, secret);
    if (sig !== expected) return { error: 'Token inválido', status: 401 };
    const { exp } = JSON.parse(atob(payload));
    if (Date.now() > exp) return { error: 'Sesión expirada', status: 401 };
    return null;
  } catch {
    return { error: 'Token inválido', status: 401 };
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

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  
  // Verify token
  const authErr = await verifyToken(request, env);
  if (authErr) {
    return error(authErr.error, authErr.status);
  }

  try {
    // Query D1 database
    const { results } = await env.DB.prepare(
      "SELECT * FROM reclamos ORDER BY id DESC"
    ).all();

    return json(results || []);
  } catch (err) {
    console.error('Error fetching reclamos from D1:', err);
    return error('Error al obtener los reclamos de la base de datos', 500);
  }
}
