---
title: "copilot-instructions"
source: "/mnt/d/SacredSpace_OS/04_SACRED_CODEX/DISTILLED/copilot-instructions.md"
keyword_count: 8
keywords_found: [etsy, merchant, revenue]
pillar: "04_SACRED_CODEX"
date_indexed: "2026-05-21"
cashflow_rank: 35
---

# ⟁ SACREDSPACE OS — COPILOT SYSTEM INSTRUCTIONS
# .github/copilot-instructions.md
# Read automatically by GitHub Copilot in VS Code every session.
# Last updated: May 2026

---

## WHO YOU ARE WORKING WITH

You are assisting Taylor, sole architect of SacredSpace OS — a sovereign,
local-first personal AI operating system. Taylor thinks in systems, symbols,
and narratives. Be direct, technical, and precise. Don't over-explain.
Prefer actual commands over descriptions of commands.

---

## MACHINE OVERVIEW

| Item | Value |
|------|-------|
| Machine | Lenovo Legion Y520 |
| OS | Windows 11 |
| WSL2 | Ubuntu 24.04 (`useroak3ytree` on `LAPTOP-7Q65KPI7`) |
| GPU | GTX 1060 6GB |
| Primary work drive | D: |
| System drive | C: (Windows — do not reorganize) |
| External backup | Toshiba HDD (SacredArchive) |
| Tailscale IP | 100.117.9.101 |
| Ollama endpoint | 192.168.240.1:11434 (WSL2) |

---

## THE NINE-PILLAR ARCHITECTURE (CANON — DO NOT DEVIATE)

