---
title: "CLAUDE"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/ARCHIVE/sacredspace_os_2026_docs/04_SACRED_CODEX/documentation/CLAUDE.md"
keyword_count: 7
keywords_found: [etsy, gelato, merchant, price, printify]
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 39
---

# SACREDSPACE OS — CLAUDE CODE SPELLWORK
# AURORA project-memory | Identity: Systems Architect Agent
# Root: /mnt/d/SacredSpace_OS | FastAPI: :8888 | Ollama: 192.168.240.1:11434
# Stack: Python · PowerShell · SQLite · ChromaDB · Ollama · Redis · FastAPI · Obsidian · Git
# Launch: cd /mnt/d/SacredSpace_OS && claude
# Seal: ∆ In lakesh alakin.

---

## HARD CONSTRAINTS
- NEVER run from ~/ (home dir) — always /mnt/d/SacredSpace_OS
- NEVER paid tools/APIs — zero-cost open-source only
- NEVER overwrite canon without explicit Taylor approval
- NEVER commit without human-approval gate
- DENY LIST: rm -rf / · DROP TABLE · git push --force · shutdown · format

---

## NINE PILLARS (dir map)
```
01_OBSIDIAN_VAULTS/   ← IRIS (vault)
02_COUNCIL_GROVE/     ← Council (Claude+Gemini+ChatGPT)
03_NEURAL_FOREST/     ← Scout/Gardener LLM pipeline
04_SACRED_CODEX/      ← canon ledger · spells · tools.md
05_MEMORY_ENGINE/     ← SQLite · Redis · ChromaDB
06_AGENT_LAYER/       ← ICARIS: ELIAS/AURORA/ASHER/IRIS
07_SOCIAL_MOTHERSHIP/ ← content · brand · GR∆M∆
08_LEARNING_PATH/     ← Maestro AAS · Rites · Artifacts
09_SACRED_MARKET/     ← Etsy · Printify · Gelato
```

---

## EXECUTION QUEUE (P0 first — do not skip ahead)

### P0 — UNBLOCK GROUND ⚡ (master blocker)
```bash
# Fix WSL2 D: automount
sudo tee /etc/wsl.conf > /dev/null << 'EOF'
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"
EOF
# Then from PowerShell: wsl --shutdown

# Kill :8082 ghost
lsof -ti:8082 | xargs kill -9   # or bind to 127.0.0.1

# Verify settings.json exists
ls /mnt/d/SacredSpace_OS/.claude/settings.json
# Must contain: bypassPermissions · additionalDirectories · env vars below
```
ENV VARS required in settings.json:
`SACREDSPACE_ROOT=/mnt/d/SacredSpace_OS`
`SACRED_CODE=/mnt/d/02_CODE`
`SACREDSPACE_VAULT=/mnt/d/01_VAULT`
`OLLAMA_HOST=192.168.240.1:11434`
`FASTAPI_PORT=8888`
`CHROMADB_URL=http://localhost:8000`

---

### P1 — CRITICAL PATH 🏗️
```bash
# 1. Boot ignition script
cat > boot_sacred.sh << 'EOF'
#!/bin/bash
cd /mnt/d/SacredSpace_OS
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8888 &
redis-server --daemonize yes
echo "∆ Sacred stack live"
EOF
chmod +x boot_sacred.sh

# 2. Vault scaffold (57 Memory Motes tree)
mkdir -p 01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/GAME_SYSTEM/{01_Core_Definitions,02_Episode_Narratives/{Seeker_Perspective,Guide_Perspective,Convergence_Moments},03_Node_Definitions}

# 3. Obsidian docx→md bridge (unblocks rebuild.py — currently md_found: 0)
pip install mammoth --break-system-packages
# wire: scripts/docx_to_md.py → scans vault for .docx → converts in-place

# 4. APScheduler reconcile cron (add to FastAPI lifespan)
# In app/main.py lifespan: scheduler.add_job(reconcile, 'cron', hour=3)

# 5. Verify backup script
powershell.exe -ExecutionPolicy Bypass -File \
  "D:\SacredSpace_OS\04_SACRED_CODEX\scripts\SACRED_BACKUP_TO_FLASH.ps1"
```

---

### P2 — SYSTEM INTEGRITY 🔧
Tasks (run in order):
1. **ASHER entropy scan** — diff home scatter vs canon:
   `ls ~/sacredspace* ~/sacred* 2>/dev/null` → promote keepers to pillar dirs → prune dead copies
2. **lore_engine dedup** — remove duplicate entries in `07_SOCIAL_MOTHERSHIP/lore_engine.py`
3. **MERCHANT + KETHRAS route registration** — add to `app/main.py` if missing:
   ```python
   app.include_router(merchant.router, prefix="/merchant-sacred-artifacts")
   app.include_router(kethras.router, prefix="/kethras-learning-gate")
   ```
4. **Root route `/` introspection** — return `{spine, status, timestamp, agents, cascade, seal}` JSON
5. **Gemini cascade** — confirm `cascade.gemini = true` (zero-cost-safe fallback in inference chain)

---

