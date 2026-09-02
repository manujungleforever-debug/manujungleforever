export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const authErr = await verifyToken(request, env);
  if (authErr) return authErr;

  if (!env.MEDIA_BUCKET) return json({ error: 'R2 MEDIA_BUCKET no configurado' }, 500);

  try {
    const { paths } = await request.json();
    if (!Array.isArray(paths) || paths.length === 0) {
      return json({ error: 'Array "paths" requerido' }, 400);
    }

    let keysToDelete = [];

    for (const p of paths) {
      keysToDelete.push(p); // Delete the item itself (if it's a file)
      
      // If it's a folder, list and collect all objects inside it
      let cursor = undefined;
      do {
        const listed = await env.MEDIA_BUCKET.list({ prefix: p + '/', cursor });
        if (listed && listed.objects) {
          keysToDelete.push(...listed.objects.map(o => o.key));
        }
        cursor = listed.truncated ? listed.cursor : undefined;
      } while (cursor);
    }

    // R2 allows deleting an array of keys in a single batch
    if (keysToDelete.length > 0) {
      // deduplicate keys just in case
      keysToDelete = [...new Set(keysToDelete)];
      await env.MEDIA_BUCKET.delete(keysToDelete);
    }
    return json({ ok: true, deleted: paths.length });
  } catch (e) {
    return json({ error: 'Error en bulk delete: ' + e.message }, 500);
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
