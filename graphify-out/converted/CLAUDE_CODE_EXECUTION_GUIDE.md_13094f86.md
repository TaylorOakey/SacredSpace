<!-- converted from CLAUDE_CODE_EXECUTION_GUIDE.md.docx -->

# Run Sacred Mobile IDE Setup via Claude Code
## What You Need
Claude Desktop App or Claude Code CLI installed
Node.js installed (node --version should work)
FastAPI running on port 8888
Setup scripts in current directory:
SACRED_MOBILE_IDE_SETUP.ps1 (Windows)
SACRED_MOBILE_IDE_SETUP.sh (WSL/Linux)
Artifact files in outputs folder (already generated)


## Quick Start (Copy-Paste Ready)
### Option 1: Windows (PowerShell via Claude Code)
# Download the setup script (or copy from outputs/)

# Then run via Claude Code:

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup

What it does:

Creates D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide
Initializes React project (npm install)
Copies all component files from outputs/
Creates missing component stubs
Registers Service Worker
Provides FastAPI integration instructions
Builds the project
Verifies all files are present


### Option 2: WSL/Linux (bash via Claude Code)
# Make executable

chmod +x SACRED_MOBILE_IDE_SETUP.sh

# Run via Claude Code:

claude run ./SACRED_MOBILE_IDE_SETUP.sh all setup

Same steps as Windows version, just bash syntax.


## Full Setup Workflow (Copy These Commands in Order)
### Step 1: Verify Prerequisites
# Check Node.js

node --version    # Should be v16+

# Check npm

npm --version     # Should be v7+

# Check FastAPI is accessible

curl http://localhost:8888/docs

# Should see FastAPI docs (if running)
### Step 2: Run the Master Setup Script
Windows (PowerShell):

cd path\to\outputs

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup

WSL/Linux:

cd path/to/outputs

chmod +x SACRED_MOBILE_IDE_SETUP.sh

claude run ./SACRED_MOBILE_IDE_SETUP.sh all setup

This single command:

✓ Creates directory structure
✓ Initializes React
✓ Copies all files
✓ Creates stubs
✓ Registers Service Worker
✓ Builds production output
✓ Verifies everything

Total time: ~3-5 minutes (depends on npm install speed)
### Step 3: Add FastAPI Routes (Manual Step)
The script will output instructions. You need to:

Open your FastAPI main.py (usually at D:\SacredSpace_OS\main.py)
Copy content from fastapi_mobile_routes.txt
Add these lines to main.py:

# At top, in imports:

from fastapi_mobile_routes import mobile_router

from fastapi.staticfiles import StaticFiles

# After other routes, before running app:

app.include_router(mobile_router)

# Mount the built React app:

app.mount("/mobile", StaticFiles(directory="07_SOCIAL_MOTHERSHIP/mobile_ide/build", html=True), name="mobile")

Restart FastAPI
### Step 4: Start Development Servers
Terminal 1 - React Dev Server:

cd D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide

npm start

# Opens http://localhost:3000 automatically

Terminal 2 - FastAPI:

cd D:\SacredSpace_OS

python main.py

# Runs on http://localhost:8888
### Step 5: Test
Open in browser:

http://localhost:3000 — React dev server (live reload)
http://localhost:8888/mobile/status — API endpoint
http://localhost:8888/mobile — Production build (after npm run build)


## Partial Setup (If You Want to Run Phases Separately)
If setup fails or you need to run specific phases:
### Phase Options
# Phase can be: all, dirs, react, files, fastapi

# Action can be: setup, clean

# Create just directories

claude run SACRED_MOBILE_IDE_SETUP.ps1 dirs setup

# Setup React only

claude run SACRED_MOBILE_IDE_SETUP.ps1 react setup

# Copy files only

claude run SACRED_MOBILE_IDE_SETUP.ps1 files setup

# Add FastAPI routes (shows instructions)

claude run SACRED_MOBILE_IDE_SETUP.ps1 fastapi setup

