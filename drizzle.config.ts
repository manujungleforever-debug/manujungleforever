import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
  dialect: 'sqlite',
  driver: 'd1-http',
  dbCredentials: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID || '',
    databaseId: 'c0765748-5818-44ee-ab40-c43607a106d6',
    token: process.env.CLOUDFLARE_D1_TOKEN || ''
  }
});
