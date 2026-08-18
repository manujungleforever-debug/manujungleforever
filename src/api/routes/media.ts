import { Hono } from 'hono';
import { Bindings } from '../../db';

export const mediaRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET R2 MEDIA LIST ──
mediaRoutes.get('/', async (c) => {
  const bucket = c.env.MEDIA_BUCKET;
  if (!bucket) {
    return c.json({ error: 'MEDIA_BUCKET no configurado' }, 500);
  }

  const listed = await bucket.list({ limit: 500 });
  const files = listed.objects.map(obj => ({
    key: obj.key,
    size: obj.size,
    uploaded: obj.uploaded,
    url: `/media/${encodeURIComponent(obj.key)}`
  }));

  return c.json({ files });
});

// ── UPLOAD FILE TO R2 ──
mediaRoutes.post('/', async (c) => {
  const bucket = c.env.MEDIA_BUCKET;
  if (!bucket) {
    return c.json({ error: 'MEDIA_BUCKET no configurado' }, 500);
  }

  const fileNameHeader = c.req.header('X-File-Name');
  let key = fileNameHeader ? decodeURIComponent(fileNameHeader) : 'upload_' + Date.now();
  // Sanitize key
  key = key.replace(/^\/+/, '');

  const contentType = c.req.header('Content-Type') || 'application/octet-stream';
  const body = await c.req.arrayBuffer();

  await bucket.put(key, body, {
    httpMetadata: { contentType }
  });

  const publicUrl = `/media/${encodeURIComponent(key)}`;
  return c.json({
    success: true,
    file: publicUrl,
    key
  }, 201);
});

// ── DELETE FILE FROM R2 ──
mediaRoutes.delete('/:key', async (c) => {
  const bucket = c.env.MEDIA_BUCKET;
  if (!bucket) {
    return c.json({ error: 'MEDIA_BUCKET no configurado' }, 500);
  }

  const key = decodeURIComponent(c.req.param('key'));
  await bucket.delete(key);
  return c.json({ ok: true });
});