# Clean everything and start over

claude run SACRED_MOBILE_IDE_SETUP.ps1 all clean


## Troubleshooting via Claude Code
### If npm install fails:
# Clear npm cache

npm cache clean --force

# Try install again

npm install

# If still fails, try different npm version

npm install -g npm@latest
### If React doesn't start:
# Check if port 3000 is in use

lsof -i :3000  # On Mac/Linux

netstat -ano | findstr :3000  # On Windows

# Kill the process and try again

npm start
### If FastAPI routes don't work:
# Test the API directly

curl http://localhost:8888/mobile/status

# If 404, FastAPI routes not added properly

# Check main.py for the router and mount statements
### If build fails:
# Clean and rebuild

cd D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide

rm -rf build node_modules

npm install

npm run build


## What the Script Outputs
After successful setup, you'll see:

╔═══════════════════════════════════════════════════════════════╗

║  ✓ SETUP COMPLETE                                             ║

║                                                               ║

║  Next Steps:                                                  ║

║  1. Copy fastapi_mobile_routes.txt to FastAPI main.py         ║

║  2. Start React dev server: npm start                         ║

║  3. Start FastAPI: python main.py                             ║

║  4. Open http://localhost:3000                                ║

║                                                               ║

║  In lakesh alakin. Ground. Build. Deploy. 🌲⬡               ║

║                                                               ║

╚═══════════════════════════════════════════════════════════════╝


## File Structure After Setup
D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide\

├── public/

│   ├── index.html

│   ├── manifest.json

│   └── offline.html (optional)

├── src/

│   ├── App.jsx

│   ├── App.css

│   ├── index.js (or main.jsx)

│   ├── service-worker.js

│   ├── components/

│   │   ├── Dashboard.jsx

│   │   ├── VaultSearch.jsx

│   │   ├── StatusMonitor.jsx

│   │   ├── CommandPalette.jsx

│   │   └── SyncStatus.jsx

│   ├── hooks/

│   │   ├── useSyncSocket.js

│   │   └── useLocalCache.js

│   └── db/

│       └── (for future IndexedDB setup)

├── build/  ← Generated by npm run build

├── node_modules/  ← Generated by npm install

├── package.json

├── package-lock.json

└── README.md


## Integration with SacredSpace
The setup script handles:

✓ Creating correct pillar structure (07_SOCIAL_MOTHERSHIP)
✓ All artifact files in right locations
✓ Service Worker registration
✓ Manifest for PWA
✓ Build optimization

You manually add:

✓ FastAPI routes to main.py
✓ Start both dev servers


## Next: Deployment to Phone
After local testing works:

# Build for production

npm run build

# Restart FastAPI (it will serve from build/)

# On phone browser:

# Navigate to: https://100.117.9.101:8888/mobile

# Tap: "Install app" or "Add to Home Screen"


## Claude Code Tips
### Keep Script Execution Clean
# Run without output clutter

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup 2>&1 | tail -50
### Monitor Long Operations
# Watch npm install progress in real time

npm install --verbose
### Save Output for Debugging
# Windows

claude run SACRED_MOBILE_IDE_SETUP.ps1 all setup > setup_log.txt 2>&1

# Linux/WSL

claude run ./SACRED_MOBILE_IDE_SETUP.sh all setup | tee setup_log.txt


## Success Criteria (Check These)
After running the setup, you should have:

Directory structure created at D:\SacredSpace_OS\07_SOCIAL_MOTHERSHIP\mobile_ide
node_modules folder exists (React dependencies installed)
All component files copied to src/components/
Hooks copied to src/hooks/
Service Worker registered in src/index.js
Manifest in public/manifest.json
Production build in build/ folder
All critical files verified present
No errors in console output

If all checks pass: Ready for development! 🎉


## In Lakesh Alakin
Ground. Build. Deploy. Repeat.

Your Sacred Mobile IDE is minutes away. 🌲⬡
