import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://genaipick.com',
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
  integrations: [sitemap({
    lastmod: new Date(),
    changefreq: 'weekly',
    priority: 0.7,
  })],
});
