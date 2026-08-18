import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const blogRoutes = new Hono<{ Bindings: Bindings }>();

// ── GET ALL BLOG POSTS ──
blogRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const isPublic = c.req.query('public') === 'true';

  let list = await db.select().from(schema.blogPosts).orderBy(desc(schema.blogPosts.fecha)).all();
  if (isPublic) {
    list = list.filter(p => p.estado === 'publicado');
  }

  return c.json({ posts: list });
});

// ── GET POST BY SLUG ──
blogRoutes.get('/:slug', async (c) => {
  const db = getDb(c.env.DB);
  const slug = c.req.param('slug');
  const post = await db.select().from(schema.blogPosts).where(eq(schema.blogPosts.slug, slug)).get();

  if (!post) return c.json({ error: 'Post no encontrado' }, 404);
  return c.json({ post });
});

// ── CREATE OR UPDATE POST ──
blogRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  const id = body.id || 'post_' + Date.now();
  await db.insert(schema.blogPosts).values({
    id,
    slug: body.slug,
    titulo: body.titulo,
    autor: body.autor || 'Manu Jungle Forever',
    fecha: body.fecha || new Date().toISOString().split('T')[0],
    categoria: body.categoria || 'Naturaleza',
    extracto: body.extracto || null,
    contenido: body.contenido || '',
    imagenHero: body.imagen_hero || null,
    estado: body.estado || 'publicado',
    createdAt: new Date().toISOString()
  }).onConflictDoUpdate({
    target: schema.blogPosts.id,
    set: {
      slug: body.slug,
      titulo: body.titulo,
      autor: body.autor,
      fecha: body.fecha,
      categoria: body.categoria,
      extracto: body.extracto,
      contenido: body.contenido,
      imagenHero: body.imagen_hero,
      estado: body.estado,
      updatedAt: new Date().toISOString()
    }
  });

  return c.json({ ok: true, id }, 201);
});

// ── DELETE POST ──
blogRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.blogPosts).where(eq(schema.blogPosts.id, id));
  return c.json({ ok: true });
});
