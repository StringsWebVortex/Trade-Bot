import { defineConfig } from 'vitest/config';

// GOV-070: ./scripts/problems selftest vitest runs only the fixture that
// fails on purpose, so the report it parses is a real vitest report.
export default defineConfig({
  test: {
    include: ['problems-fixture/**/*.selftest.js'],
    // GOV-070: problem lines only, with the failing line and column.
    reporters: ['./problems-reporter.js'],
    includeTaskLocation: true,
  },
});
