// Electron navigation / IPC / credential helpers (FE-01, FE-07). Pure functions
// so they can be tested without an Electron runtime.
"use strict";

/** Only https: may be handed to the OS (no file:, smb:, custom handlers). */
function isSafeExternalUrl(url) {
  try {
    return new URL(url).protocol === "https:";
  } catch {
    return false;
  }
}

/** True when `url` is the dev server's origin or a file:// app page. */
function isAppUrl(url, devUrl) {
  try {
    const u = new URL(url);
    if (u.protocol === "file:") return true;
    return !!devUrl && u.origin === new URL(devUrl).origin;
  } catch {
    return false;
  }
}

/** IPC guard: the calling frame must be the app, not some navigated page. */
function isTrustedSender(event, devUrl) {
  const url = event && event.senderFrame && event.senderFrame.url;
  return typeof url === "string" && isAppUrl(url, devUrl);
}

/**
 * Header injector for the API origin. The admin/desktop key lives only in the
 * main process (env TRADEBOT_DESKTOP_API_KEY) and is attached to requests (and
 * the WebSocket upgrade) bound for the API, so the renderer never holds it.
 */
function apiKeyHeaderHook(apiOrigin, key) {
  return (details, callback) => {
    const headers = { ...details.requestHeaders };
    if (key && details.url.startsWith(apiOrigin)) headers["x-api-key"] = key;
    callback({ requestHeaders: headers });
  };
}

module.exports = { isSafeExternalUrl, isAppUrl, isTrustedSender, apiKeyHeaderHook };
