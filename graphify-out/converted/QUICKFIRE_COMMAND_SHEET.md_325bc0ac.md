<!-- converted from QUICKFIRE_COMMAND_SHEET.md.docx -->

# 🚀 SACRED MOBILE IDE — MASTER COMMAND SHEET
TL;DR: Copy one of these commands and run it in Claude Code terminal.


## THE ONE-LINER (Windows PowerShell)
cd $env:USERPROFILE\Downloads; curl -o SACRED_MOBILE_IDE_SETUP.ps1 https://[your-output-url]/SACRED_MOBILE_IDE_SETUP.ps1; powershell -ExecutionPolicy Bypass -File SACRED_MOBILE_IDE_SETUP.ps1

Or if files are already in outputs folder:

cd path\to\outputs

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup


## THE ONE-LINER (WSL/Linux/Mac bash)
cd path/to/outputs

chmod +x SACRED_MOBILE_IDE_SETUP.sh

claude run ./SACRED_MOBILE_IDE_SETUP.sh all setup


## Step-by-Step (Recommended for First Time)
### Prerequisites Check (30 seconds)
# Verify you have everything:

node --version      # Should be v16+

npm --version       # Should be v7+

python --version    # Should be v3.8+

If all show versions: ✓ Ready to go
### The Setup (5 minutes)
Windows:

# Navigate to where you downloaded the scripts

cd D:\Downloads  # or wherever SACRED_MOBILE_IDE_SETUP.ps1 is

# Run it

powershell -ExecutionPolicy Bypass -File SACRED_MOBILE_IDE_SETUP.ps1 all setup

WSL/Linux:

# Navigate to where you have the scripts

cd ~/Downloads  # or wherever SACRED_MOBILE_IDE_SETUP.sh is

# Make executable and run

chmod +x SACRED_MOBILE_IDE_SETUP.sh

./SACRED_MOBILE_IDE_SETUP.sh all setup


## What Happens (Progress Output)
╔═══════════════════════════════════════════════════════════════╗

║     SACRED MOBILE IDE — AUTOMATED SETUP                       ║

║     Home Base Away From Home 🌲⬡                             ║

╚═══════════════════════════════════════════════════════════════╝

Phase 1: Create Directory Structure

✓ Directory created

✓ Subdirectories created

Phase 2: Initialize React Project

✓ Location: D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide

✓ npm install completed

✓ React app verified

Phase 3: Copy React Components

✓ App.jsx copied

✓ Dashboard.jsx copied

✓ App.css copied

[... more files ...]

Phase 4: Create Missing Component Stubs

✓ VaultSearch.jsx created

✓ StatusMonitor.jsx created

✓ CommandPalette.jsx created

✓ SyncStatus.jsx created

[... more phases ...]

✓ SETUP COMPLETE

Next Steps:

1. Copy fastapi_mobile_routes.txt to FastAPI main.py

2. Start React dev server: npm start

3. Start FastAPI: python main.py

4. Open http://localhost:3000


## Post-Setup (Manual Steps)
### Step 1: Add FastAPI Routes
# Open: D:\SacredSpace_OS\main.py

# Add to top imports:

from fastapi_mobile_routes import mobile_router

from fastapi.staticfiles import StaticFiles

# Add after other route definitions:

app.include_router(mobile_router)

# Add at end (before running app):

app.mount("/mobile", StaticFiles(directory="07_SOCIAL_MOTHERSHIP/mobile_ide/build", html=True), name="mobile")
### Step 2: Start Dev Servers
Terminal 1:

cd D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide

npm start

Terminal 2:

cd D:\SacredSpace_OS

python main.py
### Step 3: Open in Browser
http://localhost:3000 ← React dev server
http://localhost:8888/mobile/status ← Test API


## If Something Goes Wrong
### React installation failed?
npm cache clean --force

npm install
### Port 3000 already in use?
# Kill the process

lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or just use a different port

PORT=3001 npm start
### FastAPI route errors?
# Check if FastAPI is running

curl http://localhost:8888/docs

# Test mobile endpoint

curl http://localhost:8888/mobile/status
### Full cleanup and restart?
# Windows