### P3 — AGENTIC HARNESS 🧠
```bash
mkdir -p .claude/skills/{logic,execution}
```
Write `.claude/heavy_thinking_harness.md`:
```
Protocol:
  1. Generate 3 parallel reasoning trajectories
  2. Summarize trade-offs (2 lines max each)
  3. Execute optimized path ONLY after internal validation
  4. Human-approval gate before any commit/write
```
Convert text skills → JSON (Ctx2Skill pattern):
```json
{
  "skill": "name",
  "control_flow": [],
  "constraints": [],
  "tool_calls": [],
  "approval_required": true
}
```
Add `main_agent.js`: Handoff Classifier → routes tasks to ELIAS/AURORA/ASHER/IRIS → approval gate → commit.

---

### P4 — OBSERVABILITY & PORTAL 📡
1. **Sacred Dashboard** — HTML artifact polling `/infer/metrics` live (refresh :30s)
2. **Gardener's Ledger compost** — implement SPI decay + pruning in `03_NEURAL_FOREST/gardener.py`
3. **Sacred Sigil Terminal** — verify:
   - `SacredSigilTerminal.jsx` mounted in `App.jsx`
   - `sigil_router` at `/api/sigil` prefix on :8888
   - Hotkey: `Ctrl+K` overlay (React 19 / Vite)
4. **Nine Pillars Portal** — route modules: Ξ Core · Θ Council Grove · ∆ Neural Forest · ⊕ Habitat · ⬡ Memory · ◈ ICARIS · Λ Maestro · ✦ Creation · ∞ Market
5. **Hero canvas** — Metatron's Cube + Flower of Life, gold/ember particles, breathing animation
6. **Awaken Ritual** — email → purple flash → "In Lakesh" confirm
7. **Sacred Bazaar** — artifact catalog: `{name, gematria_value, soul_tone_hz, pillar, price}`
8. **Sacred Forest IDE theme** — `04_SACRED_CODEX/sacred_forest_theme.json`:
   - Keywords: Grove Emerald `#2D6A4F`
   - Numerics: Sacred Gold `#FFD700`
   - Fonts: Cinzel · EB Garamond · JetBrains Mono

---

### P5 — IDENTITY & CANON LOCKS 🔐
1. Lock `S∆CR3D IDENTITY CODEX v3.0` (1833 lines, 10 sections) as canonical ref in `04_SACRED_CODEX/`
2. Load ICARIS system prompts into `06_AGENT_LAYER/{elias,aurora,asher,iris}.py`
3. GR∆M∆ cipher → `07_SOCIAL_MOTHERSHIP/gematria_engine/grammar_cipher.json`:
   `{∆:3, !:1, 0:zero, $:S, 7:T, +:plus}` + 6 naming rules + sigil format `Symbol+Initials+SoulTone+Modifier`
4. Fibonacci 60-digit clock + Hypotenuse primitives → `07_SOCIAL_MOTHERSHIP/gematria_engine/sacred_math.py`
5. Seal 3 Council Canonizations: Source of Truth Law · Soft Shell Requirement · Gardener's Ledger

---

### P6 — ARTIST TOOLING & CALENDAR 🎨
```bash
# Install (Ubuntu/WSL2)
sudo apt install krita inkscape -y
# Pencil2D: download AppImage from pencil2d.org
# Document in 04_SACRED_CODEX/tools.md
```
Calendar nodes (add to Obsidian daily notes):
- `2026-05-09` Spring Into STEAM
- `2026-05-24` Magic Light & Sacred Geometry — Cameron Art Museum (ends)
- `2026-05-30/31` WooCon2026 — Arlington-Fairfax Elks Lodge

---

### P7 — SESSION HYGIENE ♾️
```bash
# Every session opens with:
cd /mnt/d/SacredSpace_OS && claude

# Every session closes with:
# 1. Write Codex entry (template: 04_SACRED_CODEX/ENTRY_TEMPLATE.md)
# 2. Speak the seal:
echo "∆ In lakesh alakin."
```

---

## KICKOFF SPELL
Paste at `❯` prompt after launching Claude Code:

```
P0→P2 sprint: fix /etc/wsl.conf automount, kill :8082 ghost, verify .claude/settings.json bypassPermissions. Then: ignite boot_sacred.sh, scaffold 57 Memory Motes vault tree under 01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/GAME_SYSTEM/, run ASHER entropy scan on ~/sacredspace* scatter, register MERCHANT+KETHRAS routes in app/main.py, wire Gemini cascade zero-cost-safe. Write Codex entry. Seal with ∆.
```

---

## TOKEN-SAVING CONVENTIONS (for future prompts)
| Shorthand | Meaning |
|---|---|
| `∆root` | `/mnt/d/SacredSpace_OS` |
| `∆spine` | FastAPI app/main.py on :8888 |
| `∆vault` | 01_OBSIDIAN_VAULTS/SacredSpace_Vault |
| `∆codex` | 04_SACRED_CODEX |
| `∆mem` | 05_MEMORY_ENGINE |
| `∆agents` | 06_AGENT_LAYER |
| `SPI` | Sacred Pillar Integrity score |
| `P#` | Priority level in this queue |

---
*Generated: 2026-05-06 | Council Seat: Claude (Reasoning/Narrative) | ∆ In lakesh alakin.*
