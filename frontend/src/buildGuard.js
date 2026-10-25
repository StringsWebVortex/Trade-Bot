/**
 * FE-01: Vite inlines every VITE_* value into the built JS. The admin key
 * (API_SECRET_KEY) must never travel that way; only a read-only key may.
 * Throws when a build environment tries to bake the admin key in.
 */
export function assertNoAdminKeyInBundle(env) {
  if (env && env.VITE_API_KEY) {
    throw new Error(
      'VITE_API_KEY would be inlined into the JS bundle. Use VITE_API_READONLY_KEY '
      + '(API_READONLY_KEY) instead and enter the admin key in the dashboard at runtime.',
    );
  }
}

/**
 * FE-08: Content-Security-Policy injected into the built index.html (the dev
 * server needs inline scripts for hot reload, so it is build-only). Used by
 * both the browser build and the Electron file:// load. frame-ancestors is
 * ignored in a meta tag, so it is not listed.
 */
export function contentSecurityPolicy(apiOrigin = '') {
  const extra = apiOrigin ? ` ${apiOrigin} ${apiOrigin.replace(/^http/, 'ws')}` : '';
  return [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self' data:",
  `connect-src 'self' http://localhost:* http://127.0.0.1:* ws://localhost:* ws://127.0.0.1:*${extra}`,
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
].join('; ');
}

export const CONTENT_SECURITY_POLICY = contentSecurityPolicy();

export function cspMetaTag(apiOrigin = '') {
  return `<meta http-equiv="Content-Security-Policy" content="${contentSecurityPolicy(apiOrigin)}" />`;
}

/** Vite plugin: add the CSP meta to the built page only. */
export function cspPlugin(apiOrigin = '') {
  return {
    name: 'tradebot-csp',
    apply: 'build',
    transformIndexHtml(html) {
      return html.replace('<head>', `<head>\n    ${cspMetaTag(apiOrigin)}`);
    },
  };
}
