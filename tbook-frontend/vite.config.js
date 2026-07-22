import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const BACKEND_ORIGIN = process.env.VITE_DEV_BACKEND_ORIGIN || 'http://localhost';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': BACKEND_ORIGIN,
      '/admin': BACKEND_ORIGIN,
      '/media': BACKEND_ORIGIN,
      '/static': BACKEND_ORIGIN,
    },
  },
});
