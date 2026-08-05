---
title: Google Drive organizer script
domain: 04_SACRED_CODEX
source: chatgpt: 2025-11-21_Google_Drive_organizer_script.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Google Drive organizer script
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-11-21_Google_Drive_organizer_script.md

# Google Drive organizer script
> **Source:** ChatGPT  |  **Date:** 2025-11-21  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

## Transcript

### ∆ **USER** — 2025-11-21 00:50

How's that script for organizing Google drive

---

### ⚙ **ASSISTANT** — 2025-11-21 00:50

Your Google Drive-organizer script is ready to drop into Google Apps Script and run. It’s built to scan your Drive, detect your **Sacred Space categories**, auto-create folders if they don’t exist, and then **sort files based on keywords**. It doesn’t delete anything. It moves with gentle monk-hands.

Before I paste the code, here’s the vibe: imagine a librarian in a cosmic hoodie quietly rearranging your universe.

---

## ⭐ Your Google Drive Auto-Organizer Script

This script:

• Creates a top-level folder called **SACREDSPACE_MASTER**  
• Creates category folders inside it  
• Scans files in your Drive (or a chosen folder ID)  
• Sorts them according to categories based on keywords you can edit  
• Leaves a log so you can see what it moved

You can literally copy/paste this into Google Apps Script:

---

### **📜 Google Apps Script: Sacred Space Drive Organizer**

```javascript
/**
 * SACRED SPACE: GOOGLE DRIVE ORGANIZER
 * Moves files into categorized folders based on keywords.
 * Safe: Does NOT delete anything.
 */

function organizeSacredSpace() {

  // ===== MASTER FOLDER =====
  const masterFolderName = "SACREDSPACE_MASTER";
  const masterFolder = getOrCreateFolder(masterFolderName);

  // ===== CATEGORY DEFINITIONS =====
  const categories = {
    "01_GRAPHIC_NOVEL": ["jenga", "novel", "graphic", "comic", "chapter", "sacred space story"],
    "02_BOARD_GAME": ["game", "board", "rulebook", "tarot", "silent echo", "cards"],
    "03_PLANT_NURSERY": ["plant", "nursery", "garden", "arboretum", "botany"],
    "04_NONPROFIT & GRANTS": ["grant", "nonprofit", "501", "funding", "proposal"],
    "05_DIGITAL_SANCTUARY": ["obsidian", "vault", "script", "ai studio", "json", "code"],
    "06_FAMILY": ["iris", "asher", "mimi", "school", "northeast"],
    "07_ARTWORK": ["drawing", "art", "sketch", "design", "mockup"],
    "08_AUDIO_VIDEO": ["audio", "video", "mp3", "wav", "footage", "screen recording"],
    "09_PERSONAL_WRITING": ["journal", "poem", "notes", "psycho cybernetics"],
    "10_MISC": [] // catches anything that doesn't fit
  };

  // ===== ORGANIZE FILES =====
  const root = DriveApp.getRootFolder();
  const files = root.getFiles();
  const log = [];

  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName().toLowerCase();

    let moved = false;

    for (const [folderName, keywords] of Object.entries(categories)) {
      if (keywords.some(kw => name.includes(kw))) {
        moveFile(file, masterFolder, folderName, log);
        moved = true;
        break;
      }
    }

    if (!moved) {
      moveFile(file, masterFolder, "10_MISC", log);
    }
  }

  // ===== OUTPUT LOG =====
  Logger.log("SACREDSPACE ORGANIZER LOG:");
  log.forEach(line => Logger.log(line));
}

function moveFile(file, masterFolder, category, log) {
  const categoryFolder = getOrCreateFolder(category, masterFolder);
  categoryFolder.addFile(file);
  file.getParents().next().removeFile(file);

  log.push(`Moved: ${file.getName()} → ${category}`);
}

function getOrCreateFolder(name, parent = DriveApp) {
  const folderIterator = parent.getFoldersByName(name);
  return folderIterator.hasNext()
    ? folderIterator.next()
    : parent.createFolder(name);
}
```

---

## 🌀 How to Use It (Phone-Friendly Instructions)

You can absolutely do this **on your Moto G Stylus**:

1. Open your browser → go to  
   **https://script.google.com/**

2. Tap **New Project**

3. Delete the default code  
   Paste **all of the code above**

4. Hit the floppy-disk icon → name the project  
   “SacredDrive_Organizer”

5. Tap **Run → organizeSacredSpace()**

6. Google will ask for permissions  
   Accept → Continue

Let it run for a minute.  
Your Drive will quietly re-arrange itself into clean, cosmic order.

---

## 🌳 Want to customize the categories?

Tell me:

• Any new categories you want  
• Keywords you want added  
• Whether you want it to organize **only SacredSpace files** or your whole Drive  
• Whether you want automated weekly cleanup  

I can modify the script to match the exact shape of your creative universe.

---

### ∆ **USER** — 2025-11-21 03:54

Is there any other way around using Google scripts.

---

### ⚙ **ASSISTANT** — 2025-11-21 03:54

There *is* another way, and it doesn’t require wrestling with Google Apps Script’s quirky little gremlins. Think of these alternatives like different trails up the same mountain—each with its own terrain, but all leading toward a cleaner, calmer Drive.

I’ll lay them out in plain language so you can sense which path feels lightest.

---

## **1. Use Google Drive’s built-in “Search Chips” + Bulk Actions**  
Kind of like sweeping the whole house with a giant magnet.

Drive’s search bar is
