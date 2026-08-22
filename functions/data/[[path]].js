const REPO   = 'manujungleforever-debug/manujungleforever';
const BRANCH = 'main';

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const filePath = params.path ? params.path.join('/') : '';
  if (!filePath) {
    return new Response('File not found', { status: 404 });
  }

  // 1. Try raw.githubusercontent.com (fast, no rate-limits)
  const rawUrl = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/www.manujungleforever.com/data/${filePath}?v=${Date.now()}`;
  try {
    const rawRes = await fetch(rawUrl, {
      headers: {
        'User-Agent': 'MJF-CMS/1.0',
        'Cache-Control': 'no-cache'
      }
    });

    if (rawRes.ok) {
      const content = await rawRes.text();
      return new Response(content, {
        status: 200,
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  } catch (e) {
    // continue to fallback
  }

  // 2. Fallback to static asset if raw request fails
  if (env.ASSETS) {
    return env.ASSETS.fetch(request);
  }
  return new Response('Not found', { status: 404 });
}
