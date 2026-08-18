import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core';

// ── 1. USERS & ROLES ──
export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  passwordHash: text('password_hash').notNull(),
  name: text('name').notNull(),
  role: text('role', { enum: ['admin', 'editor', 'guia'] }).default('admin').notNull(),
  createdAt: text('created_at').notNull(),
  updatedAt: text('updated_at')
});

// ── 2. TOURS CATALOG ──
export const tours = sqliteTable('tours', {
  id: text('id').primaryKey(),
  slug: text('slug').notNull().unique(),
  nombre: text('nombre').notNull(),
  categoria: text('categoria').notNull(),
  estado: text('estado', { enum: ['activo', 'inactivo', 'borrador'] }).default('activo').notNull(),
  duracionDias: integer('duracion_dias').notNull(),
  duracionNoches: integer('duracion_noches').notNull(),
  precioDesde: real('precio_desde').notNull(),
  moneda: text('moneda').default('USD').notNull(),
  capacidadMin: integer('capacidad_min').default(1),
  capacidadMax: integer('capacidad_max').default(8),
  dificultad: text('dificultad'),
  temporada: text('temporada'),
  descripcionCorta: text('descripcion_corta'),
  descripcionLarga: text('descripcion_larga'),
  imagenHero: text('imagen_hero'),
  imagenAlt: text('imagen_alt'),
  galeriaJson: text('galeria_json'),
  itinerarioJson: text('itinerario_json'),
  transporteJson: text('transporte_json'),
  createdAt: text('created_at').notNull(),
  updatedAt: text('updated_at')
});

// ── 3. DEPARTURES (SALIDAS) ──
export const departures = sqliteTable('departures', {
  id: text('id').primaryKey(),
  tourId: text('tour_id').references(() => tours.id),
  tourNombre: text('tour_nombre').notNull(),
  fechaSalida: text('fecha_salida').notNull(),
  fechaRetorno: text('fecha_retorno'),
  cuposTotales: integer('cupos_totales').default(8).notNull(),
  precio: real('precio').notNull(),
  moneda: text('moneda').default('USD').notNull(),
  guiaAsignado: text('guia_asignado'),
  estado: text('estado', { enum: ['programada', 'confirmada', 'completada', 'cancelada'] }).default('confirmada').notNull(),
  createdAt: text('created_at').notNull(),
  updatedAt: text('updated_at')
});

// ── 4. PASSENGERS (PASAJEROS) ──
export const passengers = sqliteTable('passengers', {
  id: text('id').primaryKey(),
  departureId: text('departure_id').notNull().references(() => departures.id, { onDelete: 'cascade' }),
  nombreCompleto: text('nombre_completo').notNull(),
  nacionalidad: text('nacionalidad'),
  fechaNacimiento: text('fecha_nacimiento'),
  pasaporte: text('pasaporte'),
  whatsapp: text('whatsapp'),
  email: text('email'),
  restriccionesDieteticas: text('restricciones_dieteticas'),
  condicionesMedicas: text('condiciones_medicas'),
  costo: real('costo').default(0),
  montoPagado: real('monto_pagado').default(0),
  saldoPendiente: real('saldo_pendiente').default(0),
  estadoPago: text('estado_pago', { enum: ['pendiente', 'reserva', 'pagado'] }).default('pendiente').notNull(),
  foto: text('foto'),
  createdAt: text('created_at').notNull(),
  updatedAt: text('updated_at')
});

// ── 5. BLOG POSTS ──
export const blogPosts = sqliteTable('blog_posts', {
  id: text('id').primaryKey(),
  slug: text('slug').notNull().unique(),
  titulo: text('titulo').notNull(),
  autor: text('autor').default('Manu Jungle Forever'),
  fecha: text('fecha').notNull(),
  categoria: text('categoria'),
  extracto: text('extracto'),
  contenido: text('contenido').notNull(),
  imagenHero: text('imagen_hero'),
  estado: text('estado', { enum: ['publicado', 'borrador'] }).default('publicado').notNull(),
  createdAt: text('created_at').notNull(),
  updatedAt: text('updated_at')
});

// ── 6. TESTIMONIALS ──
export const testimonials = sqliteTable('testimonials', {
  id: text('id').primaryKey(),
  nombre: text('nombre').notNull(),
  pais: text('pais'),
  tourNombre: text('tour_nombre'),
  rating: integer('rating').default(5),
  comentario: text('comentario').notNull(),
  foto: text('foto'),
  fecha: text('fecha').notNull(),
  estado: text('estado', { enum: ['publicado', 'oculto'] }).default('publicado').notNull(),
  createdAt: text('created_at').notNull()
});

// ── 7. RECLAMOS (LIBRO DE RECLAMACIONES) ──
export const reclamos = sqliteTable('reclamos', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  codigoReclamo: text('codigo_reclamo').notNull().unique(),
  fecha: text('fecha').notNull(),
  nombres: text('nombres').notNull(),
  documento: text('documento').notNull(),
  domicilio: text('domicilio').notNull(),
  telefono: text('telefono').notNull(),
  correo: text('correo').notNull(),
  apoderado: text('apoderado'),
  bienTipo: text('bien_tipo'),
  bienMonto: text('bien_monto'),
  bienDescripcion: text('bien_descripcion'),
  tipo: text('tipo').notNull(),
  detalle: text('detalle').notNull(),
  pedido: text('pedido').notNull(),
  estado: text('estado').default('Pendiente'),
  detalleRespuesta: text('detalle_respuesta'),
  fechaRespuesta: text('fecha_respuesta')
});
