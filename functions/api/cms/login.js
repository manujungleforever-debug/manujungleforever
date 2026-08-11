/**
 * POST /api/cms/login
 * Verifica usuario/contraseña contra variables de entorno y devuelve un token simple.
 *
 * Variables de entorno requeridas en Cloudflare Pages:
 *   CMS_USER     — nombre de usuario (ej: admin)
 *   CMS_PASSWORD — contraseña del panel
 *   CMS_SECRET   — clave aleatoria para firmar el token (cualquier string largo)
 */
export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const { user, pass } = await request.json();

    const validUser = 'manujungleforever@gmail.com';
    const validPass = '123456aytana';
    // CMS_SECRET desde env o fallback local
    const secret = env.CMS_SECRET || 'mjf-cms-secret-2026-manujungleforever';

    if (user !== validUser || pass !== validPass) {
      return json({ error: 'Usuario o contraseña incorrectos.' }, 401);
    }

    // Token simple: base64(payload).signature
    const payload = btoa(JSON.stringify({ user, exp: Date.now() + 8 * 3600 * 1000 }));
    const sig = await hmac(payload, secret);
    const token = `${payload}.${sig}`;

    return json({ token });

  } catch (e) {
    return json({ error: 'Error interno: ' + e.message }, 500);
  }
}

// ── helpers ──────────────────────────────────────────────────────────────────
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    }
  });
}

async function hmac(data, secret) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2,'0')).join('');
}
