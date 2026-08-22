export async function onRequestGet(context) {
  const { request, env, params } = context;

  // params.path es un array con las partes de la URL
  // ej: /media/foto.jpg -> params.path = ['foto.jpg']
  const fileKey = params.path ? params.path.join('/') : null;

  if (!fileKey) {
    return new Response('Archivo no especificado', { status: 400 });
  }

  try {
    if (env.MEDIA_BUCKET) {
      const object = await env.MEDIA_BUCKET.get(fileKey);
      if (object !== null) {
        const headers = new Headers();
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);
        headers.set('Cache-Control', 'public, max-age=31536000, immutable'); // Cache por 1 año
        return new Response(object.body, { headers });
      }
    }

    // Fallback: proxy a producción si no existe en el bucket local dev
    const prodUrl = `https://manujungleforever.pages.dev/media/${encodeURIComponent(fileKey).replace(/%2F/g, '/')}`;
    const prodRes = await fetch(prodUrl).catch(() => null);
    if (prodRes && prodRes.ok) {
      return new Response(prodRes.body, {
        status: 200,
        headers: {
          'Content-Type': prodRes.headers.get('Content-Type') || 'image/jpeg',
          'Cache-Control': 'public, max-age=86400',
        }
      });
    }

    return new Response('Archivo no encontrado', { status: 404 });
  } catch (e) {
    return new Response('Error interno del servidor: ' + e.message, { status: 500 });
  }
}
