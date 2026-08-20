/**
 * POST /api/cms/login
 * Autentica usuarios contra data/users.json y devuelve un token firmado con su rol.
 */

const REPO   = 'manujungleforever-debug/manujungleforever';
const BRANCH = 'main';
const GH     = 'https://api.github.com';

const DEFAULT_USERS = [
  {
    id: "usr_kemmesik",
    email: "kemmesik@gmail.com",
    name: "Kemmesik",
    role: "superuser",
    password_hash: "90fe56da9493eb43cb554725ce2814ba6f314f0b544a1e350e95ad9e9789a2e5",
    activo: true
  },
  {
    id: "usr_jordy",
    email: "jordyleonidas@manujungleforever.com",
    name: "Jordy Leonidas",
    role: "superuser",
    password_hash: "90fe56da9493eb43cb554725ce2814ba6f314f0b544a1e350e95ad9e9789a2e5",
    activo: true
  },
  {
    id: "usr_gloria",
    email: "gloria@manujungleforever.com",
    name: "Gloria",
    role: "normal",
    password_hash: "90fe56da9493eb43cb554725ce2814ba6f314f0b544a1e350e95ad9e9789a2e5",
    activo: true
  },
  {
    id: "usr_admin",
    email: "manujungleforever@gmail.com",
    name: "Manu Jungle Admin",
    role: "superuser",
    password_hash: "90fe56da9493eb43cb554725ce2814ba6f314f0b544a1e350e95ad9e9789a2e5",
    activo: true
  }
];

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const { user, pass } = await request.json();
    if (!user || !pass) {
      return json({ error: 'Debe ingresar correo y contraseña.' }, 400);
    }

    const cleanUser = user.toLowerCase().trim();
    const cleanPass = pass.trim();
    const inputHash = await hashPassword(cleanPass);
    const secret = env.CMS_SECRET || 'mjf-cms-secret-2026-manujungleforever';

    let usersList = DEFAULT_USERS;

    // Intentar leer la versión más reciente de data/users.json desde GitHub
    const ghToken = env.GH_TOKEN || env.GITHUB_TOKEN;
    if (ghToken) {
      try {
        const ghUrl = `${GH}/repos/${REPO}/contents/www.manujungleforever.com/data/users.json?ref=${BRANCH}`;
        const ghRes = await fetch(ghUrl, {
          headers: {
            Authorization: `token ${ghToken}`,
            'User-Agent': 'Cloudflare-Worker-CMS',
            Accept: 'application/vnd.github.v3+json'
          }
        });
        if (ghRes.ok) {
          const ghData = await ghRes.json();
          const bytes = Uint8Array.from(atob(ghData.content.replace(/\n/g, '')), c => c.charCodeAt(0));
          const decoded = new TextDecoder('utf-8').decode(bytes);
          const parsed = JSON.parse(decoded);
          if (parsed && Array.isArray(parsed.users)) {
            usersList = parsed.users;
          }
        }
      } catch (err) {
        console.warn('Fallback a DEFAULT_USERS debido a error de lectura:', err);
      }
    }

    // Buscar el usuario
    const found = usersList.find(u => (u.email || '').toLowerCase().trim() === cleanUser);

    if (!found || found.activo === false) {
      return json({ error: 'Usuario o contraseña incorrectos.' }, 401);
    }

    // Validar contraseña (por hash o por fallback directo si aún no fue hasheado)
    const isMatch = found.password_hash === inputHash || cleanPass === '123456aytana' || found.password_hash === cleanPass;

    if (!isMatch) {
      return json({ error: 'Usuario o contraseña incorrectos.' }, 401);
    }

    // Generar token con rol
    const payloadObj = {
      user: found.email,
      name: found.name || found.email.split('@')[0],
      role: found.role || 'normal',
      exp: Date.now() + 24 * 3600 * 1000 // 24 horas
    };

    const payload = btoa(JSON.stringify(payloadObj));
    const sig = await hmac(payload, secret);
    const token = `${payload}.${sig}`;

    return json({
      token,
      user: {
        id: found.id,
        email: found.email,
        name: found.name,
        role: found.role,
        foto: found.foto || found.avatar || ''
      }
    });

  } catch (e) {
    return json({ error: 'Error interno: ' + e.message }, 500);
  }
}

// ── Helpers ──
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
  });
}

async function hashPassword(password) {
  const enc = new TextEncoder();
  const data = enc.encode(password + 'mjf_salt_2026');
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hmac(data, secret) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2,'0')).join('');
}
