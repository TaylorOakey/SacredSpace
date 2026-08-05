---
title: Link Obsidian to Google Drive
domain: 01_OBSIDIAN_VAULTS
source: gemini: 2025-11-17_288_link-obsidian-to-google-drive.md
tags: ${item.tags}\n`;,full-body
type: knowledge_artifact
---

# Link Obsidian to Google Drive
**Domain:** 01_OBSIDIAN_VAULTS
**Source:** gemini: 2025-11-17_288_link-obsidian-to-google-drive.md

# Link Obsidian to Google Drive

> **Catalog #288** | Extracted 2026-06-16 04:03 UTC
> Created: 2025-11-17 10:30 UTC
> Updated: 2025-11-18 23:13 UTC

**211 messages**

---

### Message 3 — 👤 User

---

### Message 5 — 👤 User

Before I move any farther I would like to get the automation linked to obsidian and Google drive Google docs and my email linked can you give me the code to do so or suggest the best path we talked about this before but now with the new understanding we have and new data can we go ahead and lock this in

---

### Message 8 — 🤖 Assistant

---

### Message 9 — 🤖 Assistant

---

### Message 10 — 🤖 Assistant

---

### Message 11 — 🤖 Assistant

Nice, this is exactly the moment to “lock in the plumbing” before you build more temples on top of it. Let’s wire Obsidian ⇄ Google Drive/Docs ⇄ Gmail in a way you can actually use.

I’ll give you:

1. The *best architecture* (low cost, realistic for you right now).  
2. A **ready-to-paste Google Apps Script** that links Drive + your Obsidian vault + Gmail.  
3. Quick setup steps so you’re not left staring at a blank code editor.

---

## 1. Big picture: how everything connects

Here’s the cleanest path with the tools you already use:

### Step A – Make Obsidian “live” inside Google Drive

You want your Obsidian vault to sit in a folder that Google Drive can see.

**If you haven’t already:**

1. Install **Google Drive for Desktop** on your computer (the one that runs Obsidian).
2. In Drive for Desktop, you’ll get a “My Drive” folder on your machine.
3. Create a folder there called something like:

   `SacredSpace_Obsidian_Vault`

4. Move or create your Obsidian vault *inside* that folder.
   - In Obsidian: `Open folder as vault` → select `SacredSpace_Obsidian_Vault`.

Now:

- Every `.md` note you create in Obsidian is also a file in Google Drive.
- That means Google Apps Script can see your vault as a Drive folder.

That’s the bridge.

---

### Step B – Use Google Apps Script as your “automation brain”

Google Apps Script can:

- Read Obsidian notes (markdown files in Drive).
- Organize / index them in a **Google Sheet** or a **Google Doc**.
- Email you a **daily or weekly digest** through Gmail.
- Later: be used as a backend endpoint for Google AI Studio / Gemini.

We’ll set up one central script that does:

- Scan your Obsidian vault folder in Drive  
- Build/update an index (sheet) of notes  
- Email you a summary

From there, we can add extra flows (archive old docs, auto-label stuff, etc.).

---

## 2. The core automation script (Drive + Obsidian + Gmail)

### Step 1 – Create the script project

1. Go to **script.google.com** (or in Google Drive → “New” → “More” → “Apps Script”).
2. Create a new project, name it:

   `SacredSpace_Automation_Core`

3. Delete any placeholder code in `Code.gs` and paste **all** of the code below.

---

### Step 2 – Paste this code (you only edit the CONFIG section)

```javascript
/***********************
 * SACREDSPACE AUTOMATION CORE
 * Links: Obsidian (via Drive) + Google Drive/Docs + Gmail
 ***********************/

/**
 * ========= CONFIG =========
 * Set these values for YOUR setup.
 */
const CONFIG = {
  // 1. Folder ID of your Obsidian vault on Google Drive
  //    Get this by opening the folder in Drive and copying the ID from the URL.
  OBSIDIAN_FOLDER_ID: 'PUT_OBSIDIAN_FOLDER_ID_HERE',

  // 2. Folder where you want automation artifacts (index sheet, logs, etc.)
  ROOT_AUTOMATION_FOLDER_ID: 'PUT_AUTOMATION_FOLDER_ID_HERE',

  // 3. Your email (for digests & notifications)
  SUMMARY_EMAIL: 'your_email_here@gmail.com',

  // 4. Name of the index sheet file that will be created/updated
  INDEX_SHEET_NAME: 'SacredSpace_Obsidian_Index'
};


/**
 * Entry point: run this to sync Obsidian → Sheet + send a summary email.
 * You can hook this to a time-driven trigger (e.g., daily at 8am).
 */
function runSacredSpaceSync() {
  const files = getObsidianMarkdownFiles_();
  const indexInfo = buildIndexFromFiles_(files);
  const sheet = getOrCreateIndexSheet_();
  writeIndexToSheet_(sheet, indexInfo);
  sendDigestEmail_(indexInfo);
}


/**
 * Get all .md files in the Obsidian vault folder (non-recursive OR recursive).
 * This version is recursive and walks subfolders.
 */
function getObsidianMarkdownFiles_() {
  const rootFolder = DriveApp.getFolderById(CONFIG.OBSIDIAN_FOLDER_ID);
  const files = [];
  walkFolder_(rootFolder, files);
  return files;
}

function walkFolder_(folder, filesArray) {
  // Add .md files in this folder
  const files = folder.getFiles();
  while (files.hasNext()) {
    const f = files.next();
    if (f.getName().toLowerCase().endsWith('.md')) {
      filesArray.push(f);
    }
  }

  // Recurse into subfolders
  const subfolders = folder.getFolders();
  while (subfolders.hasNext()) {
    const sub = subfolders.next();
    walkFolder_(sub, filesArray);
  }
}


/**
 * Build a simple index: title, fileName, path (parent folder), tags (from frontmatter), last updated.
 */
function buildIndexFromFiles
