#!/usr/bin/env node
/**
 * Generate sitemap.xml for the application
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BASE_URL = 'https://agentic-workflows-pm7o.onrender.com';

const routes = [
  { path: '/', priority: '1.0', changefreq: 'daily' },
  { path: '/login', priority: '0.8', changefreq: 'monthly' },
  { path: '/register', priority: '0.8', changefreq: 'monthly' },
  { path: '/workflows', priority: '0.9', changefreq: 'weekly' },
  { path: '/plugins', priority: '0.7', changefreq: 'weekly' },
  { path: '/api/docs', priority: '0.6', changefreq: 'monthly' },
];

const generateSitemap = () => {
  const lastmod = new Date().toISOString().split('T')[0];
  
  const urls = routes.map(route => `
  <url>
    <loc>${BASE_URL}${route.path}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${route.changefreq}</changefreq>
    <priority>${route.priority}</priority>
  </url>`).join('');

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;

  const distPath = path.join(__dirname, '../dist');
  if (!fs.existsSync(distPath)) {
    fs.mkdirSync(distPath, { recursive: true });
  }

  fs.writeFileSync(path.join(distPath, 'sitemap.xml'), sitemap);
  console.log('✅ Sitemap generated successfully at dist/sitemap.xml');
};

generateSitemap();
