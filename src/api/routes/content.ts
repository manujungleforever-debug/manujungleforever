import { Hono } from 'hono';
import { eq } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const contentRoutes = new Hono<{ Bindings: Bindings }>();

const ALLOWED_KEYS = ['home', 'about', 'contact', 'global'];

// ── GET CONTENT BY KEY ──
contentRoutes.get('/:key', async (c) => {
  const key = c.req.param('key');
  if (!ALLOWED_KEYS.includes(key)) {
    return c.json({ error: 'Clave no permitida' }, 400);
  }

  const db = getDb(c.env.DB);
  const row = await db.select().from(schema.siteContent).where(eq(schema.siteContent.key, key)).get();

  if (!row) return c.json({ error: 'Contenido no encontrado' }, 404);

  let parsed;
  try { parsed = JSON.parse(row.value); } catch { parsed = row.value; }

  return c.json({ key, data: parsed, updatedAt: row.updatedAt });
});

// ── PUT CONTENT BY KEY (upsert) ──
contentRoutes.put('/:key', async (c) => {
  const key = c.req.param('key');
  if (!ALLOWED_KEYS.includes(key)) {
    return c.json({ error: 'Clave no permitida' }, 400);
  }

  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const value = typeof body === 'string' ? body : JSON.stringify(body);
  const updatedAt = new Date().toISOString();

  await db.insert(schema.siteContent).values({ key, value, updatedAt })
    .onConflictDoUpdate({
      target: schema.siteContent.key,
      set: { value, updatedAt }
    });

  return c.json({ ok: true, key });
});
