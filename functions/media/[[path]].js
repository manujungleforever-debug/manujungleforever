export async function onRequestGet(context) {
  const { request, env, params } = context;

  if (!env.MEDIA_BUCKET) {
    return new Response('R2 MEDIA_BUCKET no configurado', { status: 500 });
  }

  // params.path es un array con las partes de la URL
  // ej: /media/foto.jpg -> params.path = ['foto.jpg']
  const fileKey = params.path ? params.path.join('/') : null;

  if (!fileKey) {
    return new Response('Archivo no especificado', { status: 400 });
  }

  try {
    const object = await env.MEDIA_BUCKET.get(fileKey);

    if (object === null) {
      return new Response('Archivo no encontrado', { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('etag', object.httpEtag);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable'); // Cache por 1 año

    return new Response(object.body, { headers });
  } catch (e) {
    return new Response('Error interno del servidor', { status: 500 });
  }
}
