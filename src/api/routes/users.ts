import { Hono } from 'hono';
import { eq, desc } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

export const usersRoutes = new Hono<{ Bindings: Bindings }>();

// Simple SHA-256 password hash helper
async function hashPassword(password: string): Promise<string> {
  const enc = new TextEncoder();
  const data = enc.encode(password + 'mjf_salt_2026');
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// ── GET ALL USERS ──
usersRoutes.get('/', async (c) => {
  const db = getDb(c.env.DB);
  const list = await db.select({
    id: schema.users.id,
    email: schema.users.email,
    name: schema.users.name,
    role: schema.users.role,
    createdAt: schema.users.createdAt,
    updatedAt: schema.users.updatedAt
  }).from(schema.users).orderBy(desc(schema.users.createdAt)).all();

  return c.json({ users: list });
});

// ── CREATE USER ──
usersRoutes.post('/', async (c) => {
  const db = getDb(c.env.DB);
  const body = await c.req.json();

  if (!body.email || !body.name) {
    return c.json({ error: 'Faltan campos obligatorios (email, name)' }, 400);
  }
  if (!body.password && !body.password_hash) {
    return c.json({ error: 'Se requiere password o password_hash' }, 400);
  }

  const existing = await db.select().from(schema.users).where(eq(schema.users.email, body.email)).get();
  if (existing) {
    return c.json({ error: 'El correo ya se encuentra registrado' }, 409);
  }

  const id = body.id || ('usr_' + Date.now());
  // Accept pre-hashed password from admin panel or hash plain text
  const pHash = body.password_hash && body.password_hash !== '(stored in D1)'
    ? body.password_hash
    : await hashPassword(body.password || '123456aytana');

  // Map panel role names to D1 enum values
  const role = body.role === 'superuser' ? 'admin'
    : body.role === 'normal' ? 'editor'
    : (body.role || 'editor') as 'admin' | 'editor' | 'guia';

  await db.insert(schema.users).values({
    id,
    email: body.email,
    name: body.name,
    passwordHash: pHash,
    role,
    createdAt: body.created_at || new Date().toISOString()
  });

  return c.json({
    ok: true,
    user: { id, email: body.email, name: body.name, role }
  }, 201);
});


// ── UPDATE USER (ROLE, NAME, PASSWORD) ──
usersRoutes.put('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');
  const body = await c.req.json();

  // Map panel role names to D1 enum values
  const role = body.role === 'superuser' ? 'admin'
    : body.role === 'normal' ? 'editor'
    : body.role as 'admin' | 'editor' | 'guia' | undefined;

  const updates: Partial<typeof schema.users.$inferInsert> = {
    name: body.name,
    role,
    updatedAt: new Date().toISOString()
  };

  if (body.password && body.password.trim().length >= 4) {
    updates.passwordHash = await hashPassword(body.password.trim());
  } else if (body.password_hash && body.password_hash !== '(stored in D1)') {
    updates.passwordHash = body.password_hash;
  }

  await db.update(schema.users).set(updates).where(eq(schema.users.id, id));
  return c.json({ ok: true });
});


// ── DELETE USER ──
usersRoutes.delete('/:id', async (c) => {
  const db = getDb(c.env.DB);
  const id = c.req.param('id');

  await db.delete(schema.users).where(eq(schema.users.id, id));
  return c.json({ ok: true });
});
