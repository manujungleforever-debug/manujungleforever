/**
 * Cloudflare Pages Function: /api/auth
 * Inicia el flujo OAuth con GitHub para Decap CMS.
 *
 * Variables de entorno requeridas (en Cloudflare Pages → Settings → Env Variables):
 *   GITHUB_CLIENT_ID     — Client ID de tu GitHub OAuth App
 *   GITHUB_CLIENT_SECRET — Client Secret de tu GitHub OAuth App
 *
 * La GitHub OAuth App debe tener como Authorization callback URL:
 *   https://hiddenjunglecusco-2jc.pages.dev/api/auth/callback
 *
 * NOTA: Al pasar al dominio definitivo, cambiar también en config.yml:
 *   base_url: https://www.hiddenjunglecusco.com
 *   Y actualizar el callback URL en la GitHub OAuth App.
 */
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Generar un state aleatorio para proteger contra CSRF
  const state = crypto.randomUUID();

  // Construir la URL de autorización de GitHub
  const githubAuthUrl = new URL('https://github.com/login/oauth/authorize');
  githubAuthUrl.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  githubAuthUrl.searchParams.set('scope', 'repo,user');
  githubAuthUrl.searchParams.set('state', state);
  githubAuthUrl.searchParams.set(
    'redirect_uri',
    `${url.origin}/api/auth/callback`
  );

  // Redirigir al usuario a GitHub para autorización
  return Response.redirect(githubAuthUrl.toString(), 302);
}
