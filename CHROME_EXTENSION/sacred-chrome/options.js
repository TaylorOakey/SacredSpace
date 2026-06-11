// SacredSpace OS — Options Logic (uses config.js)

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.sync.get({ spineUrl: SACRED_DEFAULTS.SPINE_URL, geminiKey: '' }, (items) => {
    document.getElementById('spine-url').value = items.spineUrl;
    document.getElementById('gemini-key').value = items.geminiKey || '';
  });

  document.getElementById('save-btn').addEventListener('click', save);
  document.getElementById('reset-btn').addEventListener('click', reset);
});

function save() {
  const spineUrl  = document.getElementById('spine-url').value.trim().replace(/\/$/, '')
                    || SACRED_DEFAULTS.SPINE_URL;
  const geminiKey = document.getElementById('gemini-key').value.trim();

  chrome.storage.sync.set({ spineUrl, geminiKey }, () => {
    flash('∆ Saved.');
  });
}

function reset() {
  chrome.storage.sync.set({ spineUrl: SACRED_DEFAULTS.SPINE_URL, geminiKey: '' }, () => {
    document.getElementById('spine-url').value = SACRED_DEFAULTS.SPINE_URL;
    document.getElementById('gemini-key').value = '';
    flash('∆ Reset to defaults.');
  });
}

function flash(msg) {
  const el = document.getElementById('status');
  el.textContent = msg;
  setTimeout(() => { el.textContent = ''; }, 2500);
}
