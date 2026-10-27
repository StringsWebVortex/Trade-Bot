import { defineConfig } from 'vite';

// GOV-070: ./scripts/problems selftest build builds only the fixture with a
// syntax error, so the build error it parses is a real vite error.
export default defineConfig({
  logLevel: 'error',
  build: {
    outDir: 'problems-fixture-dist',
    emptyOutDir: true,
    rollupOptions: { input: 'problems-fixture/broken.js' },
  },
});
