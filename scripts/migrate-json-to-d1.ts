import fs from 'fs';
import path from 'path';

export function generateMigrationSql(): string {
  let sql = '-- Data migration from flat JSON files to Cloudflare D1\n\n';

  // 1. Tours
  const toursPath = path.join(__dirname, '../www.manujungleforever.com/data/tours.json');
  if (fs.existsSync(toursPath)) {
    const toursData = JSON.parse(fs.readFileSync(toursPath, 'utf8'));
    (toursData.tours || []).forEach((t: any) => {
      const id = t.id || t.slug;
      const slug = t.slug || t.id;
      const nombre = (t.nombre || '').replace(/'/g, "''");
      const categoria = (t.categoria || 'wildlife').replace(/'/g, "''");
      const estado = t.estado || 'activo';
      const duracionDias = t.duracion_dias || 1;
      const duracionNoches = t.duracion_noches || 0;
      const precioDesde = t.precio_desde || 0;
      const moneda = t.moneda || 'USD';
      const capacidadMin = t.capacidad_min || 1;
      const capacidadMax = t.capacidad_max || 8;
      const dificultad = (t.dificultad || '').replace(/'/g, "''");
      const temporada = (t.temporada || '').replace(/'/g, "''");
      const descripcionCorta = (t.descripcion_corta || '').replace(/'/g, "''");
      const descripcionLarga = (t.descripcion_larga || '').replace(/'/g, "''");
      const imagenHero = (t.imagen_hero || '').replace(/'/g, "''");
      const imagenAlt = (t.imagen_alt || '').replace(/'/g, "''");
      const galeriaJson = JSON.stringify(t.galeria || []).replace(/'/g, "''");
      const itinerarioJson = JSON.stringify(t.itinerario || []).replace(/'/g, "''");
      const transporteJson = JSON.stringify(t.transporte || []).replace(/'/g, "''");
      const now = new Date().toISOString();

      sql += `INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('${id}', '${slug}', '${nombre}', '${categoria}', '${estado}', ${duracionDias}, ${duracionNoches}, ${precioDesde}, '${moneda}', ${capacidadMin}, ${capacidadMax}, '${dificultad}', '${temporada}', '${descripcionCorta}', '${descripcionLarga}', '${imagenHero}', '${imagenAlt}', '${galeriaJson}', '${itinerarioJson}', '${transporteJson}', '${now}');\n`;
    });
  }

  // 2. Departures & Passengers
  const depPath = path.join(__dirname, '../www.manujungleforever.com/data/departures.json');
  if (fs.existsSync(depPath)) {
    const depData = JSON.parse(fs.readFileSync(depPath, 'utf8'));
    (depData.salidas || []).forEach((s: any) => {
      const id = s.id;
      const tourId = s.tour_id || null;
      const tourNombre = (s.tour_nombre || '').replace(/'/g, "''");
      const fechaSalida = s.fecha_salida || '';
      const fechaRetorno = s.fecha_retorno || '';
      const cuposTotales = s.cupos_totales || 8;
      const precio = s.precio || 0;
      const moneda = s.moneda || 'USD';
      const guia = (s.guia_asignado || '').replace(/'/g, "''");
      const estado = s.estado || 'confirmada';
      const now = new Date().toISOString();

      sql += `INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('${id}', ${tourId ? `'${tourId}'` : 'NULL'}, '${tourNombre}', '${fechaSalida}', '${fechaRetorno}', ${cuposTotales}, ${precio}, '${moneda}', '${guia}', '${estado}', '${now}');\n`;

      (s.pasajeros || []).forEach((p: any, idx: number) => {
        const pId = p.id || `pax_${id}_${idx + 1}`;
        const nombreCompleto = (p.nombre_completo || '').replace(/'/g, "''");
        const nacionalidad = (p.nacionalidad || '').replace(/'/g, "''");
        const fechaNac = p.fecha_nacimiento || '';
        const pasaporte = (p.pasaporte || '').replace(/'/g, "''");
        const whatsapp = (p.whatsapp || '').replace(/'/g, "''");
        const email = (p.email || '').replace(/'/g, "''");
        const diet = (p.restricciones_dieteticas || '').replace(/'/g, "''");
        const med = (p.condiciones_medicas || '').replace(/'/g, "''");
        const costo = p.costo || 0;
        const montoPagado = p.monto_pagado || 0;
        const saldoPendiente = p.saldo_pendiente || 0;
        const estadoPago = p.estado_pago || 'pendiente';
        const foto = (p.foto || '').replace(/'/g, "''");

        sql += `INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('${pId}', '${id}', '${nombreCompleto}', '${nacionalidad}', '${fechaNac}', '${pasaporte}', '${whatsapp}', '${email}', '${diet}', '${med}', ${costo}, ${montoPagado}, ${saldoPendiente}, '${estadoPago}', '${foto}', '${now}');\n`;
      });
    });
  }

  // 3. Testimonials
  const testPath = path.join(__dirname, '../www.manujungleforever.com/data/testimonials.json');
  if (fs.existsSync(testPath)) {
    const testData = JSON.parse(fs.readFileSync(testPath, 'utf8'));
    (testData.testimonials || testData.testimonios || []).forEach((t: any, idx: number) => {
      const id = t.id || `test_${idx + 1}`;
      const nombre = (t.nombre || 'Anónimo').replace(/'/g, "''");
      const pais = (t.pais || '').replace(/'/g, "''");
      const tourNombre = (t.tour_nombre || t.tour || '').replace(/'/g, "''");
      const rating = t.rating || 5;
      const comentario = (t.comentario || t.texto || '').replace(/'/g, "''");
      const foto = (t.foto || '').replace(/'/g, "''");
      const fecha = t.fecha || '2026-08-01';
      const origen = t.origen || 'manual';
      const estado = t.estado || (t.activo === false ? 'oculto' : 'publicado');
      const now = new Date().toISOString();

      sql += `INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('${id}', '${nombre}', '${pais}', '${tourNombre}', ${rating}, '${comentario}', '${foto}', '${fecha}', '${origen}', '${estado}', '${now}');\n`;
    });
  }

  // 4. Site Content (home, about, contact, global)
  const contentKeys = ['home', 'about', 'contact', 'global'];
  contentKeys.forEach(key => {
    const fPath = path.join(__dirname, `../www.manujungleforever.com/data/${key}.json`);
    if (fs.existsSync(fPath)) {
      const raw = fs.readFileSync(fPath, 'utf8');
      const escaped = raw.replace(/'/g, "''");
      const now = new Date().toISOString();
      sql += `INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES ('${key}', '${escaped}', '${now}');\n`;
    }
  });

  return sql;
}

if (require.main === module) {
  const sql = generateMigrationSql();
  const outPath = path.join(__dirname, '../drizzle/seed.sql');
  const dir = path.dirname(outPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(outPath, sql, 'utf8');
  console.log(`Generated migration SQL at: ${outPath}`);
}
