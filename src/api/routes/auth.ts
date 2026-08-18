import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';
import { eq } from 'drizzle-orm';
import { getDb, schema, Bindings } from '../../db';

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(4)
});

export const authRoutes = new Hono<{ Bindings: Bindings }>();

// Simple SHA-256 password hash helper
async function hashPassword(password: string): Promise<string> {
  const enc = new TextEncoder();
  const data = enc.encode(password + 'mjf_salt_2026');
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Generate simple HMAC-SHA256 Token
async function createToken(payload: { email: string; role: string; exp: number }, secret: string): Promise<string> {
  const enc = new TextEncoder();
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = btoa(JSON.stringify(payload));
  const data = enc.encode(`${header}.${body}`);
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', key, data);
  const sig = btoa(String.fromCharCode(...new Uint8Array(signature))).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `${header}.${body}.${sig}`;
}

authRoutes.post('/login', zValidator('json', loginSchema), async (c) => {
  const { email, password } = c.req.valid('json');
  const db = getDb(c.env.DB);
  const secret = c.env.JWT_SECRET || 'mjf_super_secret_jwt_2026';

  // 1. Check if user exists in D1
  const existingUser = await db.select().from(schema.users).where(eq(schema.users.email, email)).get();

  if (existingUser) {
    const computedHash = await hashPassword(password);
    if (existingUser.passwordHash !== computedHash) {
      return c.json({ error: 'Credenciales inválidas' }, 401);
    }

    const token = await createToken({
      email: existingUser.email,
      role: existingUser.role,
      exp: Math.floor(Date.now() / 1000) + (60 * 60 * 24 * 7) // 7 days
    }, secret);

    return c.json({
      token,
      user: {
        id: existingUser.id,
        email: existingUser.email,
        name: existingUser.name,
        role: existingUser.role
      }
    });
  }

  // 2. Fallback to env admin password (bootstrap admin)
  const envEmail = c.env.ADMIN_EMAIL || 'admin@manujungleforever.com';
  const envPassword = c.env.ADMIN_PASSWORD || 'ManuJungle2026!';

  if (email.toLowerCase() === envEmail.toLowerCase() && password === envPassword) {
    // Bootstrap user into D1
    const pHash = await hashPassword(password);
    const newId = 'usr_' + Date.now();
    await db.insert(schema.users).values({
      id: newId,
      email: envEmail,
      name: 'Super Admin',
      passwordHash: pHash,
      role: 'admin',
      createdAt: new Date().toISOString()
    }).onConflictDoNothing();

    const token = await createToken({
      email: envEmail,
      role: 'admin',
      exp: Math.floor(Date.now() / 1000) + (60 * 60 * 24 * 7)
    }, secret);

    return c.json({
      token,
      user: {
        id: newId,
        email: envEmail,
        name: 'Super Admin',
        role: 'admin'
      }
    });
  }

  return c.json({ error: 'Credenciales inválidas' }, 401);
});

authRoutes.get('/me', async (c) => {
  const authHeader = c.req.header('Authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return c.json({ error: 'No autorizado' }, 401);
  }
  return c.json({ ok: true });
});
