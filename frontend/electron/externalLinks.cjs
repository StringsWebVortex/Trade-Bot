"use strict";

const { pathToFileURL } = require("url");

// Pure helpers for deciding which URLs may leave the app window.
// Kept free of Electron imports so they can be unit-tested directly.

const SAFE_EXTERNAL_PROTOCOLS = new Set(["https:", "http:"]);

/**
 * True only for well-formed http(s) URLs. Anything else (file:, smb:,
 * javascript:, custom protocol handlers, malformed input) must never be
 * handed to shell.openExternal, which would dispatch it to the OS.
 * @param {unknown} url
 * @returns {boolean}
 */
function isSafeExternalUrl(url) {
  if (typeof url !== "string" || url.length === 0) return false;
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return false;
  }
  return SAFE_EXTERNAL_PROTOCOLS.has(parsed.protocol) && parsed.hostname.length > 0;
}

/**
 * True when `url` is the app's own content: same origin as the dev server
 * in development, or the exact packaged index.html file in production.
 * @param {unknown} url
 * @param {{ devUrl?: string, indexFilePath?: string }} app
 * @returns {boolean}
 */
function isAppNavigation(url, { devUrl, indexFilePath } = {}) {
  if (typeof url !== "string") return false;
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return false;
  }
  if (devUrl) {
    try {
      return parsed.origin === new URL(devUrl).origin;
    } catch {
      return false;
    }
  }
  if (indexFilePath) {
    if (parsed.protocol !== "file:") return false;
    return parsed.pathname === pathToFileURL(indexFilePath).pathname;
  }
  return false;
}

module.exports = { isSafeExternalUrl, isAppNavigation };
