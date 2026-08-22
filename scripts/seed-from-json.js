#!/usr/bin/env node
/**
 * seed-from-json.js
 * Genera un archivo SQL de seed leyendo los data/*.json existentes
 * y produciendo INSERTs para todas las tablas D1.
 *
 * Uso:
 *   node scripts/seed-from-json.js > drizzle/migrations/seed_data.sql
 *   npx wrangler d1 execute manujungleforever-db --local --file=drizzle/migrations/seed_data.sql
 *   npx wrangler d1 execute manujungleforever-db --remote --file=drizzle/migrations/seed_data.sql
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'www.manujungleforever.com', 'data');
const now = new Date().toISOString();

function esc(v) {
  if (v === null || v === undefined) return 'NULL';
  if (typeof v === 'number') return v;
  if (typeof v === 'boolean') return v ? 1 : 0;
  return `'${String(v).replace(/'/g, "''")}'`;
}

function read(file) {
  try {
    return JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'));
  } catch(e) {
    console.error('Could not read ' + file + ': ' + e.message);
    return null;
  }
}

const lines = [];
lines.push('-- Seed generated from data/*.json on ' + now);
lines.push('PRAGMA foreign_keys = OFF;');
lines.push('');

// ── TOURS ──────────────────────────────────────────────────────────────────
const toursData = read('tours.json');
if (toursData?.tours?.length) {
  lines.push('-- tours');
  for (const t of toursData.tours) {
    const id = t.id || t.slug;
    lines.push(
      `INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at, updated_at) VALUES (` +
      [
        esc(id), esc(t.slug), esc(t.nombre), esc(t.categoria || 'General'),
        esc(t.estado || 'activo'), esc(t.duracion_dias || 1), esc(t.duracion_noches || 0),
        esc(t.precio_desde || 0), esc(t.moneda || 'USD'),
        esc(t.capacidad_min || 1), esc(t.capacidad_max || 8),
        esc(t.dificultad || null), esc(t.temporada || null),
        esc(t.descripcion_corta || null), esc(t.descripcion_larga || null),
        esc(t.imagen_hero || null), esc(t.imagen_alt || null),
        esc(t.galeria ? JSON.stringify(t.galeria) : null),
        esc(t.itinerario ? JSON.stringify(t.itinerario) : null),
        esc(t.transporte ? JSON.stringify(t.transporte) : null),
        esc(t.created_at || now), esc(t.updated_at || now)
      ].join(', ') + `);`
    );
  }
  lines.push('');
}

// ── BLOG POSTS ─────────────────────────────────────────────────────────────
const postsData = read('posts-index.json');
if (postsData?.posts?.length) {
  lines.push('-- blog_posts');
  for (const p of postsData.posts) {
    const id = p.id || ('post_' + (p.slug || '').replace(/-/g, '_'));
    lines.push(
      `INSERT OR REPLACE INTO blog_posts (id, slug, titulo, autor, fecha, categoria, extracto, contenido, imagen_hero, estado, created_at, updated_at) VALUES (` +
      [
        esc(id), esc(p.slug), esc(p.titulo || p.title || ''),
        esc(p.autor || p.author || 'Manu Jungle Forever'),
        esc(p.fecha || p.date || now.split('T')[0]),
        esc(p.categoria || p.category || 'Naturaleza'),
        esc(p.extracto || p.excerpt || null),
        esc(p.contenido || p.content || ''),
        esc(p.imagen_hero || p.image || null),
        esc(p.publicado === false ? 'borrador' : (p.estado || 'publicado')),
        esc(p.created_at || now), esc(p.updated_at || now)
      ].join(', ') + `);`
    );
  }
  lines.push('');
}

// ── TESTIMONIALS ───────────────────────────────────────────────────────────
const testData = read('testimonials.json');
const testList = testData?.testimonials || testData?.testimonios;
if (testList?.length) {
  lines.push('-- testimonials');
  for (const t of testList) {
    const id = String(t.id || ('test_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6)));
    const estado = (t.activo === false || t.estado === 'oculto') ? 'oculto' : 'publicado';
    lines.push(
      `INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES (` +
      [
        esc(id), esc(t.nombre), esc(t.pais || null), esc(t.tour || t.tour_nombre || null),
        esc(t.rating || 5), esc(t.texto || t.comentario || ''), esc(t.foto || null),
        esc(t.fecha || now.split('T')[0]),
        esc(t.origen || 'manual'), esc(estado),
        esc(t.created_at || now)
      ].join(', ') + `);`
    );
  }
  lines.push('');
}

// ── DEPARTURES ─────────────────────────────────────────────────────────────
const depData = read('departures.json');
if (depData?.salidas?.length) {
  lines.push('-- departures');
  for (const s of depData.salidas) {
    lines.push(
      `INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at, updated_at) VALUES (` +
      [
        esc(s.id), esc(s.tour_id || null), esc(s.tour_nombre || ''),
        esc(s.fecha_salida), esc(s.fecha_retorno || null),
        esc(s.cupos_totales || 8), esc(s.precio || 0),
        esc(s.moneda || 'USD'), esc(s.guia_asignado || null),
        esc(s.estado || 'confirmada'),
        esc(s.created_at || now), esc(s.updated_at || now)
      ].join(', ') + `);`
    );
  }
  lines.push('');
}

// ── SITE CONTENT ───────────────────────────────────────────────────────────
lines.push('-- site_content');
for (const key of ['about', 'home', 'contact', 'global']) {
  const data = read(key + '.json');
  if (data) {
    lines.push(
      `INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES (${esc(key)}, ${esc(JSON.stringify(data))}, ${esc(now)});`
    );
  }
}
lines.push('');

lines.push('PRAGMA foreign_keys = ON;');
lines.push('-- Seed complete');

console.log(lines.join('\n'));
