import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const salidasRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET ALL DEPARTURES WITH PASSENGERS ──
salidasRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const isPublic = c.req.query('public') === 'true';

  const departuresList = await db.select().from(schema.departures).orderBy(desc(schema.departures.fechaSalida)).all();
  const passengersList = isPublic ? [] : await db.select().from(schema.passengers).all();

  // Group passengers by departureId
  const paxMap: Record<string, typeof passengersList> = {};
  passengersList.forEach(p => {
    if (!paxMap[p.departureId]) paxMap[p.departureId] = [];
    paxMap[p.departureId].push(p);
  });

  const result = departuresList.map(dep => {
    const paxs = paxMap[dep.id] || [];
    const cuposOcupados = paxs.length;
    const cuposDisponibles = Math.max(0, dep.cuposTotales - cuposOcupados);

    if (isPublic) {
      return {
        id: dep.id,
        tour_id: dep.tourId,
        tour_nombre: dep.tourNombre,
        fecha_salida: dep.fechaSalida,
        fecha_retorno: dep.fechaRetorno,
        cupos_totales: dep.cuposTotales,
        cupos_disponibles: cuposDisponibles,
        precio: dep.precio,
        moneda: dep.moneda,
        estado: dep.estado
      };
    }

    return {
      id: dep.id,
      tour_id: dep.tourId,
      tour_nombre: dep.tourNombre,
      fecha_salida: dep.fechaSalida,
      fecha_retorno: dep.fechaRetorno,
      cupos_totales: dep.cuposTotales,
      cupos_disponibles: cuposDisponibles,
      precio: dep.precio,
      moneda: dep.moneda,
      guia_asignado: dep.guiaAsignado,
      estado: dep.estado,
      pasajeros: paxs.map(p => ({
        id: p.id,
        nombre_completo: p.nombreCompleto,
        nacionalidad: p.nacionalidad,
        fecha_nacimiento: p.fechaNacimiento,
        pasaporte: p.pasaporte,
        whatsapp: p.whatsapp,
        email: p.email,
        restricciones_dieteticas: p.restriccionesDieteticas,
        condiciones_medicas: p.condicionesMedicas,
        costo: p.costo,
        monto_pagado: p.montoPagado,
        saldo_pendiente: p.saldoPendiente,
        estado_pago: p.estadoPago,
        foto: p.foto
      }))
    };
  });

  return c.json({ salidas: result });
});

// ── CREATE DEPARTURE ──
salidasRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const id = body.id || 'dep_' + Date.now();
  await db.insert(schema.departures).values({
    id,
    tourId: body.tour_id || null,
    tourNombre: body.tour_nombre,
    fechaSalida: body.fecha_salida,
    fechaRetorno: body.fecha_retorno || null,
    cuposTotales: body.cupos_totales || 8,
    precio: body.precio || 0,
    moneda: body.moneda || 'USD',
    guiaAsignado: body.guia_asignado || null,
    estado: body.estado || 'confirmada',
    createdAt: new Date().toISOString()
  });

  return c.json({ ok: true, id }, 201);
});

// ── UPDATE DEPARTURE ──
salidasRoutes.put('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');
  const body = await c.req.json();

  await db.update(schema.departures).set({
    tourNombre: body.tour_nombre,
    fechaSalida: body.fecha_salida,
    fechaRetorno: body.fecha_retorno,
    cuposTotales: body.cupos_totales,
    precio: body.precio,
    guiaAsignado: body.guia_asignado,
    estado: body.estado,
    updatedAt: new Date().toISOString()
  }).where(eq(schema.departures.id, id));

  return c.json({ ok: true });
});

// ── DELETE DEPARTURE ──
salidasRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.departures).where(eq(schema.departures.id, id));
  return c.json({ ok: true });
});

// ── PASSENGERS MANAGEMENT ──
salidasRoutes.post('/:departureId/passengers', async (c) => {
  const db = getDb(c.env.DB);
  const departureId = c.req.param('departureId');
  const body = await c.req.json();

  const id = body.id || 'pax_' + Date.now();
  await db.insert(schema.passengers).values({
    id,
    departureId,
    nombreCompleto: body.nombre_completo,
    nacionalidad: body.nacionalidad || null,
    fechaNacimiento: body.fecha_nacimiento || null,
    pasaporte: body.pasaporte || null,
    whatsapp: body.whatsapp || null,
    email: body.email || null,
    restriccionesDieteticas: body.restricciones_dieteticas || null,
    condicionesMedicas: body.condiciones_medicas || null,
    costo: body.costo || 0,
    montoPagado: body.monto_pagado || 0,
    saldoPendiente: body.saldo_pendiente || 0,
    estadoPago: body.estado_pago || 'pendiente',
    foto: body.foto || null,
    createdAt: new Date().toISOString()
  });

  return c.json({ ok: true, id }, 201);
});

salidasRoutes.put('/:departureId/passengers/:paxId', async (c) => {
  const db = getDb(c.env.DB);
  const paxId = c.req.param('paxId');
  const body = await c.req.json();

  await db.update(schema.passengers).set({
    nombreCompleto: body.nombre_completo,
    nacionalidad: body.nacionalidad,
    fechaNacimiento: body.fecha_nacimiento,
    pasaporte: body.pasaporte,
    whatsapp: body.whatsapp,
    email: body.email,
    restriccionesDieteticas: body.restricciones_dieteticas,
    condicionesMedicas: body.condiciones_medicas,
    costo: body.costo,
    montoPagado: body.monto_pagado,
    saldoPendiente: body.saldo_pendiente,
    estadoPago: body.estado_pago,
    foto: body.foto,
    updatedAt: new Date().toISOString()
  }).where(eq(schema.passengers.id, paxId));

  return c.json({ ok: true });
});

salidasRoutes.delete('/:departureId/passengers/:paxId', async (c) => {
  const db = getDb(c.env.DB);
  const paxId = c.req.param('paxId');

  await db.delete(schema.passengers).where(eq(schema.passengers.id, paxId));
  return c.json({ ok: true });
});
