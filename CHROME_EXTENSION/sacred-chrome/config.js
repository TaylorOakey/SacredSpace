// SacredSpace OS — Shared config
// Edit SPINE_URL in Options page (chrome-extension options) to override.

const SACRED_DEFAULTS = {
  SPINE_URL: "http://localhost:8888",
  TAILSCALE_URL: "https://sacredspace-wsl.sacredspace.ts.net:8888",
  GEMINI_URL: "https://gemini.google.com",
  CLAUDE_URL: "https://claude.ai",
  CHATGPT_URL: "https://chatgpt.com",
  OBSIDIAN_PROTOCOL: "obsidian://open?vault=SacredSpace_Vault",
};

const PILLARS = [
  { id: "01", name: "Obsidian Vaults",     icon: "📖", color: "#7c6f9f", url: "obsidian://open?vault=SacredSpace_Vault" },
  { id: "02", name: "Council Grove",       icon: "⚖️",  color: "#5c8a6f", url: null, action: "council" },
  { id: "03", name: "Neural Forest",       icon: "🌲", color: "#3d7a5e", url: null, action: "spine?route=/pillars" },
  { id: "04", name: "Sacred Codex",        icon: "📜", color: "#8a6f3d", url: null, action: "spine?route=/pillars" },
  { id: "05", name: "Memory Engine",       icon: "🧠", color: "#6f3d8a", url: null, action: "spine?route=/memory" },
  { id: "06", name: "Agent Layer",         icon: "🤖", color: "#3d5c8a", url: null, action: "spine?route=/icaris" },
  { id: "07", name: "Social Mothership",   icon: "📡", color: "#8a3d5c", url: null, action: "spine?route=/pillars" },
  { id: "08", name: "Learning Path",       icon: "🎓", color: "#5c8a3d", url: null, action: "spine?route=/kethras-learning-gate" },
  { id: "09", name: "Sacred Market",       icon: "🏛️",  color: "#8a7a3d", url: null, action: "spine?route=/merchant-sacred-artifacts" },
];

async function getSpineUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get({ spineUrl: SACRED_DEFAULTS.SPINE_URL }, (items) => {
      resolve(items.spineUrl);
    });
  });
}

async function spineGet(route) {
  const base = await getSpineUrl();
  try {
    const res = await fetch(`${base}${route}`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return { ok: true, data: await res.json() };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

async function spinePost(route, body) {
  const base = await getSpineUrl();
  try {
    const res = await fetch(`${base}${route}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return { ok: true, data: await res.json() };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