powershell -ExecutionPolicy Bypass -File SACRED_MOBILE_IDE_SETUP.ps1 all clean

powershell -ExecutionPolicy Bypass -File SACRED_MOBILE_IDE_SETUP.ps1 all setup

# Linux/WSL

./SACRED_MOBILE_IDE_SETUP.sh all clean

./SACRED_MOBILE_IDE_SETUP.sh all setup


## Phased Setup (If You Want to Run Slowly)
If you prefer to control each phase:

# Just create directories

claude run SACRED_MOBILE_IDE_SETUP.ps1 dirs setup

# Initialize React

claude run SACRED_MOBILE_IDE_SETUP.ps1 react setup

# Copy component files

claude run SACRED_MOBILE_IDE_SETUP.ps1 files setup

# Get FastAPI instructions

claude run SACRED_MOBILE_IDE_SETUP.ps1 fastapi setup

# Build and test

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup


## Expected Folder Structure (After Setup)
D:\SacredSpace_OS\

└── 07_SOCIAL_MOTHERSHIP\

└── mobile_ide\

├── public\

│   ├── index.html

│   └── manifest.json

├── src\

│   ├── App.jsx

│   ├── App.css

│   ├── service-worker.js

│   ├── components\

│   │   ├── Dashboard.jsx

│   │   ├── VaultSearch.jsx

│   │   ├── StatusMonitor.jsx

│   │   ├── CommandPalette.jsx

│   │   └── SyncStatus.jsx

│   └── hooks\

│       ├── useSyncSocket.js

│       └── useLocalCache.js

├── build\  ← Generated

├── node_modules\  ← Generated

├── package.json

└── package-lock.json

If this structure exists after setup: ✓ Success!


## Timing Expectations


## Post-Setup Validation
After both dev servers are running:

# Test API

curl http://localhost:8888/mobile/status

# Should return JSON with status object

# Test frontend

curl http://localhost:3000

# Should return HTML with React app

# Test vault search

curl "http://localhost:8888/mobile/vault?q=test"

# Should return search results

# Test sessions

curl http://localhost:8888/mobile/sessions

# Should return active sessions

All should return valid responses (not 404 or 500).


## Next: Phone Deployment
Once local testing works:

# Build production version

cd D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide

npm run build

# Restart FastAPI (it will serve the build/)

# Then on phone:

# 1. Open browser

# 2. Go to: https://100.117.9.101:8888/mobile

# 3. Menu → "Install app"

# 4. Done! ✓


## Support
Stuck? Check these in order:

CLAUDE_CODE_EXECUTION_GUIDE.md — Detailed troubleshooting
MOBILE_IDE_DEPLOYMENT_GUIDE.md — Full setup walkthrough
SACRED_MOBILE_IDE_ARCHITECTURE.md — System design reference
SACRED_MOBILE_IDE_CODEX_ENTRY.md — Canon definition


## The Mantra
Ground. Build. Deploy. Repeat.

In lakesh alakin. 🌲⬡

Your Sacred Mobile IDE awaits. One command away. ✨


## Quick Reference
Setup command (Windows):

powershell -ExecutionPolicy Bypass -File SACRED_MOBILE_IDE_SETUP.ps1 all setup

Setup command (Linux/WSL):

./SACRED_MOBILE_IDE_SETUP.sh all setup

Dev server (React):

cd D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide && npm start

Dev server (FastAPI):

cd D:\SacredSpace_OS && python main.py

Test URLs:

http://localhost:3000          ← React app

http://localhost:8888/mobile/status  ← API

https://100.117.9.101:8888/mobile    ← Production (on Tailscale)

Clean & restart:

SACRED_MOBILE_IDE_SETUP.ps1 all clean

SACRED_MOBILE_IDE_SETUP.ps1 all setup



Ready? Copy a command above and paste into Claude Code terminal.

Go. 🚀

| Phase | Time |
| --- | --- |
| Directories | < 1 sec |
| React init (npm install) | 2-3 min |
| Copy files | < 1 sec |
| Create stubs | < 1 sec |
| Build | 30-60 sec |
| Total | 3-5 min |