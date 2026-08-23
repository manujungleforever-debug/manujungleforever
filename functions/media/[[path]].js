export async function onRequestGet(context) {
  const { request, env, params } = context;

  // params.path es un array con las partes de la URL
  // ej: /media/foto.jpg -> params.path = ['foto.jpg']
  const fileKey = params.path ? params.path.join('/') : null;

  if (!fileKey) {
    return new Response('Archivo no especificado', { status: 400 });
  }

  try {
    // 1. Intentar cargar desde el bucket R2
    if (env.MEDIA_BUCKET) {
      const object = await env.MEDIA_BUCKET.get(fileKey);
      if (object !== null) {
        const headers = new Headers();
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);
        headers.set('Cache-Control', 'public, max-age=31536000, immutable');
        return new Response(object.body, { headers });
      }
    }

    // 2. Intentar buscar en assets estáticos si existe
    if (env.ASSETS) {
      const assetRes = await env.ASSETS.fetch(new URL(`/assets/img/${fileKey.split('/').pop()}`, request.url)).catch(() => null);
      if (assetRes && assetRes.ok) {
        return assetRes;
      }
    }

    // 3. Fallback inteligente a producción R2 y GitHub raw si el archivo no está en R2 local
    const REPO = 'manujungleforever-debug/manujungleforever';
    const BRANCH = 'main';
    const rawPaths = [
      `https://www.manujungleforever.com/media/${fileKey}`,
      `https://raw.githubusercontent.com/${REPO}/${BRANCH}/www.manujungleforever.com/media/${fileKey}`,
      `https://raw.githubusercontent.com/${REPO}/${BRANCH}/www.manujungleforever.com/assets/img/${fileKey.split('/').pop()}`,
      `https://raw.githubusercontent.com/${REPO}/${BRANCH}/www.manujungleforever.com/assets/img/hero.png`
    ];

    for (const rawUrl of rawPaths) {
      try {
        const rawRes = await fetch(rawUrl).catch(() => null);
        if (rawRes && rawRes.ok) {
          const contentType = rawRes.headers.get('Content-Type') || (fileKey.endsWith('.png') ? 'image/png' : 'image/jpeg');
          return new Response(rawRes.body, {
            status: 200,
            headers: {
              'Content-Type': contentType,
              'Cache-Control': 'public, max-age=86400',
              'Access-Control-Allow-Origin': '*'
            }
          });
        }
      } catch {}
    }

    // 4. Fallback final: Si env.ASSETS está disponible, retornar hero.png por defecto
    if (env.ASSETS) {
      const fallbackHero = await env.ASSETS.fetch(new URL('/assets/img/hero.png', request.url)).catch(() => null);
      if (fallbackHero && fallbackHero.ok) {
        return fallbackHero;
      }
    }

    return new Response('Archivo no encontrado', { status: 404 });
  } catch (e) {
    return new Response('Error interno del servidor: ' + e.message, { status: 500 });
  }
}

export const onRequest = onRequestGet;
export const onRequestHead = onRequestGet;

