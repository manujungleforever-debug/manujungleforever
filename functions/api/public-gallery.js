export async function onRequestGet(context) {
  const { env } = context;
  
  if (!env.MEDIA_BUCKET) {
    return new Response(JSON.stringify({ error: 'R2 MEDIA_BUCKET no configurado' }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
  
  try {
    const list = await env.MEDIA_BUCKET.list({ prefix: 'medios/gallery/', limit: 1000 });
    const files = list.objects.map(obj => ({
      key: obj.key,
      url: `/media/${obj.key}`
    }));
    
    return new Response(JSON.stringify({ files }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300'
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Error listando bucket: ' + e.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
}
