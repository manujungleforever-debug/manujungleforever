// ── High-Performance D1 Data Engine for /data/*.json ──
// Serves all legacy and current /data/*.json requests directly from Cloudflare D1 (SQLite)
// with seamless fallback to GitHub raw data if D1 table is empty.

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const filePath = params.path ? params.path.join('/') : '';
  const url = new URL(request.url);
  const isPublic = url.searchParams.get('public') !== 'false';

  const jsonHeaders = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Access-Control-Allow-Origin': '*'
  };

  try {
    if (env.DB) {
      // 1. Tours Catalog
      if (filePath === 'tours.json') {
        const query = isPublic ? "SELECT * FROM tours WHERE estado = 'activo'" : "SELECT * FROM tours";
        const { results } = await env.DB.prepare(query).all();
        if (results && results.length > 0) {
          const formatted = results.map(t => ({
            id: t.id,
            slug: t.slug,
            nombre: t.nombre,
            categoria: t.categoria,
            estado: t.estado,
            duracion_dias: t.duracion_dias,
            duracion_noches: t.duracion_noches,
            precio_desde: t.precio_desde,
            moneda: t.moneda,
            capacidad_min: t.capacidad_min,
            capacidad_max: t.capacidad_max,
            dificultad: t.dificultad,
            temporada: t.temporada,
            descripcion_corta: t.descripcion_corta,
            descripcion_larga: t.descripcion_larga,
            imagen_hero: t.imagen_hero,
            imagen_alt: t.imagen_alt,
            galeria: t.galeria_json ? JSON.parse(t.galeria_json) : [],
            itinerario: t.itinerario_json ? JSON.parse(t.itinerario_json) : [],
            transporte: t.transporte_json ? JSON.parse(t.transporte_json) : []
          }));
          return new Response(JSON.stringify({ tours: formatted }, null, 2), { status: 200, headers: jsonHeaders });
        }
      }

      // 2. Blog Posts Index
      if (filePath === 'posts-index.json') {
        const query = isPublic ? "SELECT * FROM blog_posts WHERE estado = 'publicado' ORDER BY fecha DESC" : "SELECT * FROM blog_posts ORDER BY fecha DESC";
        const { results } = await env.DB.prepare(query).all();
        if (results && results.length > 0) {
          const posts = results.map(p => ({
            id: p.id,
            slug: p.slug,
            title: p.titulo,
            titulo: p.titulo,
            author: p.autor,
            autor: p.autor,
            date: p.fecha,
            fecha: p.fecha,
            category: p.categoria,
            categoria: p.categoria,
            excerpt: p.extracto,
            extracto: p.extracto,
            content: p.contenido,
            contenido: p.contenido,
            image: p.imagen_hero,
            imagen: p.imagen_hero,
            publicado: p.estado === 'publicado',
            estado: p.estado,
            url: `${p.slug}/index.html`
          }));
          return new Response(JSON.stringify({ posts }, null, 2), { status: 200, headers: jsonHeaders });
        }
      }

      // 3. Testimonials
      if (filePath === 'testimonials.json') {
        const query = isPublic ? "SELECT * FROM testimonials WHERE estado = 'publicado' ORDER BY fecha DESC" : "SELECT * FROM testimonials ORDER BY fecha DESC";
        const { results } = await env.DB.prepare(query).all();
        if (results && results.length > 0) {
          const list = results.map(t => ({
            id: t.id,
            nombre: t.nombre,
            pais: t.pais,
            tour: t.tour_nombre,
            tour_nombre: t.tour_nombre,
            rating: t.rating,
            texto: t.comentario,
            comentario: t.comentario,
            foto: t.foto,
            fecha: t.fecha,
            origen: t.origen || 'manual',
            activo: t.estado === 'publicado',
            estado: t.estado
          }));
          return new Response(JSON.stringify({ testimonials: list, testimonios: list }, null, 2), { status: 200, headers: jsonHeaders });
        }
      }

      // 4. Departures
      if (filePath === 'departures.json') {
        const { results } = await env.DB.prepare("SELECT * FROM departures ORDER BY fecha_salida ASC").all();
        if (results && results.length > 0) {
          return new Response(JSON.stringify({ salidas: results }, null, 2), { status: 200, headers: jsonHeaders });
        }
      }

      // 5. Site Content (about, home, contact, global)
      const contentKeys = ['about', 'home', 'contact', 'global'];
      const matchedKey = contentKeys.find(k => filePath === `${k}.json`);
      if (matchedKey) {
        const row = await env.DB.prepare("SELECT value FROM site_content WHERE key = ?").bind(matchedKey).first();
        if (row && row.value) {
          return new Response(row.value, { status: 200, headers: jsonHeaders });
        }
      }
    }
  } catch (err) {
    console.error(`Error in D1 data proxy for ${filePath}:`, err);
  }

  // 6. Fallback to raw GitHub or Static Assets
  const REPO = 'manujungleforever-debug/manujungleforever';
  const BRANCH = 'main';
  try {
    const rawUrl = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/www.manujungleforever.com/data/${filePath}?v=${Date.now()}`;
    const rawRes = await fetch(rawUrl, { headers: { 'User-Agent': 'MJF-CMS/1.0', 'Cache-Control': 'no-cache' } });
    if (rawRes.ok) {
      const content = await rawRes.text();
      return new Response(content, { status: 200, headers: jsonHeaders });
    }
  } catch (e) {}

  if (env.ASSETS) {
    return env.ASSETS.fetch(request);
  }
  return new Response('Not found', { status: 404 });
}
