---
title: YouTube Watch Later URLs
domain: 08_LEARNING_PATH
source: chatgpt: 2025-11-22_YouTube_Watch_Later_URLs.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# YouTube Watch Later URLs
**Domain:** 08_LEARNING_PATH
**Source:** chatgpt: 2025-11-22_YouTube_Watch_Later_URLs.md

# YouTube Watch Later URLs
> **Source:** ChatGPT  |  **Date:** 2025-11-22  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `08_LEARNING`

---

## Transcript

### ∆ **USER** — 2025-11-22 22:56

I want a list of all the urls in my YouTube watch later list to plug into notebook lm

---

### ⚙ **ASSISTANT** — 2025-11-22 22:57

Short version: I can’t see your YouTube account directly, so I can’t pull the list for you—but I *can* give you a one-time “copy everything out of Watch Later” move that you can run yourself and then feed into NotebookLM.

Let’s do the “library computer / desktop browser” method first, because it’s the cleanest.

---

## Method 1 – On a computer (recommended)

**Goal:** Get a simple text list like:

```text
Video Title 1 - https://www.youtube.com/watch?v=xxxx
Video Title 2 - https://www.youtube.com/watch?v=yyyy
...
```

### Step 1: Open your Watch Later playlist

1. On a computer, open a browser (Chrome, Edge, Firefox, whatever).
2. Go to YouTube and sign in.
3. In the left sidebar, click **“Watch later”**.  
   Or directly visit: `https://www.youtube.com/playlist?list=WL`

### Step 2: Make sure *all* videos are loaded

YouTube only loads what’s on screen at first.

1. Scroll down…  
2. Keep scrolling slowly until you hit the bottom and **no new videos appear**.
   - You’re basically forcing YouTube to load the full playlist into the page.

### Step 3: Open the browser console

This is where we’ll run a tiny script to grab all the links.

- **Chrome / Edge (Windows/Linux):**
  - Press `Ctrl + Shift + J`
- **Chrome / Edge (Mac):**
  - Press `Cmd + Option + J`
- Or:
  - Right-click on the page → **Inspect** → click the **Console** tab

You should see a blank area where you can type JavaScript.

### Step 4: Run this script to grab titles + URLs

Copy everything in this box and paste it into the console, then press Enter:

```js
// Grab all video entries in the Watch Later playlist
const items = Array.from(
  document.querySelectorAll('ytd-playlist-video-renderer a#video-title')
);

// Build lines: "Title - URL"
const lines = items.map(a => {
  const title = a.textContent.trim().replace(/\s+/g, ' ');
  const href = a.getAttribute('href') || '';
  // Ensure we get a clean watch URL (drop &list, &index, etc.)
  const url = href.startsWith('http')
    ? href.split('&')[0]
    : 'https://www.youtube.com' + href.split('&')[0];
  return `${title} - ${url}`;
});

// Make a text file and download it
const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
const url = URL.createObjectURL(blob);
const downloadLink = Object.assign(document.createElement('a'), {
  href: url,
  download: 'youtube_watch_later_links.txt'
});
document.body.appendChild(downloadLink);
downloadLink.click();
document.body.removeChild(downloadLink);
URL.revokeObjectURL(url);

console.log(`Exported ${lines.length} videos from Watch Later.`);
```

What this does:

- Collects every video in your Watch Later playlist that’s currently loaded on the page.
- Extracts:
  - The **title**
  - A clean **https://www.youtube.com/watch?v=...** URL
- Downloads a file to your computer called  
  **`youtube_watch_later_links.txt`**

### Step 5: Plug into NotebookLM

Now you’ve got a nice portable file.

Options:

1. **Upload the .txt file to Google Drive**  
   - In NotebookLM, create a new notebook.
   - Add a source → choose Google Drive → pick `youtube_watch_later_links.txt`.
2. Or **copy-paste the contents** into a Google Doc and use that as your NotebookLM source.
3. Or paste straight into NotebookLM as a “note” / text source if that’s easier.

---

## Method 2 – On your phone (Android) only

Phone-only is more annoying, but roughly:

1. Open Chrome on your phone.
2. Go to `https://www.youtube.com/playlist?list=WL`.
3. In Chrome menu (⋮), tap **“Desktop site”** so you see the full desktop layout.
4. Scroll all the way to the bottom until all videos are loaded.
5. If your mobile browser lets you open **Developer Tools** (most don’t), you could run the same script in a console.  
   Realistically, this is painful on a phone.

Given your whole Sacred Workflow, using the **library computer** or any desktop is by far the least headache for this job. You just have to do it once, then NotebookLM can chew on that list forever.

---

## Once you’ve got the list…

You can do some fun things with it in NotebookLM:

- Cluster videos by topic (geometry, music, storytelling, consciousness, etc.).
- Ask it: “Group these links into SacredSpace ‘study paths’.”
- Build “learning quests”:
  - Path 1: Geometry & Symmetry
  - Path 2: Music, Frequency, and Color
  - Path 3: Myth, Archetype, and Storytelling

So this export isn’t just busywork; it turns your chaotic Watch Later pile into a curated Sacred Library you can actually *use*.

---
