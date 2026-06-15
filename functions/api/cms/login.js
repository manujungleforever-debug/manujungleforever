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

    if (!env.CMS_USER || !env.CMS_PASSWORD || !env.CMS_SECRET) {
      return json({ error: 'Panel no configurado. Contacta al administrador.' }, 500);
    }

    if (user !== env.CMS_USER || pass !== env.CMS_PASSWORD) {
      return json({ error: 'Usuario o contraseña incorrectos.' }, 401);
    }

    // Token simple: base64(payload).signature
    const payload = btoa(JSON.stringify({ user, exp: Date.now() + 8 * 3600 * 1000 }));
    const sig = await hmac(payload, env.CMS_SECRET);
    const token = `${payload}.${sig}`;

    return json({ token });

  } catch (e) {
    return json({ error: 'Error interno.' }, 500);
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
