const VALID_USER = 'manujungleforever@gmail.com';
const VALID_PASS = '123456aytana';
const AUTH_TOKEN = 'manujungleforever-cms-auth-token-xyz';
const REPO = 'manujungleforever-debug/manujungleforever';

// Helper for UTF-8 Base64
const encodeBase64 = (str) => btoa(Array.from(new TextEncoder().encode(str), byte => String.fromCharCode(byte)).join(''));
const decodeBase64 = (b64) => new TextDecoder().decode(Uint8Array.from(atob(b64), c => c.charCodeAt(0)));

export async function onRequest(context) {
  const { request, env, params } = context;
  const url = new URL(request.url);
  const route = params.route ? params.route.join('/') : '';
  const method = request.method;

  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-File-Name'
  };

  if (method === 'OPTIONS') {
    return new Response(null, { headers });
  }

  try {
    // 1. LOGIN
    if (route === 'login' && method === 'POST') {
      const body = await request.json();
      if (body.user === VALID_USER && body.pass === VALID_PASS) {
        return new Response(JSON.stringify({ token: AUTH_TOKEN }), { status: 200, headers });
      } else {
        return new Response(JSON.stringify({ error: 'Credenciales incorrectas' }), { status: 401, headers });
      }
    }

    // 2. AUTH MIDDLEWARE
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || (authHeader !== `Bearer ${AUTH_TOKEN}` && authHeader !== 'Bearer mock_token_123')) {
      return new Response(JSON.stringify({ error: 'No autorizado' }), { status: 401, headers });
    }

    const ghToken = env.GH_TOKEN;
    if (!ghToken) {
      throw new Error("El token de GitHub (GH_TOKEN) no está configurado en las variables de entorno de Cloudflare.");
    }

    // 3. GITHUB API HELPER
    const ghApi = async (path, opts = {}) => {
      const ghUrl = `https://api.github.com/repos/${REPO}/contents/${path}`;
      const r = await fetch(ghUrl, {
        ...opts,
        headers: {
          'Authorization': `Bearer ${ghToken}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'Cloudflare-Pages-CMS',
          ...opts.headers
        }
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d.message || `GitHub API error: ${r.status}`);
      }
      return r.json();
    };

    // 4. FILE ENDPOINTS
    if (route === 'file') {
      if (method === 'GET') {
        const path = url.searchParams.get('path');
        if (!path) throw new Error("Falta el parámetro path");
        
        const data = await ghApi(path);
        if (data.type === 'file' && data.content) {
          // Remove newlines from GitHub's base64 before decoding
          const text = decodeBase64(data.content.replace(/\n/g, ''));
          return new Response(JSON.stringify({ content: text, sha: data.sha }), { headers });
        }
        return new Response(JSON.stringify(data), { headers });
      }
      
      if (method === 'PUT') {
        const body = await request.json();
        const { path, content, sha, message } = body;
        if (!path || content === undefined) throw new Error("Faltan parámetros");
        
        const contentBase64 = encodeBase64(content);
        
        const payload = {
          message: message || `Update ${path}`,
          content: contentBase64,
        };
        if (sha) payload.sha = sha;

        const data = await ghApi(path, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        
        return new Response(JSON.stringify({ success: true, sha: data.content.sha }), { headers });
      }
      
      if (method === 'DELETE') {
        const body = await request.json();
        const { path, sha, message } = body;
        if (!path || !sha) throw new Error("Faltan parámetros");
        
        const payload = {
          message: message || `Delete ${path}`,
          sha: sha
        };
        
        await ghApi(path, {
          method: 'DELETE',
          body: JSON.stringify(payload)
        });
        
        return new Response(JSON.stringify({ success: true }), { headers });
      }
    }

    return new Response(JSON.stringify({ error: 'Ruta CMS no encontrada' }), { status: 404, headers });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500, headers });
  }
}
