import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { Bindings } from '../db';

import { authRoutes } from './routes/auth';
import { salidasRoutes } from './routes/salidas';
import { reclamosRoutes } from './routes/reclamos';
import { mediaRoutes } from './routes/media';
import { testimonialsRoutes } from './routes/testimonials';

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
app.route('/salidas', salidasRoutes);
app.route('/reclamos', reclamosRoutes);
app.route('/media', mediaRoutes);
app.route('/testimonios', testimonialsRoutes);
app.route('/testimonials', testimonialsRoutes);

// Healthcheck
app.get('/health', (c) => c.json({ status: 'ok', engine: 'Hono + Drizzle + Cloudflare D1', timestamp: new Date().toISOString() }));

export default app;
