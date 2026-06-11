// SacredSpace OS — Service Worker (MV3)
// Uses chrome.storage.sync for settings (persists across Chrome sign-in)

const DEFAULT_SPINE    = 'http://localhost:8888';
const TAILSCALE_SPINE  = 'https://sacredspace-wsl.sacredspace.ts.net:8888';

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.get(['spineUrl'], (result) => {
    if (!result.spineUrl) {
      chrome.storage.sync.set({ spineUrl: DEFAULT_SPINE });
    }
  });
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === 'CHECK_SPINE') {
    checkSpine(msg.url || DEFAULT_SPINE).then(sendResponse);
    return true;
  }
});

async function checkSpine(baseUrl) {
  for (const url of [baseUrl, TAILSCALE_SPINE]) {
    try {
      const res = await fetch(`${url}/health`, { signal: AbortSignal.timeout(3000) });
      if (res.ok) return { ok: true, status: 'alive', url };
    } catch {}
  }
  return { ok: false, status: 'offline' };
}
