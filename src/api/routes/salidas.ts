import { Hono } from 'hono';
import { eq, desc, or } from 'drizzle-orm';
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
    const rawDisp = (dep as any).cuposDisponibles ?? (dep as any).cupos_disponibles;
    const cuposDisponibles = (rawDisp !== null && rawDisp !== undefined)
      ? Number(rawDisp)
      : Math.max(0, dep.cuposTotales - cuposOcupados);
    const cuposMinimos = (dep as any).cuposMinimos ?? (dep as any).cupos_minimos ?? 2;

    if (isPublic) {
      return {
        id: dep.id,
        tour_id: dep.tourId,
        tour_nombre: dep.tourNombre,
        fecha_salida: dep.fechaSalida,
        fecha_retorno: dep.fechaRetorno,
        cupos_totales: dep.cuposTotales,
        cupos_minimos: cuposMinimos,
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
      fecha_regreso: dep.fechaRetorno,
      cupos_totales: dep.cuposTotales,
      plazas_totales: dep.cuposTotales,
      cupos_minimos: cuposMinimos,
      plazas_minimas: cuposMinimos,
      cupos_disponibles: cuposDisponibles,
      plazas_disponibles: cuposDisponibles,
      precio: dep.precio,
      moneda: dep.moneda,
      guia_asignado: dep.guiaAsignado || '',
      notas: dep.notas || '',
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

  return c.json({ salidas: result, departures: result });
});

// ── BATCH SAVE DEPARTURES ──
salidasRoutes.put('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();
  const list = Array.isArray(body) ? body : (body.salidas || [body]);

  await Promise.all(list.map(async (dep: any) => {
    if (!dep || !dep.id) return;
    const tourNombre = dep.tour_nombre || dep.nombre || 'Tour';
    const fechaSalida = dep.fecha_salida || new Date().toISOString().split('T')[0];
    const fechaRetorno = dep.fecha_retorno || dep.fecha_regreso || null;
    const cuposTotales = Number(dep.cupos_totales ?? dep.plazas_totales ?? 8);
    const cuposMinimos = Number(dep.cupos_minimos ?? dep.plazas_minimas ?? 2);
    const cuposDisponibles = (dep.cupos_disponibles !== undefined || dep.plazas_disponibles !== undefined)
      ? Number(dep.cupos_disponibles ?? dep.plazas_disponibles)
      : null;
    const precio = Number(dep.precio || 0);
    const guiaAsignado = dep.guiaAsignado || dep.guia_asignado || null;
    const notas = dep.notas || null;
    const estado = dep.estado || 'confirmada';

    await db.insert(schema.departures).values({
      id: dep.id,
      tourId: dep.tour_id || null,
      tourNombre,
      fechaSalida,
      fechaRetorno,
      cuposTotales,
      cuposMinimos,
      cuposDisponibles,
      precio,
      moneda: dep.moneda || 'USD',
      guiaAsignado,
      notas,
      estado,
      createdAt: dep.created_at || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }).onConflictDoUpdate({
      target: schema.departures.id,
      set: {
        tourNombre,
        fechaSalida,
        fechaRetorno,
        cuposTotales,
        cuposMinimos,
        cuposDisponibles,
        precio,
        guiaAsignado,
        notas,
        estado,
        updatedAt: new Date().toISOString()
      }
    });
  }));

  return c.json({ ok: true });
});

// ── CREATE DEPARTURE ──
salidasRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const id = body.id || ('DEP-' + String(Date.now()).slice(-4));
  const tourNombre = body.tour_nombre || body.nombre || 'Tour';
  const fechaSalida = body.fecha_salida || new Date().toISOString().split('T')[0];
  const fechaRetorno = body.fecha_retorno || body.fecha_regreso || null;
  const cuposTotales = Number(body.cupos_totales || body.plazas_totales || 8);
  const cuposMinimos = Number(body.cupos_minimos || body.plazas_minimas || 2);
  const cuposDisponibles = (body.cupos_disponibles !== undefined || body.plazas_disponibles !== undefined)
    ? Number(body.cupos_disponibles ?? body.plazas_disponibles)
    : null;
  const precio = Number(body.precio || 0);
  const guiaAsignado = body.guia_asignado || null;
  const notas = body.notas || null;
  const estado = body.estado || 'confirmada';

  await db.insert(schema.departures).values({
    id,
    tourId: body.tour_id || null,
    tourNombre,
    fechaSalida,
    fechaRetorno,
    cuposTotales,
    cuposMinimos,
    cuposDisponibles,
    precio,
    moneda: body.moneda || 'USD',
    guiaAsignado,
    notas,
    estado,
    createdAt: new Date().toISOString()
  }).onConflictDoUpdate({
    target: schema.departures.id,
    set: {
      tourNombre,
      fechaSalida,
      fechaRetorno,
      cuposTotales,
      cuposMinimos,
      cuposDisponibles,
      precio,
      guiaAsignado,
      notas,
      estado,
      updatedAt: new Date().toISOString()
    }
  });

  return c.json({ ok: true, id }, 201);
});

// ── UPDATE DEPARTURE ──
salidasRoutes.put('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');
  const body = await c.req.json();

  const updates: Partial<typeof schema.departures.$inferInsert> = {
    updatedAt: new Date().toISOString()
  };

  if (body.tour_nombre || body.nombre) updates.tourNombre = body.tour_nombre || body.nombre;
  if (body.fecha_salida) updates.fechaSalida = body.fecha_salida;
  if (body.fecha_retorno !== undefined || body.fecha_regreso !== undefined) {
    updates.fechaRetorno = body.fecha_retorno || body.fecha_regreso || null;
  }
  if (body.cupos_totales !== undefined || body.plazas_totales !== undefined) {
    updates.cuposTotales = Number(body.cupos_totales ?? body.plazas_totales);
  }
  if (body.cupos_minimos !== undefined || body.plazas_minimas !== undefined) {
    updates.cuposMinimos = Number(body.cupos_minimos ?? body.plazas_minimas);
  }
  if (body.cupos_disponibles !== undefined || body.plazas_disponibles !== undefined) {
    updates.cuposDisponibles = Number(body.cupos_disponibles ?? body.plazas_disponibles);
  }
  if (body.precio !== undefined) updates.precio = Number(body.precio);
  if (body.guia_asignado !== undefined) updates.guiaAsignado = body.guia_asignado || null;
  if (body.notas !== undefined) updates.notas = body.notas || null;
  if (body.estado) updates.estado = body.estado;

  // Case-insensitive ID update
  await db.update(schema.departures)
    .set(updates)
    .where(or(
      eq(schema.departures.id, id),
      eq(schema.departures.id, id.toLowerCase()),
      eq(schema.departures.id, id.toUpperCase())
    ));

  return c.json({ ok: true });
});

// ── DELETE DEPARTURE ──
salidasRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.departures).where(or(
    eq(schema.departures.id, id),
    eq(schema.departures.id, id.toLowerCase()),
    eq(schema.departures.id, id.toUpperCase())
  ));
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
