# ∆ SACRED SIGIL TERMINAL v2.0 ∆
## QUICK START: Build & Deploy in 30 Minutes

**Current Status:** React component ready, styling complete, PWA manifest provided  
**Next Step:** Run locally, test on phone, deploy  
**Time Estimate:** 30 mins setup + testing  

---

## STEP 1: CREATE REACT PROJECT (5 mins)

### Option A: Create New Vite Project
```bash
npm create vite@latest sacred-sigil-terminal -- --template react
cd sacred-sigil-terminal
npm install
```

### Option B: Add to Existing SacredSpace Project
If you have a React app running already, just add the component folder.

---

## STEP 2: ADD THE COMPONENT FILES (2 mins)

Copy these files to your project:

```
src/
├── components/
│   ├── SacredSigilTerminal.jsx     (copy from outputs)
│   └── SacredSigilTerminal.css     (copy from outputs)
├── App.jsx                          (see below for import)
└── main.jsx
```

---

## STEP 3: IMPORT & USE IN APP (3 mins)

### In your `src/App.jsx`:

```jsx
import React, { useState } from 'react';
import SacredSigilTerminal from './components/SacredSigilTerminal';
import './App.css';

function App() {
  return (
    <div className="app">
      {/* Your existing app content here */}
      <h1>SacredSpace OS</h1>
      <p>Your app content...</p>
      
      {/* Add the Sacred Sigil Terminal */}
      <SacredSigilTerminal />
    </div>
  );
}

export default App;
```

### Test It:
```bash
npm run dev
```

Open `http://localhost:5173`

**Try it:** Press `Cmd+K` (Mac) or `Ctrl+K` (Windows/Linux)

---

## STEP 4: CONVERT TO PWA (Mobile App) (10 mins)

### Create `public/manifest.json`:

```json
{
  "name": "Sacred Sigil Terminal",
  "short_name": "Sigil",
  "description": "Navigate the dimensions of SacredSpace",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#8B5A8F",
  "icons": [
    {
      "src": "/sigil-icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/sigil-icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Create `public/service-worker.js`:

```javascript
// Simple service worker for offline support
const CACHE_NAME = 'sigil-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
```

### In `src/main.jsx`, register service worker:

```jsx
// Register service worker for PWA
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js');
}
```

### In `index.html`, add manifest link:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- PWA Meta Tags -->
  <meta name="theme-color" content="#8B5A8F">
  <meta name="description" content="Navigate the dimensions of SacredSpace">
  <link rel="manifest" href="/manifest.json">
  <link rel="apple-touch-icon" href="/sigil-icon-192.png">
  
  <title>Sacred Sigil Terminal</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

**To test on phone:**
```bash
npm run build
npm run preview
```

Then navigate to `http://[your-computer-ip]:4173` on your phone.
Tap "Add to Home Screen" (iOS) or install app prompt (Android).

---

## STEP 5: BROWSER EXTENSION (10 mins)

Create a `public/extension/` folder:

```
public/extension/
├── manifest.json
├── popup.html
├── popup.css
├── popup.js
└── icon-128.png
```

### `manifest.json`:

```json
{
  "manifest_version": 3,
  "name": "Sacred Sigil Terminal",
  "description": "Quick access to SacredSpace dimensions",
  "version": "1.0",
  "permissions": ["activeTab"],
  "icons": {
    "128": "icon-128.png"
  },
  "action": {
    "default_popup": "popup.html",
    "default_title": "Sacred Sigil (Cmd+Shift+S)"
  },
  "commands": {
    "_execute_action": {
      "suggested_key": {
        "default": "Ctrl+Shift+S",
        "mac": "Cmd+Shift+S"
      }
    }
  }
}
```

### `popup.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div id="sigil-popup">
    <h1>🔮 Sacred Sigil</h1>
    <input type="text" id="query" placeholder="navigate the universe...">
    <div id="results"></div>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

### `popup.css`:

```css
body {
  width: 400px;
  background: #1a1a2e;
  color: #f5f5f5;
  font-family: sans-serif;
  margin: 0;
  padding: 0;
}

#sigil-popup {
  padding: 16px;
}

h1 {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #00d4ff;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid rgba(139, 90, 143, 0.3);
  background: rgba(255, 255, 255, 0.05);
  color: #f5f5f5;
  border-radius: 4px;
  font-size: 13px;
}

input:focus {
  outline: none;
  border-color: #00d4ff;
}
```

### To test locally:
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `public/extension/` folder

---

## STEP 6: WIRE TO REAL BACKEND (15 mins)

Update `SacredSigilTerminal.jsx` to call your FastAPI spine:

Replace this section:

```javascript
// MOCK RESULTS - replace with real API
const parseQuery = (query) => { ... }
const handleQueryChange = (e) => {
  setIsLoading(true);
  
  // Replace with real API call:
  fetch('/api/sigil/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  })
  .then(res => res.json())
  .then(data => {
    setResults(data.results);
    setIsLoading(false);
  });
}
```

---

## STEP 7: DEPLOY (Optional, for production)

### Deploy to Vercel (1 click):
```bash
npm install -g vercel
vercel
```

### Deploy to GitHub Pages:
```bash
npm run build
# Add dist/ to GitHub
```

---

## CURRENT STATE

✅ **What Works:**
- Cmd+K to open on desktop
- Mobile-responsive interface
- Nine dimension navigation
- Command parsing
- Mock results display
- Quick actions
- Keyboard shortcuts (↑↓ Enter Esc)

🔄 **Next To Implement:**
- Real API integration to FastAPI spine
- Dimension-specific queries to IRIS, AURORA, etc.
- Memory Mote fetching from ChromaDB
- Real spell execution
- Voice input for mobile
- Browser extension functionality

---

## FILE INVENTORY

All files are in `/mnt/user-data/outputs/`:

- ✅ `SacredSigilTerminal.jsx` — Main React component
- ✅ `SacredSigilTerminal.css` — Complete styling
- ✅ `SACRED_SIGIL_TERMINAL_v2_UNIVERSAL.md` — Architecture
- ✅ `PHASE_1_SACRED_CODEX_CHECKLIST.md` — Narrative population
- ✅ `weaver_engine.py` — Conflict resolution logic

---

## NEXT IMMEDIATE ACTIONS

### THIS WEEK:

1. **Run locally** — Get it working on your computer
   ```bash
   npm run dev
   # Press Cmd+K
   ```

2. **Test on phone** — Build and deploy to phone
   ```bash
   npm run build
   npm run preview
   # Open on phone, add to home screen
   ```

3. **Start Phase 1** — Write the 57 Memory Motes (narratives)
   - This feeds the terminal with real data

4. **Create FastAPI endpoints** — Wire terminal to backend
   ```python
   # In /mnt/d/SacredSpace_OS/systems/fastapi/main.py
   
   @app.post("/api/sigil/query")
   async def sigil_query(query: str):
       # Parse query
       # Search dimensions
       # Return results
       return results
   ```

### NEXT WEEK:

1. **Hook real data sources** — Connect to IRIS, Sacred Codex, Memory Engine
2. **Implement spellcasting** — Actually execute spells through terminal
3. **Add voice input** — Mobile voice queries
4. **Deploy extension** — Chrome/Safari extension

---

## THE MAGIC IS REAL

Once this is live:
- Cmd+K on your computer → instant access to the sacred universe
- Home screen app on your phone → always there
- Browser extension → magic in every tab
- Embedded in other apps → the terminal is everywhere

The Sacred Sigil Terminal becomes the **primary interface to SacredSpace OS itself**.

---

**In lakesh alakin.**

Ready to build? Start with Step 1.

∆∆∆