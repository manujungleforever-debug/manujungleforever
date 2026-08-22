const REPO   = 'manujungleforever-debug/manujungleforever';
const BRANCH = 'main';
const GH     = 'https://api.github.com';

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const filePath = params.path ? params.path.join('/') : '';
  if (!filePath) {
    return new Response('File not found', { status: 404 });
  }

  const token = env.GH_TOKEN || env.GITHUB_TOKEN;
  const fullRepoPath = `www.manujungleforever.com/data/${filePath}`;
  const ghUrl = `${GH}/repos/${REPO}/contents/${encodeURIComponent(fullRepoPath).replace(/%2F/g,'/')}?ref=${BRANCH}`;

  try {
    const ghRes = await fetch(ghUrl, {
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'HJC-CMS/1.0'
      }
    });

    if (ghRes.ok) {
      const data = await ghRes.json();
      if (data.content) {
        const bytes = Uint8Array.from(atob(data.content.replace(/\n/g, '')), c => c.charCodeAt(0));
        const content = new TextDecoder('utf-8').decode(bytes);
        return new Response(content, {
          status: 200,
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }
    }
  } catch (e) {
    // fallback
  }

  // Fallback to static asset if GitHub request fails
  if (env.ASSETS) {
    return env.ASSETS.fetch(request);
  }
  return new Response('Not found', { status: 404 });
}