All SacredSpace work lives under `D:\SacredSpace_OS\` (WSL2: `/mnt/d/SacredSpace_OS/`).
The canonical nine pillars are:

```
D:\SacredSpace_OS\
├── 01_OBSIDIAN_VAULTS\     ← Obsidian vault, knowledge archive, exported notes
│   └── SacredSpace_Vault\  ← The live vault (NEVER edit .md files directly here)
├── 02_COUNCIL_GROVE\       ← Multi-AI governance, cross-agent protocols, handoffs
├── 03_NEURAL_FOREST\       ← LLM pipeline: Scout, Gardener, harvester scripts
├── 04_SACRED_CODEX\        ← Canon ledger, spell entries, codex documents
├── 05_MEMORY_ENGINE\       ← SQLite DBs, ChromaDB, Redis, Ebbinghaus decay system
├── 06_AGENT_LAYER\         ← ICARIS Quartet scripts, FastAPI spine, Chrome extension
│   └── sacred-chrome\      ← Chrome extension (manifest.json, newtab.html, etc.)
├── 07_SOCIAL_MOTHERSHIP\   ← Brand content, social media, SacredArcana Studios
├── 08_LEARNING_PATH\       ← AAS AI Engineering coursework, spells, rites, groves
└── 09_SACRED_MARKET\       ← Print-on-demand, Etsy, revenue, artifact listings
```

Also at `D:\SacredSpace_OS\`:
- `systems/sski/icaris_env.py` — ICARIS daemon
- `systems/fastapi/main.py`   — FastAPI spine (port 8888)
- `CLAUDE.md`                  — Claude Code instruction scroll
- `02_COUNCIL_GROVE/handoff_ritual.py`        — agent handoff script
- `02_COUNCIL_GROVE/LATEST_HANDOFF.md`        — current handoff capsule

---

## FILE TYPE ROUTING TABLE

When organizing files, route by type AND content:

### Python Scripts (.py)
| Content | Destination |
|---------|-------------|
| Agent logic (ELIAS, AURORA, ASHER, IRIS) | `06_AGENT_LAYER/` |
| FastAPI routes / spine modules | `systems/fastapi/` |
| ICARIS / SSKI / memory system | `systems/sski/` |
| Data harvesting / scraping | `03_NEURAL_FOREST/` |
| Artifact / merchant / market logic | `09_SACRED_MARKET/` |
| Vault sync / Obsidian integration | `01_OBSIDIAN_VAULTS/` |
| Learning / study scripts | `08_LEARNING_PATH/` |
| Utility / one-off scripts | `00_SYSTEM_CORE/scripts/` |

### Shell Scripts (.sh, .ps1, .bat)
| Content | Destination |
|---------|-------------|
| Boot / startup scripts | `D:\SacredSpace_OS\` (root) |
| Deploy scripts | `D:\SacredSpace_OS\` (root) |
| WSL2 config scripts | `00_SYSTEM_CORE/scripts/` |
| Backup scripts | `06_AGENT_LAYER/` or `00_SYSTEM_CORE/scripts/` |

### Markdown / Documentation (.md)
| Content | Destination |
|---------|-------------|
| Obsidian vault notes | `01_OBSIDIAN_VAULTS/SacredSpace_Vault/` (via vault_watcher only) |
| Canon codex entries | `04_SACRED_CODEX/` |
| README files | Keep at their project root |
| Cross-AI protocols | `02_COUNCIL_GROVE/` |
| Session logs / handoffs | `02_COUNCIL_GROVE/HANDOFFS/` |
| Brand / social content | `07_SOCIAL_MOTHERSHIP/` |
| Learning notes / spells | `08_LEARNING_PATH/` |
| Duplicate READMEs | Archive to `00_SYSTEM_CORE/archive/` |

### HTML / CSS / JS
| Content | Destination |
|---------|-------------|
| Chrome extension files | `06_AGENT_LAYER/sacred-chrome/` |
| Dashboard / portal builds | `06_AGENT_LAYER/sacred-chrome/` or `07_SOCIAL_MOTHERSHIP/` |
| Learning / study tools | `08_LEARNING_PATH/` |

### JSON / YAML / Config
| Content | Destination |
|---------|-------------|
| VS Code settings | Stay at `.vscode/` at D: root |
| GitHub Actions | Stay at `.github/` at D: root |
| Obsidian settings | Stay at `.obsidian/` |
| App configs (.env) | `00_SYSTEM_CORE/` (NEVER commit .env to git) |
| Schema / data files | `05_MEMORY_ENGINE/` |
| Agent state files | Near their owning script |

### Media Files
| Type | Destination |
|------|-------------|
| Photos / images (.jpg, .png, .webp) | `07_SOCIAL_MOTHERSHIP/media/` or `09_SACRED_MARKET/assets/` |
| Videos (.mp4, .mov) | `07_SOCIAL_MOTHERSHIP/media/video/` |
| Audio | `07_SOCIAL_MOTHERSHIP/media/audio/` |
| AI-generated images | `09_SACRED_MARKET/assets/ai_generated/` |
| Family / personal media | `07_SOCIAL_MOTHERSHIP/family/` |

### Databases
| Type | Destination |
|------|-------------|
| SQLite (.db) | `05_MEMORY_ENGINE/databases/` |
| ChromaDB data | `05_MEMORY_ENGINE/chromadb/` |
| Backups (.db.bak, .sql) | `06_BACKUPS/` or `05_MEMORY_ENGINE/databases/backups/` |

### PDFs / Documents
| Content | Destination |
|---------|-------------|
| Technical guides / references | `04_SACRED_CODEX/documentation/` |
| Course materials (AAS) | `08_LEARNING_PATH/course_materials/` |
| Business / legal docs | `00_SYSTEM_CORE/documents/` |
| Brand documents | `07_SOCIAL_MOTHERSHIP/brand/` |

### ZIP / Archives
| Content | Destination |
|---------|-------------|
| Extension builds | `06_AGENT_LAYER/builds/` |
| Backup archives | `06_BACKUPS/` |
| Legacy imports | `08_EXPORTS/legacy_imports/` → archive, don't unpack unless needed |

---

## D: DRIVE CURRENT STATE (May 2026)

The D: drive root still has legacy folders being migrated. When helping organize:

**These folders at D: root are LEGACY — should migrate to nine-pillar structure:**
```
01_AGENTS       → 06_AGENT_LAYER/
01_VAULT        → 01_OBSIDIAN_VAULTS/
02_AGENT_SYSTEM → 06_AGENT_LAYER/systems/
02_CODE         → 06_AGENT_LAYER/code/
02_GITHUB       → 02_COUNCIL_GROVE/github/
02_MEMORY       → 05_MEMORY_ENGINE/
03_AI_MODELS    → 02_COUNCIL_GROVE/models/
03_ARCHIVES     → 00_SYSTEM_CORE/archive/
03_ASSETS       → 07_SOCIAL_MOTHERSHIP/assets/
04_EXPORTS      → 01_OBSIDIAN_VAULTS/exports/
04_PROJECTS     → 03_NEURAL_FOREST/projects/
05_DATABASE     → 05_MEMORY_ENGINE/databases/
05_MEDIA        → 07_SOCIAL_MOTHERSHIP/media/
05_WORLD_ENGINE → 03_NEURAL_FOREST/world_engine/
06_BACKUPS      → 00_SYSTEM_CORE/backups/
06_FAMILY_SYSTEMS → 07_SOCIAL_MOTHERSHIP/family/
06_LOGS         → 00_SYSTEM_CORE/logs/
07_INSTALLERS   → 00_SYSTEM_CORE/installers/
07_INTERFACES   → 06_AGENT_LAYER/interfaces/
08_EXPORTS      → 01_OBSIDIAN_VAULTS/exports/ (check for conflicts)
08_LOGS         → 00_SYSTEM_CORE/logs/ (check for conflicts)
09_TEMP         → 00_SYSTEM_CORE/temp/
```

**These at D: root are PERMANENT — do not move:**
```
SacredSpace_OS\    ← canonical project root (DO NOT MOVE)
.github\           ← GitHub config (stay at D: root)
.vscode\           ← VS Code config (stay at D: root)
.obsidian\         ← Obsidian config (stay at D: root)
.env               ← environment vars (stay at D: root, never commit)
CLAUDE.md          ← if at D: root, this is a copy — canonical is at SacredSpace_OS\
```

**Loose files at D: root to route:**
```
*.md files         → 04_SACRED_CODEX/documentation/ (after reviewing content)
*.pdf files        → 04_SACRED_CODEX/documentation/ or 08_LEARNING_PATH/
*.jpg, *.png       → 07_SOCIAL_MOTHERSHIP/media/
*.mp4, *.mov       → 07_SOCIAL_MOTHERSHIP/media/video/
Duplicate READMEs  → Delete or archive — keep only the most recent
```

---

## C: DRIVE RULES

**Do not reorganize C: drive.** It is a standard Windows system drive.

You may work with files in:
- `C:\Users\USER\Downloads\` — staging area for downloads before moving to D:
- `C:\Users\USER\Documents\` — only if Taylor puts something there
- `C:\Users\USER\AppData\` — config only, never reorganize
- `C:\Program Files\` — read only, never touch

The WSL2 home directory is at `C:\Users\USER\AppData\Local\Packages\...\LocalState\rootfs\home\useroak3ytree\` — access via WSL2 as `~`, never via Windows Explorer reorganization.

---

## HOW TO HELP ORGANIZE FILES

### Decision Tree for File Placement

```
Is it a Python script?
  → What does it do? Route to the matching pillar above.

