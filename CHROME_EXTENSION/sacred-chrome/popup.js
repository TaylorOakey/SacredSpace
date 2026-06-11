// SacredSpace OS — Popup Logic
// Uses config.js for PILLARS, SACRED_DEFAULTS, spineGet, spinePost

let queryInFlight = false;

// ── Init ───────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  renderPillars();
  checkSpineStatus();
  bindEvents();
});

// ── Pillar Grid (from config.js PILLARS) ───────────────
function renderPillars() {
  const grid = document.getElementById('pillars-grid');
  grid.innerHTML = '';
  PILLARS.forEach((p) => {
    const card = document.createElement('div');
    card.className = 'pillar-card';
    card.dataset.key = p.id;
    card.innerHTML = `
      <span class="pillar-num">${p.id}</span>
      <span class="pillar-icon">${p.icon}</span>
      <span class="pillar-name">${p.name.replace(' ', '\n')}</span>
    `;
    card.addEventListener('click', () => onPillarClick(p, card));
    grid.appendChild(card);
  });
}

function onPillarClick(pillar, card) {
  document.querySelectorAll('.pillar-card').forEach(c => c.classList.remove('active'));
  card.classList.add('active');

  if (pillar.url) {
    chrome.tabs.create({ url: pillar.url });
    return;
  }

  if (pillar.action) {
    if (pillar.action.startsWith('spine?route=')) {
      const route = pillar.action.replace('spine?route=', '');
      terminalLog(`∆ Querying Pillar ${pillar.id} — ${pillar.name}`, 'system');
      spineGet(route).then(r => {
        if (r.ok) {
          const text = JSON.stringify(r.data).substring(0, 300);
          terminalLog(text, 'result');
        } else {
          terminalLog(`Spine error: ${r.error}`, 'error');
        }
      });
    } else if (pillar.action === 'council') {
      chrome.tabs.create({ url: chrome.runtime.getURL('pages/sidebar.html') });
    }
    return;
  }

  terminalLog(`Pillar ${pillar.id} — ${pillar.name} (no action configured)`, 'system');
  document.getElementById('terminal-input').value = `pillar ${pillar.id}`;
  document.getElementById('terminal-input').focus();
}

// ── Spine Status ───────────────────────────────────────
async function checkSpineStatus() {
  const dot   = document.getElementById('spine-status');
  const label = document.getElementById('spine-label');
  dot.className = 'status-dot checking';
  label.textContent = 'Spine: checking…';

  const r = await spineGet('/health').catch(() => ({ ok: false, error: 'unreachable' }));

  if (r.ok) {
    dot.className = 'status-dot online';
    label.textContent = 'Spine: online';
    terminalLog('∆ Spine connected', 'system');
  } else {
    // Try Tailscale URL
    const tsUrl = SACRED_DEFAULTS.TAILSCALE_URL;
    try {
      const tsRes = await fetch(`${tsUrl}/health`, { signal: AbortSignal.timeout(2000) });
      if (tsRes.ok) {
        dot.className = 'status-dot online';
        label.textContent = 'Spine: online (Tailscale)';
        terminalLog('∆ Spine via Tailscale mesh', 'system');
        chrome.storage.sync.set({ spineUrl: tsUrl });
        return;
      }
    } catch {}

    dot.className = 'status-dot offline';
    label.textContent = 'Spine: offline';
    terminalLog('⚠ Spine offline — run SACRED_LAUNCH.ps1', 'error');
  }
}

// ── Terminal ───────────────────────────────────────────
function terminalLog(text, type = 'result') {
  const out  = document.getElementById('terminal-output');
  const line = document.createElement('div');
  line.className = `terminal-line ${type}`;
  line.textContent = text;
  out.appendChild(line);
  out.scrollTop = out.scrollHeight;
}

async function runQuery() {
  if (queryInFlight) return;
  const input = document.getElementById('terminal-input');
  const query = input.value.trim();
  if (!query) return;

  terminalLog(`∆> ${query}`, 'query');
  input.value = '';

  const btn = document.getElementById('query-btn');
  btn.disabled = true;
  queryInFlight = true;
  terminalLog('Scrying…', 'system');

  const r = await spinePost('/memory', { query, top_k: 3 });

  queryInFlight = false;
  btn.disabled = false;

  if (!r.ok) {
    terminalLog(`Error: ${r.error || 'spine unreachable'}`, 'error');
    return;
  }

  const data = r.data;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    terminalLog('No results found in memory.', 'system');
    return;
  }

  if (Array.isArray(data)) {
    data.slice(0, 3).forEach((mote, i) => {
      const text = mote.text || mote.content || JSON.stringify(mote);
      terminalLog(`[${i + 1}] ${text.substring(0, 160)}`, 'result');
    });
  } else {
    terminalLog(JSON.stringify(data).substring(0, 300), 'result');
  }
}

async function runHermesQuery() {
  if (queryInFlight) return;
  const input = document.getElementById('terminal-input');
  const query = input.value.trim() || 'What does the SacredSpace OS reveal?';
  input.value = '';

  terminalLog(`[GR∆M∆]> ${query}`, 'query');
  queryInFlight = true;
  const btn = document.getElementById('query-btn');
  btn.disabled = true;
  terminalLog('Invoking GR∆M∆ Oracle…', 'system');

  const r = await spinePost('/hermes/', { query });

  queryInFlight = false;
  btn.disabled = false;

  if (!r.ok) {
    terminalLog(`Oracle error: ${r.error || 'spine unreachable'}`, 'error');
    return;
  }

  const text = r.data?.response || r.data?.answer || r.data?.output || JSON.stringify(r.data);
  terminalLog(text.substring(0, 400), 'hermes');
}

// ── Event Bindings ─────────────────────────────────────
function bindEvents() {
  document.getElementById('query-btn').addEventListener('click', runQuery);

  document.getElementById('terminal-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') runQuery();
  });

  document.getElementById('refresh-status').addEventListener('click', checkSpineStatus);

  document.getElementById('open-options').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  document.getElementById('gemini-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: SACRED_DEFAULTS.GEMINI_URL });
    window.close();
  });

  document.getElementById('hermes-btn').addEventListener('click', runHermesQuery);

  document.getElementById('vault-btn').addEventListener('click', () => {
    spineGet('/').then(r => {
      if (r.ok) {
        chrome.storage.sync.get({ spineUrl: SACRED_DEFAULTS.SPINE_URL }, (items) => {
          chrome.tabs.create({ url: `${items.spineUrl}/` });
        });
      } else {
        terminalLog('Vault: open Obsidian directly — spine is offline', 'error');
        chrome.tabs.create({ url: SACRED_DEFAULTS.OBSIDIAN_PROTOCOL });
      }
    });
  });
}
