// GOV-070 self-test fixture: one test that fails on purpose. Only
// vitest.selftest.config.js includes it; `npm test` never runs it.
import { expect, test } from 'vitest';

test('a failing expectation is reported at its line', () => {
  expect(5).toBe(4);
});

test('a passing test prints nothing', () => {
  expect(1).toBe(1);
});
