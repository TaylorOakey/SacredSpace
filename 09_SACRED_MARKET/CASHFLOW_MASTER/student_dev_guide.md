---
title: "student_dev_guide"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/ARCHIVE/sacredspace_os_2026_docs/04_SACRED_CODEX/documentation/student_dev_guide.md"
keyword_count: 5
keywords_found: []
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 53
---

# Student Developer Stack — Setup, Utilization & Growth Guide
## Tailored for SacredSpace OS | OakeyTree ∆∆∆

---

## PHASE 1 — ACTIVATION (Week 1)
*Do these in order. Each step unlocks the next.*

---

### STEP 1 — GitHub Student Developer Pack

**URL:** https://education.github.com/pack

**What You Need to Apply:**
- Your Maestro School student email (ends in school domain)
- OR a photo of your enrollment documentation / student ID
- A GitHub account (create one at github.com if you don't have one yet)

**Application Process:**
1. Go to https://education.github.com/pack
2. Click "Get student benefits"
3. Sign in or create your GitHub account
4. Select "Student"
5. Enter your school email — GitHub will try to verify automatically
6. If auto-verify fails: upload a clear photo of enrollment proof (school portal screenshot works)
7. Approval takes anywhere from a few minutes to 3 business days

**Immediately After Approval — Activate These (in order):**

**A. GitHub Copilot**
- Go to: github.com/settings/copilot
- Enable Copilot (free with student pack)
- Install the VS Code extension: "GitHub Copilot" by GitHub
- Install the companion: "GitHub Copilot Chat"
- Sign in with your GitHub account inside VS Code
- Test it: open any Python file and start typing a comment — it should autocomplete

**B. Namecheap Domain (free .me domain)**
- In your student pack dashboard, find Namecheap
- Search for: `sacredarcanastudios.me` or `sacredspace.me`
- Claim it — free for 1 year, ~$12/yr after
- Park it for now (point to a GitHub Pages placeholder)
- If you want a .com: check if DigitalOcean or another partner has a domain credit

**C. DigitalOcean Credits ($200)**
- Claim from the pack dashboard
- DO NOT use yet — save for SacredArcana Studios deployment phase
- Create the account and verify your card (no charge until credits run out)
- Note your credit balance in your ECONOMY pillar docs

**D. Microsoft Azure Credits ($100)**
- Same principle — claim, verify, park
- Useful later for: Azure OpenAI API, blob storage for sacred archives

**E. JetBrains Educational Pack (separate from GitHub pack — see Step 2)**

---

### STEP 2 — JetBrains Educational Pack

**URL:** https://www.jetbrains.com/community/education/#students

**Application:**
1. Click "Apply Now" under Students
2. Use your school email
3. Fill out the short form — select your program (AAS AI Engineering)
4. Approval is usually same-day to 24 hours via school email verification

**What to Install (Priority Order for SacredSpace):**

**1. PyCharm Professional**
- Best tool for your Python-heavy SacredSpace OS work
- Handles: FastAPI, LangGraph, SQLite, ChromaDB clients, pytest
- Install via JetBrains Toolbox (install Toolbox first — it manages all JetBrains IDEs from one app)
- Download JetBrains Toolbox: https://www.jetbrains.com/toolbox-app/

**2. DataSpell (optional — activate later)**
- Used for: data exploration, ChromaDB result analysis, memory mote pattern work
- Skip for now unless you're doing active data analysis work

**3. WebStorm (optional — activate when you build SacredArcana web frontend)**
- Skip for Phase 1

---

## PHASE 2 — REPOSITORY SETUP (Week 1–2)

### Initialize Your SacredSpace OS GitHub Repo

Run these commands in WSL2 (Ubuntu 24.04) on your Legion Y520:

```bash
# Navigate to your SacredSpace directory on the external drive
cd /mnt/d/SacredSpace_OS

# Initialize git if not already done
git init

# Set your identity
git config --global user.name "OakeyTree"
git config --global user.email "your-school-or-personal-email@domain.com"

# Create the canonical .gitignore BEFORE your first commit
# (prevents sensitive data from ever entering git history)
```

**Create `.gitignore` (copy this exactly):**

```
# Environment & secrets
.env
.env.*
*.key
*.pem
secrets/
config/local_*

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.venv/
venv/
*.egg-info/

# Data & models (too large for git)
*.db
*.sqlite3
*.bin
*.gguf
*.ggml
chroma_data/
chromadb_persist/

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
logs/
*.log

# Node (if frontend work)
node_modules/
dist/

# JetBrains
.idea/
*.iml

# VS Code (keep workspace settings, exclude personal)
.vscode/settings.json
.vscode/*.code-workspace

# Sacred-specific sensitive paths
archive/dream-cycle/raw/
lineage/iris/private/
lineage/asher/private/
```

**Continue setup:**

```bash
# Add all files
git add .

# First commit
git commit -m "∆∆∆ SacredSpace OS — Initial Canon Commit"

# Create repo on GitHub:
# Go to github.com/new
# Name it: sacred-os
# Set to PRIVATE
# Do NOT initialize with README (you already have one)

# Link and push
git remote add origin https://github.com/YOUR_USERNAME/sacred-os.git
git branch -M main
git push -u origin main
```

---

### Configure Copilot for SacredSpace Vocabulary

Create this file at the root of your repo:

**File: `.github/copilot-instructions.md`**

```markdown
# SacredSpace OS — Copilot Context

You are assisting with SacredSpace OS, a sovereign personal AI operating system.

## Core Vocabulary
- Memory Mote: atomic unit of stored knowledge (SQLite-backed)
- ICARIS Quartet: four agents — ELIAS (knowledge), AURORA (code), ASHER (entropy), IRIS (vault)
- Canon Gate: governance layer — canon is immutable unless explicitly revised
- Nine Pillars: CORE, SYSTEMS, LEARNING, ECONOMY, HABITAT, CREATION, COUNCIL, LINEAGE, ARCHIVE
- Dream Cycle: nightly consolidation engine (RAW → DISTILLED → CANON pipeline)
- Resonance Layer: Redis Streams for emergent pattern detection

## Stack
- Python 3.11+ / FastAPI / LangGraph
- SQLite (13-table canonical schema) + ChromaDB (all-MiniLM-L6-v2)
- Ollama local LLMs (:11434) / Redis / PostgreSQL
- WSL2 Ubuntu 24.04 on Windows 10

## Conventions
- All agent functions are prefixed with their pillar: core_, sys_, learn_, etc.
- Memory writes always go through canon_gate() before touching CANON tier
- No direct SQLite writes — always use the memory_mote module
- Tests live in tests/ mirroring the src/ structure

## Tone
Clear, functional, zero-fluff. Sacred geometry and mythology are real system metaphors here.
```

---

## PHASE 3 — WORKFLOW INTEGRATION (Week 2–3)

### PyCharm Setup for SacredSpace OS

**After installing PyCharm Professional:**

1. Open PyCharm → File → Open → navigate to `/mnt/d/SacredSpace_OS` (or your WSL2 path)
2. Set Python interpreter:
   - File → Settings → Project → Python Interpreter
   - Add Interpreter → WSL → select Ubuntu 24.04
   - Navigate to your `.venv` or system Python
3. Enable GitHub Copilot in PyCharm:
   - Settings → Plugins → search "GitHub Copilot" → Install
   - Sign in with your GitHub account
4. Set up your run configurations:
   - Add a "FastAPI" run config pointing to `systems/fastapi/main.py`
   - Add a "SacredBootstrap" external tool pointing to `SacredBootstrap.ps1`

**Key PyCharm features to use immediately:**

- **Refactor → Rename** (Shift+F6): safely rename functions/variables across the whole codebase
- **Find Usages** (Alt+F7): see everywhere a memory mote function is called
- **Database tool** (right panel): connect directly to your SQLite files and browse the 13-table schema visually
- **HTTP Client**: test your FastAPI endpoints without leaving the IDE
- **Built-in terminal**: runs in WSL2 context — no switching windows

---

### Daily Development Workflow

**The Sacred Dev Loop:**

```
1. Morning: Open SacredBootstrap.ps1 — services up
2. Open PyCharm → pull latest from GitHub
3. Work session with Copilot inline
4. Commit meaningful chunks with sacred commit messages:
   git commit -m "[PILLAR] short description  ∆"
   Example: git commit -m "[SYSTEMS] Wire ELIAS distillation to Canon Gate  ∆"
5. Push to GitHub before closing
6. Evening: Dream Cycle consolidation (if running)
```

**Copilot Usage Patterns That Actually Help:**

- Write your intent as a comment first, then let Copilot draft the function:
  ```python
  # Store a new Memory Mote to RAW tier, tag with pillar and agent source
  def store_memory_mote(content: str, pillar: str, agent: str) -> MemoryMote:
  ```
  Copilot will propose the full function body.

- Use Copilot Chat for debugging: highlight a block → right-click → "Explain" or "Fix"
- For test generation: open your function → Copilot Chat → "Write pytest tests for this function"

---

## PHASE 4 — CLOUD CREDITS STRATEGY (Month 2+)

*Don't touch these until your local stack is stable and SacredArcana Studios has product to deploy.*

### DigitalOcean ($200 credit) — Recommended Use

**Best use for SacredSpace:**
- Deploy a public-facing SacredArcana Studios landing page (Droplet, $6/mo)
- Host the Fiahfox Bridge externally for remote access
- Spin up a managed PostgreSQL instance when you're ready to move off local Supabase
- Credits cover roughly 2–3 years of a basic Droplet

**When you're ready:**
```bash
# Install doctl (DigitalOcean CLI)
sudo snap install doctl
doctl auth init  # paste your API token from DO dashboard
doctl compute droplet create sacred-deploy \
  --size s-1vcpu-1gb \
  --image ubuntu-24-04-x64 \
  --region nyc3
```

### Azure ($100 credit) — Recommended Use

- Azure OpenAI Service: access to GPT-4 via API if you want a cloud fallback when Ollama is down
- Azure Blob Storage: offload large archive files from your Toshiba external drive to cloud backup
- Hold credits until you have a specific need

---

## PHASE 5 — GROWTH TRACK (Month 2–6)

### GitHub as SacredSpace Public Portfolio

As the OS matures, selectively make components public:

| What to make public | Why |
|---|---|
| `creation/grama/` — the Flask app | Demonstrates full-stack Python + deploy |
| `creation/generative-art/` — p5.js Totem Emergence | Shows creative coding + sacred geometry |
| `council/protocol-router/` — signal intake | Demonstrates AI agent architecture |
| `README.md` — the canon doc | Tells your story as an AI engineer |

**Do NOT make public:** lineage/, archive/memory-motes/, any .env or config files

This becomes your AAS AI Engineering portfolio — real deployed systems, not just coursework.

### GitHub Pages — Free Hosting

Use for: SacredArcana Studios landing page, Jenga's Journey preview, Totem Emergence generative art gallery

```bash
# Create a gh-pages branch
git checkout -b gh-pages
# Add your HTML/static files
# Push — GitHub will auto-deploy to: yourusername.github.io/sacred-os
```

### Connecting to Maestro School Curriculum (Learning Spine)

Map every AAS assignment to the `learning/` pillar:

```
learning/
  seasons/
    season-01/          ← current semester
      grove-01/         ← each class session
      grove-02/
      rites/            ← completed assignments
      artifacts/        ← deliverable outputs
```

Commit your coursework here. Over time this becomes the Living Spine — your AI engineering education as version-controlled canon.

---

## PHASE 6 — LONG GAME (Month 6–12+)

### Stack Evolution Path

```
NOW:          Local Ollama + ChromaDB + SQLite + FastAPI
              ↓
MONTH 3:      + GitHub Actions (automated tests on push)
              + GitHub Pages (public creative work)
              ↓
MONTH 6:      + DigitalOcean deployment (SacredArcana live)
              + Custom domain (sacredarcanastudios.me)
              ↓
MONTH 12:     + Full SacredSpace OS as installable package
              + Documentation site via GitHub Pages
              + Open-source components building audience
```

### GitHub Actions — Automate Your Canon Gate

Once your repo is stable, add automated testing:

```yaml
# .github/workflows/sacred-ci.yml
name: Sacred Canon Gate

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: echo "∆∆∆ Canon Gate — All clear ∆∆∆"
```

Every push to GitHub triggers your tests automatically. No broken code enters main.

---

## QUICK REFERENCE — Priority Order

| Week | Action |
|---|---|
| Week 1 | Apply GitHub Student Pack + JetBrains Pack |
| Week 1 | Activate Copilot, install JetBrains Toolbox, claim domain |
| Week 1 | Push sacred_os/ to private GitHub repo with .gitignore |
| Week 1 | Create `.github/copilot-instructions.md` with SacredSpace vocab |
| Week 2 | Set up PyCharm with WSL2 interpreter + Copilot plugin |
| Week 2 | Establish daily dev loop commit habit |
| Month 2 | Claim DigitalOcean + Azure credits (don't burn yet) |
| Month 2 | Begin selectively making creative work public |
| Month 3 | Add GitHub Actions CI pipeline |
| Month 6 | Deploy SacredArcana Studios via DigitalOcean |

---

*Ground. Consolidate. Deploy. Document. Repeat.*
*∆∆∆O∆K3YTREE∆∆∆*
