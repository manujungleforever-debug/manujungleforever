import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const testimonialsRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET TESTIMONIALS ──
testimonialsRoutes.get('/', async (c) => {
  try {
    const db = getDb(c.env.DB);
    const isPublic = c.req.query('public') === 'true';

    let list = await db.select().from(schema.testimonials).all();
    if (isPublic) {
      list = list.filter(t => t.estado === 'publicado');
    }

    const formatted = list.map(t => ({
      id: t.id,
      nombre: t.nombre,
      pais: t.pais,
      tour: t.tourNombre,
      tour_nombre: t.tourNombre,
      rating: t.rating,
      texto: t.comentario,
      comentario: t.comentario,
      foto: t.foto,
      fecha: t.fecha,
      origen: t.origen || 'manual',
      estado: t.estado,
      activo: t.estado === 'publicado',
      created_at: t.createdAt
    }));

    return c.json({ testimonios: formatted, testimonials: formatted });
  } catch (err: any) {
    return c.json({ error: err.message, testimonios: [], testimonials: [] }, 500);
  }
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

// ── UPDATE TESTIMONIAL ──
testimonialsRoutes.put('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');
  const body = await c.req.json();

  await db.update(schema.testimonials).set({
    nombre: body.nombre,
    pais: body.pais || null,
    tourNombre: body.tour_nombre || null,
    rating: body.rating || 5,
    comentario: body.comentario,
    foto: body.foto || null,
    fecha: body.fecha,
    origen: body.origen || 'manual',
    estado: body.estado || 'publicado'
  }).where(eq(schema.testimonials.id, id));

  return c.json({ ok: true });
});

// ── DELETE TESTIMONIAL ──
testimonialsRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.testimonials).where(eq(schema.testimonials.id, id));
  return c.json({ ok: true });
});
