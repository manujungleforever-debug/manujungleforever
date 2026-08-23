import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const reclamosRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET ALL RECLAMOS (ADMIN) ──
reclamosRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const list = await db.select().from(schema.reclamos).orderBy(desc(schema.reclamos.id)).all();
  const formatted = list.map(r => ({
    id: r.id,
    codigo_reclamo: r.codigoReclamo,
    codigoReclamo: r.codigoReclamo,
    fecha: r.fecha,
    nombres: r.nombres,
    documento: r.documento,
    domicilio: r.domicilio,
    telefono: r.telefono,
    correo: r.correo,
    email: r.correo,
    apoderado: r.apoderado,
    bien_tipo: r.bienTipo,
    bienTipo: r.bienTipo,
    bien_monto: r.bienMonto,
    bienMonto: r.bienMonto,
    bien_descripcion: r.bienDescripcion,
    bienDescripcion: r.bienDescripcion,
    tipo: r.tipo,
    detalle: r.detalle,
    pedido: r.pedido,
    estado: r.estado || 'Pendiente',
    detalle_respuesta: r.detalleRespuesta,
    detalleRespuesta: r.detalleRespuesta,
    fecha_respuesta: r.fechaRespuesta,
    fechaRespuesta: r.fechaRespuesta
  }));
  return c.json({ reclamos: formatted, list: formatted });
});

// ── SUBMIT NEW RECLAMO (PUBLIC) ──
reclamosRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const year = new Date().getFullYear();
  const countRes = await db.select().from(schema.reclamos).all();
  const nextNum = String(countRes.length + 1).padStart(4, '0');
  const codigoReclamo = `REC-${year}-${nextNum}`;

  await db.insert(schema.reclamos).values({
    codigoReclamo,
    fecha: body.fecha || new Date().toLocaleDateString('es-PE'),
    nombres: body.nombres,
    documento: body.documento,
    domicilio: body.domicilio,
    telefono: body.telefono,
    correo: body.correo,
    apoderado: body.apoderado || null,
    bienTipo: body.bien_tipo || null,
    bienMonto: body.bien_monto || null,
    bienDescripcion: body.bien_descripcion || null,
    tipo: body.tipo || 'Reclamo',
    detalle: body.detalle,
    pedido: body.pedido,
    estado: 'Pendiente'
  });

  return c.json({
    ok: true,
    codigo_reclamo: codigoReclamo,
    message: 'Reclamo registrado exitosamente'
  }, 201);
});

// ── RESPONDER RECLAMO (ADMIN) ──
reclamosRoutes.put('/:id/responder', async (c) => {
  const db = getDb(c.env.DB);
  const id = Number(c.req.param('id'));
  const body = await c.req.json();

  await db.update(schema.reclamos).set({
    estado: 'Atendido',
    detalleRespuesta: body.detalle_respuesta,
    fechaRespuesta: new Date().toLocaleDateString('es-PE')
  }).where(eq(schema.reclamos.id, id));

  return c.json({ ok: true });
});
