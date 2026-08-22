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

// ── CREATE OR UPDATE TOUR (SINGLE OR BATCH) ──
toursRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const tourList = Array.isArray(body.tours) ? body.tours : [body];
  const now = new Date().toISOString();

  for (const t of tourList) {
    if (!t.slug && !t.nombre) continue;
    const id = t.id || t.slug;
    await db.insert(schema.tours).values({
      id,
      slug: t.slug,
      nombre: t.nombre,
      categoria: t.categoria || 'General',
      estado: t.estado || 'activo',
      duracionDias: t.duracion_dias || 1,
      duracionNoches: t.duracion_noches || 0,
      precioDesde: t.precio_desde || 0,
      moneda: t.moneda || 'USD',
      capacidadMin: t.capacidad_min || 1,
      capacidadMax: t.capacidad_max || 8,
      dificultad: t.dificultad || null,
      temporada: t.temporada || null,
      descripcionCorta: t.descripcion_corta || null,
      descripcionLarga: t.descripcion_larga || null,
      imagenHero: t.imagen_hero || null,
      imagenAlt: t.imagen_alt || null,
      galeriaJson: t.galeria ? JSON.stringify(t.galeria) : null,
      itinerarioJson: t.itinerario ? JSON.stringify(t.itinerario) : null,
      transporteJson: t.transporte ? JSON.stringify(t.transporte) : null,
      createdAt: t.created_at || now,
      updatedAt: now
    }).onConflictDoUpdate({
      target: schema.tours.id,
      set: {
        slug: t.slug,
        nombre: t.nombre,
        categoria: t.categoria || 'General',
        estado: t.estado,
        duracionDias: t.duracion_dias,
        duracionNoches: t.duracion_noches,
        precioDesde: t.precio_desde,
        moneda: t.moneda,
        capacidadMin: t.capacidad_min,
        capacidadMax: t.capacidad_max,
        dificultad: t.dificultad,
        temporada: t.temporada,
        descripcionCorta: t.descripcion_corta,
        descripcionLarga: t.descripcion_larga,
        imagenHero: t.imagen_hero,
        imagenAlt: t.imagen_alt,
        galeriaJson: t.galeria ? JSON.stringify(t.galeria) : null,
        itinerarioJson: t.itinerario ? JSON.stringify(t.itinerario) : null,
        transporteJson: t.transporte ? JSON.stringify(t.transporte) : null,
        updatedAt: now
      }
    });
  }

  return c.json({ ok: true, count: tourList.length }, 201);
});

// ── DELETE TOUR ──
toursRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.tours).where(eq(schema.tours.id, id));
  return c.json({ ok: true });
});
