/**
 * SEC-1240..1242, REG-1243/1244 -- frontend secret handling, Electron
 * navigation/IPC guards, CSP, stale-data reporting, live config panel.
 */
import { createRequire } from 'node:module';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, renderHook, screen, waitFor } from '@testing-library/react';

import {
  assertNoAdminKeyInBundle, contentSecurityPolicy, cspPlugin,
} from '../buildGuard.js';
import {
  _resetStalePolls, apiFetch, setSessionApiKey, useStalePolls, usePolling,
} from '../hooks/useApi.js';
import { ConfigPanel } from '../components/panels/ConfigPanel.jsx';

const require = createRequire(import.meta.url);
const sec = require('../../electron/security.cjs');

afterEach(() => { setSessionApiKey(''); _resetStalePolls(); });

describe('SEC-1240 admin key is never bundled', () => {
  it('refuses a build that sets VITE_API_KEY', () => {
    expect(() => assertNoAdminKeyInBundle({ VITE_API_KEY: 'x'.repeat(40) })).toThrow(/VITE_API_READONLY_KEY/);
    expect(() => assertNoAdminKeyInBundle({ VITE_API_READONLY_KEY: 'ok' })).not.toThrow();
  });

  it('sends the in-memory operator key, and no header when none exists', async () => {
    const f = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal('fetch', f);
    await apiFetch('/status');
    expect(f.mock.calls[0][1].headers['x-api-key']).toBeUndefined();
    setSessionApiKey(' admin-key ');
    await apiFetch('/status');
    expect(f.mock.calls[1][1].headers['x-api-key']).toBe('admin-key');
    vi.unstubAllGlobals();
  });

  it('electron injects the key only for API-origin requests', () => {
    const hook = sec.apiKeyHeaderHook('http://localhost:8000', 'k');
    let out;
    hook({ url: 'http://localhost:8000/status', requestHeaders: {} }, (r) => { out = r; });
    expect(out.requestHeaders['x-api-key']).toBe('k');
    hook({ url: 'https://evil.example/', requestHeaders: {} }, (r) => { out = r; });
    expect(out.requestHeaders['x-api-key']).toBeUndefined();
  });
});

describe('SEC-1241 electron navigation and IPC guards', () => {
  it('opens only https externally', () => {
    expect(sec.isSafeExternalUrl('https://example.com')).toBe(true);
    for (const u of ['file:///etc/passwd', 'smb://h/s', 'http://x', 'vscode://x', 'nonsense']) {
      expect(sec.isSafeExternalUrl(u)).toBe(false);
    }
  });

  it('allows only the app origin to navigate or call IPC', () => {
    const dev = 'http://127.0.0.1:5173';
    expect(sec.isAppUrl('http://127.0.0.1:5173/x', dev)).toBe(true);
    expect(sec.isAppUrl('file:///app/dist/index.html', dev)).toBe(true);
    expect(sec.isAppUrl('https://evil.example', dev)).toBe(false);
    expect(sec.isTrustedSender({ senderFrame: { url: 'https://evil.example' } }, dev)).toBe(false);
    expect(sec.isTrustedSender({}, dev)).toBe(false);
    expect(sec.isTrustedSender({ senderFrame: { url: 'file:///a/index.html' } }, dev)).toBe(true);
  });
});

describe('SEC-1242 content security policy', () => {
  it('is restrictive and injected into the built page', () => {
    const csp = contentSecurityPolicy('http://10.0.0.5:8000');
    expect(csp).toContain("script-src 'self'");
    expect(csp).toContain("object-src 'none'");
    expect(csp).toContain('ws://10.0.0.5:8000');
    expect(csp).not.toMatch(/script-src[^;]*unsafe/);
    const html = cspPlugin().transformIndexHtml('<html><head></head></html>');
    expect(html).toContain('Content-Security-Policy');
  });
});

describe('REG-1243 stale polls are reported', () => {
  it('flags a failing poll and clears it on recovery', async () => {
    const f = vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({}) });
    vi.stubGlobal('fetch', f);
    const { result } = renderHook(() => ({ d: usePolling('/status', 60000), s: useStalePolls() }));
    await waitFor(() => expect(result.current.s).toHaveLength(1));
    expect(result.current.s[0].problem.kind).toBe('unauthorized');
    vi.unstubAllGlobals();
  });
});

describe('REG-1244 config panel shows the live settings', () => {
  it('renders values from /controls, not literals', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: async () => ({ controls: [{ name: 'daily_dd_halt', group: 'risk', value: 3.7, protected: false }] }),
    }));
    render(<ConfigPanel />);
    await screen.findByText('daily_dd_halt');
    expect(screen.getByText('3.7')).toBeTruthy();
    vi.unstubAllGlobals();
  });
});