Is it a markdown file?
  → Is it a vault note? → 01_OBSIDIAN_VAULTS/ (via vault_watcher, not direct edit)
  → Is it documentation? → 04_SACRED_CODEX/
  → Is it a protocol or session log? → 02_COUNCIL_GROVE/

Is it media (image/video)?
  → Is it for social/brand? → 07_SOCIAL_MOTHERSHIP/media/
  → Is it a product asset? → 09_SACRED_MARKET/assets/
  → Is it personal/family? → 07_SOCIAL_MOTHERSHIP/family/

Is it a config file?
  → .env, .vscode, .github, .obsidian → stay at D: root
  → App-specific config → near the app it configures

Is it a duplicate?
  → Keep the newer version. Archive the older with timestamp suffix.
  → Never silently delete — archive to 00_SYSTEM_CORE/archive/

Is it unclear?
  → ASK before moving. Do not guess on important files.
```

### Commands to Use in WSL2

```bash
# Safe move with confirmation
mv -iv /mnt/d/sourcefile /mnt/d/SacredSpace_OS/destination/

# Move with backup
cp /mnt/d/file /mnt/d/SacredSpace_OS/destination/ && rm /mnt/d/file

# Find duplicates by name
find /mnt/d -name "README.md" -not -path "*/.git/*" 2>/dev/null

# Find files by type and age
find /mnt/d -name "*.py" -newer /mnt/d/SacredSpace_OS -not -path "*/.venv/*"

# Archive instead of delete
mkdir -p /mnt/d/SacredSpace_OS/00_SYSTEM_CORE/archive/
mv /mnt/d/file /mnt/d/SacredSpace_OS/00_SYSTEM_CORE/archive/file_$(date +%Y%m%d)
```

### PowerShell equivalents (from Windows terminal)

```powershell
# Move file
Move-Item -Path "D:\sourcefile" -Destination "D:\SacredSpace_OS\destination\" -WhatIf
# Remove -WhatIf to actually run

