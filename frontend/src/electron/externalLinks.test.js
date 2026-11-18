import { describe, expect, it } from 'vitest';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { isSafeExternalUrl, isAppNavigation } = require('../../electron/externalLinks.cjs');

describe('isSafeExternalUrl', () => {
  it.each([
    'https://example.com/docs',
    'http://example.com',
  ])('allows %s', url => {
    expect(isSafeExternalUrl(url)).toBe(true);
  });

  it.each([
    'file:///etc/passwd',
    'smb://x',
    'javascript:alert(1)',
    'custom-scheme://x',
    'not a url',
    '',
    undefined,
  ])('rejects %s', url => {
    expect(isSafeExternalUrl(url)).toBe(false);
  });
});

describe('isAppNavigation', () => {
  const devUrl = 'http://127.0.0.1:5173';
  const indexFilePath = path.resolve('/opt/app/dist/index.html');

  it('allows same-origin dev-server navigation only', () => {
    expect(isAppNavigation('http://127.0.0.1:5173/settings', { devUrl })).toBe(true);
    expect(isAppNavigation('http://127.0.0.1:5174/', { devUrl })).toBe(false);
    expect(isAppNavigation('https://evil.example/', { devUrl })).toBe(false);
  });

  it('allows only the packaged index file in production', () => {
    const indexUrl = pathToFileURL(indexFilePath).href;
    expect(isAppNavigation(`${indexUrl}#/positions`, { indexFilePath })).toBe(true);
    expect(isAppNavigation('file:///etc/passwd', { indexFilePath })).toBe(false);
    expect(isAppNavigation('https://example.com/', { indexFilePath })).toBe(false);
  });
});
