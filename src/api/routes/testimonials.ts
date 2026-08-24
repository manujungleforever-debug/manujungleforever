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
      bandera: t.bandera || '',
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

// ── CREATE OR UPDATE TESTIMONIAL(S) ──
testimonialsRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const list = Array.isArray(body) ? body : (Array.isArray(body.testimonials || body.testimonios) ? (body.testimonials || body.testimonios) : [body]);
  const now = new Date().toISOString();
  const createdIds: string[] = [];

  for (const item of list) {
    if (!item.nombre && !item.comentario && !item.texto) continue;
    const id = String(item.id || ('test_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6)));
    const estado = item.estado || (item.activo === false ? 'oculto' : 'publicado');
    const comentario = item.texto !== undefined ? item.texto : (item.comentario || '');
    const tourNombre = item.tour || item.tour_nombre || null;
    const pais = item.pais || null;
    const rating = typeof item.rating === 'number' ? item.rating : 5;
    const foto = item.foto || null;
    const fecha = item.fecha || now.split('T')[0];
    const origen = item.origen || 'manual';

    const bandera = item.bandera || null;

    await db.insert(schema.testimonials).values({
      id,
      nombre: item.nombre || 'Anónimo',
      pais,
      bandera,
      tourNombre,
      rating,
      comentario,
      foto,
      fecha,
      origen,
      estado,
      createdAt: item.createdAt || item.created_at || now
    }).onConflictDoUpdate({
      target: schema.testimonials.id,
      set: {
        nombre: item.nombre || 'Anónimo',
        pais,
        bandera,
        tourNombre,
        rating,
        comentario,
        foto,
        fecha,
        origen,
        estado
      }
    });

    createdIds.push(id);
  }

  c.header('Cache-Control', 'no-cache, no-store, must-revalidate');
  return c.json({ ok: true, count: createdIds.length, ids: createdIds }, 201);
});

// ── UPDATE TESTIMONIAL ──
testimonialsRoutes.put('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');
  const body = await c.req.json();

  const updates: Partial<typeof schema.testimonials.$inferInsert> = {};
  if (body.nombre) updates.nombre = body.nombre;
  if (body.pais !== undefined) updates.pais = body.pais;
  if (body.bandera !== undefined) updates.bandera = body.bandera;
  if (body.tour !== undefined || body.tour_nombre !== undefined) updates.tourNombre = body.tour || body.tour_nombre;
  if (body.rating !== undefined) updates.rating = Number(body.rating);
  if (body.texto !== undefined || body.comentario !== undefined) updates.comentario = body.texto ?? body.comentario;
  if (body.foto !== undefined) updates.foto = body.foto;
  if (body.fecha) updates.fecha = body.fecha;
  if (body.origen) updates.origen = body.origen;
  if (body.estado) updates.estado = body.estado;
  else if (body.activo !== undefined) updates.estado = body.activo ? 'publicado' : 'oculto';

  await db.update(schema.testimonials).set(updates).where(eq(schema.testimonials.id, id));
  c.header('Cache-Control', 'no-cache, no-store, must-revalidate');
  return c.json({ ok: true });
});

// ── DELETE TESTIMONIAL ──
testimonialsRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.testimonials).where(eq(schema.testimonials.id, id));
  return c.json({ ok: true });
});
