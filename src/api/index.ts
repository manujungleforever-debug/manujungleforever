import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { Bindings } from '../db';

import { authRoutes } from './routes/auth';
import { toursRoutes } from './routes/tours';
import { salidasRoutes } from './routes/salidas';
import { blogRoutes } from './routes/blog';
import { testimonialsRoutes } from './routes/testimonials';
import { reclamosRoutes } from './routes/reclamos';
import { mediaRoutes } from './routes/media';
import { usersRoutes } from './routes/users';

export const app = new Hono<{ Bindings: Bindings }>().basePath('/api');

// Middlewares
app.use('*', logger());
app.use('*', cors({
  origin: '*',
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization', 'X-File-Name']
}));

// Mount Routes
app.route('/auth', authRoutes);
app.route('/users', usersRoutes);
app.route('/tours', toursRoutes);
app.route('/salidas', salidasRoutes);
app.route('/blog', blogRoutes);
app.route('/testimonios', testimonialsRoutes);
app.route('/reclamos', reclamosRoutes);
app.route('/media', mediaRoutes);

// Healthcheck
app.get('/health', (c) => c.json({ status: 'ok', engine: 'Hono + Drizzle + Cloudflare D1', timestamp: new Date().toISOString() }));

export default app;
