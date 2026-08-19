import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const testimonialsRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET TESTIMONIALS ──
testimonialsRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const isPublic = c.req.query('public') === 'true';

  let list = await db.select().from(schema.testimonials).orderBy(desc(schema.testimonials.fecha)).all();
  if (isPublic) {
    list = list.filter(t => t.estado === 'publicado');
  }

  return c.json({ testimonios: list });
});

// ── CREATE TESTIMONIAL ──
testimonialsRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const id = body.id || 'test_' + Date.now();
  await db.insert(schema.testimonials).values({
    id,
    nombre: body.nombre,
    pais: body.pais || null,
    tourNombre: body.tour_nombre || null,
    rating: body.rating || 5,
    comentario: body.comentario,
    foto: body.foto || null,
    fecha: body.fecha || new Date().toISOString().split('T')[0],
    origen: body.origen || 'manual',
    estado: body.estado || 'publicado',
    createdAt: new Date().toISOString()
  });

  return c.json({ ok: true, id }, 201);
});

// ── DELETE TESTIMONIAL ──
testimonialsRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.testimonials).where(eq(schema.testimonials.id, id));
  return c.json({ ok: true });
});
