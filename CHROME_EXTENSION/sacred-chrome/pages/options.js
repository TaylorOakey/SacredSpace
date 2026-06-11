document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.sync.get({ spineUrl: SACRED_DEFAULTS.SPINE_URL }, (items) => {
    document.getElementById("spineUrl").value = items.spineUrl;
  });

  document.getElementById("saveBtn").addEventListener("click", () => {
    const spineUrl = document.getElementById("spineUrl").value.trim().replace(/\/$/, "");
    chrome.storage.sync.set({ spineUrl }, () => {
      const saved = document.getElementById("saved");
      saved.style.display = "inline";
      setTimeout(() => { saved.style.display = "none"; }, 2000);
    });
  });
});
