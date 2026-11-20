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

/** True only for the dev origin or the exact packaged dashboard document. */
function isAppUrl(url, devUrl, appFileUrl) {
  try {
    const candidate = new URL(url);
    if (candidate.protocol === "file:") {
      if (!appFileUrl) return false;
      const app = new URL(appFileUrl);
      if (app.protocol !== "file:") return false;
      // Hash navigation is still the same document; another local file is not.
      candidate.hash = "";
      app.hash = "";
      return candidate.href === app.href;
    }
    return !!devUrl && candidate.origin === new URL(devUrl).origin;
  } catch {
    return false;
  }
}

/** IPC guard: the calling frame must be the app, not some navigated page. */
function isTrustedSender(event, devUrl, appFileUrl) {
  const url = event && event.senderFrame && event.senderFrame.url;
  return typeof url === "string" && isAppUrl(url, devUrl, appFileUrl);
}

/**
 * Header injector for the API origin. The admin/desktop key lives only in the
 * main process (env TRADEBOT_DESKTOP_API_KEY) and is attached to requests (and
 * the WebSocket upgrade) bound for the API, so the renderer never holds it.
 */
function apiKeyHeaderHook(apiOrigin, key) {
  let expectedOrigin = null;
  try {
    expectedOrigin = new URL(apiOrigin).origin;
  } catch {
    // An invalid API origin must never receive the credential.
  }
  return (details, callback) => {
    const headers = { ...details.requestHeaders };
    let requestOrigin = null;
    try {
      requestOrigin = new URL(details.url).origin;
    } catch {
      // Non-URL requests are not API requests.
    }
    if (key && expectedOrigin && requestOrigin === expectedOrigin) headers["x-api-key"] = key;
    callback({ requestHeaders: headers });
  };
}

module.exports = { isSafeExternalUrl, isAppUrl, isTrustedSender, apiKeyHeaderHook };