# Find duplicates
Get-ChildItem -Path "D:\" -Filter "*.md" -Recurse | Group-Object Name | Where-Object Count -gt 1

# Archive a folder
Compress-Archive -Path "D:\OldFolder" -DestinationPath "D:\SacredSpace_OS\00_SYSTEM_CORE\archive\OldFolder_$(Get-Date -Format 'yyyyMMdd').zip"
```

---

## HARD RULES — NEVER VIOLATE

1. **Never edit Obsidian `.md` files directly from code.** Always use `vault_watcher.py` or the FastAPI `/beams` endpoint. Direct edits corrupt Obsidian's cache.

2. **Never move `SacredSpace_OS\` itself.** It is the canonical project root. Everything else can move; this stays at `D:\`.

3. **Never commit `.env` to git.** It contains API keys. Check `.gitignore` exists before any git operation.

4. **Never delete without archiving first.** Move to `00_SYSTEM_CORE/archive/` with a date suffix. Only delete after Taylor confirms.

5. **Never install paid tools.** All tools must be 100% open-source and zero-cost. Stack: Python, PowerShell, SQLite, ChromaDB, Ollama, Redis, FastAPI, Git, Obsidian.

6. **Never move files during an active FastAPI session** without confirming the spine won't break. The spine reads from relative paths.

7. **The ICARIS DAG governs all writes:** ASHER verifies → ELIAS plans → AURORA executes → IRIS logs. For file operations: check before move, confirm before delete, log everything significant.

---

## KEY FILE LOCATIONS (quick reference)

```
D:\SacredSpace_OS\
├── CLAUDE.md                          ← Claude Code instruction scroll
├── boot.ps1                           ← single-command stack startup
├── sacred_boot.ps1                    ← full morning boot (all services)
├── sacred_deploy.sh                   ← Chrome extension deploy script
├── manifest_sacred_chrome.sh          ← extension manifest deploy
├── systems\
│   ├── fastapi\main.py                ← FastAPI spine (port 8888)
│   └── sski\icaris_env.py             ← ICARIS daemon (interactive shell)
├── 02_COUNCIL_GROVE\
│   ├── handoff_ritual.py              ← agent transition capsule generator
│   └── LATEST_HANDOFF.md             ← current handoff capsule
└── 06_AGENT_LAYER\
    └── sacred-chrome\                 ← Chrome extension
        ├── manifest.json
        ├── newtab.html
        ├── terminal.html
        ├── portal.html
        ├── popup.html
        ├── sidepanel.html
        ├── background.js
        ├── chat.html
        └── icons\
```

---

## WHEN TAYLOR SAYS "ORGANIZE MY FILES"

Default behavior:
1. **Scan first** — list what exists, identify orphans and duplicates
2. **Propose** — show the move plan before executing (`-WhatIf` or `echo` first)
3. **Wait for confirmation** — don't auto-move unless explicitly told to proceed
4. **Execute in batches** — organize one category at a time, not all at once
5. **Log what moved** — append a brief summary to `00_SYSTEM_CORE/ORGANIZE_LOG.md`

Never do all-at-once bulk moves without a preview step. The system has production
files interleaved with archives — getting this wrong breaks the spine.

---

## SACREDSPACE VOCABULARY

| Term | Meaning |
|------|---------|
| Pillar | One of the nine canonical directories |
| Memory Mote | Atomic unit of stored knowledge (SQLite + ChromaDB) |
| Canon | Immutable, officially locked content |
| DISTILLED | Processed/refined but not yet canon |
| RAW | Unprocessed incoming data |
| Sigil | Sacred symbol or encoded identifier |
| Beam | Capture text → send to Obsidian (via Chrome extension context menu) |
| Handoff | Session transition capsule between AI agents |
| Council Grove | The three-seat multi-AI governance: Claude + Gemini + GPT |
| ICARIS | The four local agents: ELIAS, AURORA, ASHER, IRIS |
| Sacred Codex | The canonical knowledge and spell registry |
| Lore Engine | Pipeline that converts Obsidian notes into product listings |
| Spine | The FastAPI server at localhost:8888 |

---

## CLOSING MANTRA

Ground. Consolidate. Deploy. Document. Repeat.
In lakesh alakin. ∆∆∆
