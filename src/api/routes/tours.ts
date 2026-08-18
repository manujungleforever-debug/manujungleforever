import { Hono } from 'hono';
import { eq } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const toursRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET ALL TOURS ──
toursRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const isPublic = c.req.query('public') === 'true';

  let list = await db.select().from(schema.tours).all();
  if (isPublic) {
    list = list.filter(t => t.estado === 'activo');
  }

  const formatted = list.map(t => ({
    id: t.id,
    slug: t.slug,
    nombre: t.nombre,
    categoria: t.categoria,
    estado: t.estado,
    duracion_dias: t.duracionDias,
    duracion_noches: t.duracionNoches,
    precio_desde: t.precioDesde,
    moneda: t.moneda,
    capacidad_min: t.capacidadMin,
    capacidad_max: t.capacidadMax,
    dificultad: t.dificultad,
    temporada: t.temporada,
    descripcion_corta: t.descripcionCorta,
    descripcion_larga: t.descripcionLarga,
    imagen_hero: t.imagenHero,
    imagen_alt: t.imagenAlt,
    galeria: t.galeriaJson ? JSON.parse(t.galeriaJson) : [],
    itinerario: t.itinerarioJson ? JSON.parse(t.itinerarioJson) : [],
    transporte: t.transporteJson ? JSON.parse(t.transporteJson) : []
  }));

  return c.json({ tours: formatted });
});

// ── GET TOUR BY SLUG ──
toursRoutes.get('/:slug', async (c) => {
  const db = getDb(c.env.DB);
  const slug = c.req.param('slug');
  const t = await db.select().from(schema.tours).where(eq(schema.tours.slug, slug)).get();

  if (!t) return c.json({ error: 'Tour no encontrado' }, 404);

  return c.json({
    id: t.id,
    slug: t.slug,
    nombre: t.nombre,
    categoria: t.categoria,
    estado: t.estado,
    duracion_dias: t.duracionDias,
    duracion_noches: t.duracionNoches,
    precio_desde: t.precioDesde,
    moneda: t.moneda,
    capacidad_min: t.capacidadMin,
    capacidad_max: t.capacidadMax,
    dificultad: t.dificultad,
    temporada: t.temporada,
    descripcion_corta: t.descripcionCorta,
    descripcion_larga: t.descripcionLarga,
    imagen_hero: t.imagenHero,
    imagen_alt: t.imagenAlt,
    galeria: t.galeriaJson ? JSON.parse(t.galeriaJson) : [],
    itinerario: t.itinerarioJson ? JSON.parse(t.itinerarioJson) : [],
    transporte: t.transporteJson ? JSON.parse(t.transporteJson) : []
  });
});

// ── CREATE OR UPDATE TOUR ──
toursRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const id = body.id || body.slug;
  await db.insert(schema.tours).values({
    id,
    slug: body.slug,
    nombre: body.nombre,
    categoria: body.categoria,
    estado: body.estado || 'activo',
    duracionDias: body.duracion_dias || 1,
    duracionNoches: body.duracion_noches || 0,
    precioDesde: body.precio_desde || 0,
    moneda: body.moneda || 'USD',
    capacidadMin: body.capacidad_min || 1,
    capacidadMax: body.capacidad_max || 8,
    dificultad: body.dificultad || null,
    temporada: body.temporada || null,
    descripcionCorta: body.descripcion_corta || null,
    descripcionLarga: body.descripcion_larga || null,
    imagenHero: body.imagen_hero || null,
    imagenAlt: body.imagen_alt || null,
    galeriaJson: body.galeria ? JSON.stringify(body.galeria) : null,
    itinerarioJson: body.itinerario ? JSON.stringify(body.itinerario) : null,
    transporteJson: body.transporte ? JSON.stringify(body.transporte) : null,
    createdAt: new Date().toISOString()
  }).onConflictDoUpdate({
    target: schema.tours.id,
    set: {
      slug: body.slug,
      nombre: body.nombre,
      categoria: body.categoria,
      estado: body.estado,
      duracionDias: body.duracion_dias,
      duracionNoches: body.duracion_noches,
      precioDesde: body.precio_desde,
      moneda: body.moneda,
      capacidadMin: body.capacidad_min,
      capacidadMax: body.capacidad_max,
      dificultad: body.dificultad,
      temporada: body.temporada,
      descripcionCorta: body.descripcion_corta,
      descripcionLarga: body.descripcion_larga,
      imagenHero: body.imagen_hero,
      imagenAlt: body.imagen_alt,
      galeriaJson: body.galeria ? JSON.stringify(body.galeria) : null,
      itinerarioJson: body.itinerario ? JSON.stringify(body.itinerario) : null,
      transporteJson: body.transporte ? JSON.stringify(body.transporte) : null,
      updatedAt: new Date().toISOString()
    }
  });

  return c.json({ ok: true, id }, 201);
});

// ── DELETE TOUR ──
toursRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.tours).where(eq(schema.tours.id, id));
  return c.json({ ok: true });
});
