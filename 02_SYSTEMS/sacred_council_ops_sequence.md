---
title: Sacred Council Drive Operations Sequence
pillar: 02_SYSTEMS
x_source_pillar: 02_SYSTEMS
status: Active
version: 1.0.0
reviewed: 2026-06-11
reviewer: Taylor (The Forge — VALEN closure pass)
---

# Sacred Council Drive Operations Sequence
## D1 → D6 Repeatable Ritual

This document codifies the six Drive operations as a repeatable council ritual.
Run in order. Never skip. Never reverse.

---

## Pre-Flight Check (before D1)

Before beginning any Drive operation session:

- [ ] Confirm `sacred_watcher.py` is running and healthy
- [ ] Confirm `mission_state.json` reflects current active mission
- [ ] Confirm no documents carry `Status: LOCKED` in the target pillars
- [ ] Confirm Taylor has review availability before D2 executes (audit needs approval)
- [ ] Open `watcher_conflicts.log` and resolve any pending conflicts from prior session

**Council seat assignments:**
- D1 Audit → ELIAS (Deep Well / Gemini deep research)
- D2 Pillar Mapping → AURORA (Anvil / execution)
- D3 Cloud Root Build → AURORA (Anvil / execution)
- D4 NotebookLM Alignment → ELIAS (Deep Well) + Claude (Forge review)
- D5 Template Creation → The Forge (Claude / narrative + design)
- D6 Skill Spec & Watcher Integration → The Forge (Claude) + The Sacred Smith (Desktop)

---

## D1 · Drive Audit

**Purpose:** Inventory the full Drive root before touching anything.
**Owner:** ELIAS
**Output:** Google Sheet in `02_SYSTEMS/AUDITS/`

### Steps

1. ELIAS lists all files and folders in `SacredSpace_OS_CLOUD/`
2. For each item, record:
   - Current path
   - Assigned canonical pillar (01–09) or "Orphan"
   - Protection status (CANON, sigil-marked, or unprotected)
   - `X-Source-Pillar` header value if present
   - Mismatch flag if X-Source-Pillar ≠ actual path
3. Flag duplicates (same name, same modified date) → park in `_DUPLICATES/` under their pillar
4. Flag orphans → list two candidate pillars with rationale. Taylor adjudicates.
5. Output as Sheet: `File Name | Current Path | Assigned Pillar | X-Source-Pillar | Protection | Mismatch | Notes`

**Hard rules:**
- Do NOT move or delete anything during D1
- Do NOT confirm NotebookLM sources without checking the Sources panel
- Orphan adjudication must come from Taylor, never silently resolved

**Gate:** Taylor reviews and approves the audit sheet before D2 begins.

---

## D2 · Pillar Mapping

**Purpose:** Execute approved moves from D1 audit. Consolidate competing master folders.
**Owner:** AURORA
**Prerequisite:** Taylor-approved D1 audit sheet

### Steps

1. Diff competing master folders (Feb 2026 vs. all earlier versions)
   - Rescue unique content from older versions
   - Archive older versions to `_ARCHIVE/PRE-CLOUD-MIGRATION/`
   - Never delete originals — always archive first
2. Execute moves from approved audit sheet
3. Disputed placements → `_PENDING_REVIEW/[pillar]/` subfolder. Never force a placement.
4. Write `Status: LOCKED` to any document being moved. Remove lock after move confirmed.
5. Verify `X-Source-Pillar` header matches new location after each move

**Hard rules:**
- Canonical nine pillar names only — reject any invented labels
- If external AI (Gemini, ChatGPT) returns invented labels, remap before proceeding
- Never delete. Propose, move, archive — in that order only.

---

## D3 · Cloud Root Construction

**Purpose:** Build or verify the full `SacredSpace_OS_CLOUD` folder tree.
**Owner:** AURORA

### Required structure

```
SacredSpace_OS_CLOUD/
├── 01_CORE/
│   └── COMMAND/           ← mission_state.json sync target
├── 02_SYSTEMS/
│   ├── AUDITS/            ← D1 audit sheets live here
│   └── CONFIGS/           ← sacred_watcher_config.json, notebook_routing.json
├── 03_NEURAL/
├── 04_CODEX/
│   └── LORE/              ← LORE.VAULT notebook source
├── 05_MEMORY/
├── 06_AGENTS/             ← ICARIS Quartet prompt docs (with lock protocol)
├── 07_SOCIAL/
│   ├── CREATION_LAB/      ← merchant.py output drop zone (CREATION.LAB source)
│   └── SIGNAL/            ← SACRED.SIGNAL notebook source
├── 08_LEARNING/
│   └── RESEARCH/          ← KNOWLEDGE.VAULT notebook source
├── 09_MARKET/
├── _PERSONAL/
│   └── NOTEBOOKLM_SAFE/   ← FAMILY.LEGACY notebook source (ONLY subfolder that NLM touches)
│       ├── Sacred_Messages_Iris/
│       └── Sacred_Messages_Asher/
└── _ARCHIVE/
    └── PRE-CLOUD-MIGRATION/
```

**Steps:**
1. Create all folders listed above (empty structure first — no files)
2. Verify `_PERSONAL/` root is not auto-sync enabled
3. Verify `_PERSONAL/NOTEBOOKLM_SAFE/` is the ONLY _PERSONAL subfolder with NotebookLM access
4. Place `sacred_watcher_config.json` and `notebook_routing.json` in `02_SYSTEMS/CONFIGS/`
5. Place this document in `02_SYSTEMS/`

---

## D4 · NotebookLM Alignment

**Purpose:** Cross-reference Drive folders against eight Sacred Notebooks. Confirm sources.
**Owner:** ELIAS (audit) + Claude (review)

### Routing verification table

| Notebook | Source Path | Auto-Sync | Manual Only |
|---|---|---|---|
| SACRED.CORE | 04_CODEX/ | Yes | No |
| LORE.VAULT | 04_CODEX/LORE/ | Yes | No |
| GAME.SYSTEMS | 03_NEURAL/ | Yes | No |
| KNOWLEDGE.VAULT | 08_LEARNING/RESEARCH/ | Yes | No |
| FAMILY.LEGACY | _PERSONAL/NOTEBOOKLM_SAFE/ | No | Yes — Taylor only |
| CREATION.LAB | 07_SOCIAL/CREATION_LAB/ | Yes | No |
| SACRED.SIGNAL | 07_SOCIAL/SIGNAL/ | Yes | No |
| SACRED.MARKET | 09_MARKET/ | Yes | No |

### Steps

1. Open each NotebookLM notebook. Check Sources panel.
2. For each source, verify it matches the routing table above
3. Flag any source pointing to wrong pillar → remove and re-add from correct path
4. Flag any notebook with zero sources → list which documents need to be created
5. Flag any Drive file present in pillar but not sourced by any notebook → candidate for addition

**Hard rule:** Never duplicate a file in two pillars to satisfy two notebook routes. Fix the route.

---

## D5 · Sacred Void Template Creation

**Purpose:** Create or refresh the four standing Google Docs templates.
**Owner:** The Forge (Claude)

### Sacred Void brand spec

| Token | Hex |
|---|---|
| Void | #1A1233 |
| Signal | #7F77DD |
| Grove | #1D9E75 |
| Flame | #D85A30 |
| Amber | #FAC775 |
| Ash | #B4B2A9 |

**Typography:** Cinzel or Playfair Display (headings) · Lora (body)

### Required header block (every template)

```
SΔCR3DSPΔCE OS
Pillar: [PILLAR_NAME]
X-Source-Pillar: [CANONICAL_PILLAR_ID]
Status: Draft / Active / Canon / LOCKED
Version: v[N]
```

### Four standing templates

| Template | Destination Pillar | Status |
|---|---|---|
| Council Session Log | 02_SYSTEMS | Create if missing |
| Canon Entry Form | 04_CODEX | Create if missing |
| Sacred Mission Brief | 01_CORE | Create if missing |
| Creative Drop Zone Intake | 07_SOCIAL/CREATION_LAB | Create if missing |

### Steps

1. Check each pillar for existing template versions
2. Diff against spec above — update header block if missing X-Source-Pillar field
3. Create any missing templates as V2 (with full header block)
4. Store each template in its destination pillar folder with naming:
   `TEMPLATE — [TYPE] — [NAME] — v[N]`

---

## D6 · Skill Spec & Watcher Integration

**Purpose:** Verify watcher is wired to the new Drive structure. Update skill spec.
**Owner:** The Forge (Claude) + The Sacred Smith (Desktop)

### Steps

1. Confirm `sacred_watcher_config.json` paths match D3 folder tree (no drift)
2. Confirm `notebook_routing.json` paths match D4 verification (no drift)
3. Run watcher smoke test: create a test file in `02_SYSTEMS/`, confirm it is detected and cloud path resolved correctly, then delete test file
4. Confirm `never_ingest` patterns are active — test with a file named `test.env`, confirm it is blocked and logged to `watcher_security.log`
5. Confirm lock protocol is active — write `Status: LOCKED` to a test doc header, confirm watcher skips it and adds to `locked_queue`
6. Update `sacredspace-gdrive SKILL.md` with any architectural changes from this session
7. Produce session close entry in Council Session Log template

### Watcher integration snippet (reference)

```python
import json
from pathlib import Path

CONFIG = Path("D:/SacredSpace_OS/01_CORE/COMMAND/sacred_watcher_config.json")
STATE  = Path("D:/SacredSpace_OS/01_CORE/COMMAND/mission_state.json")

def get_config() -> dict:
    return json.loads(CONFIG.read_text()) if CONFIG.exists() else {}

def get_mission_tags() -> list[str]:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text()).get("context_tags", [])
        except Exception:
            return []
    return []

def is_never_ingest(filepath: str, config: dict) -> bool:
    """Return True if file matches any never_ingest pattern."""
    from fnmatch import fnmatch
    patterns = config.get("never_ingest", [])
    return any(fnmatch(filepath, p) for p in patterns)

def is_locked(filepath: str) -> bool:
    """Return True if file header contains Status: LOCKED."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            head = [next(f) for _ in range(10)]
        return any("Status: LOCKED" in line for line in head)
    except Exception:
        return False

def should_ingest(filepath: str, file_tags: list[str], config: dict) -> bool:
    """Full ingest gate: security check → lock check → mission tag check."""
    if is_never_ingest(filepath, config):
        _log_security(filepath)
        return False
    if is_locked(filepath):
        _log_locked(filepath)
        return False
    mission_tags = get_mission_tags()
    if not mission_tags:
        return True  # open ingestion when no active mission
    return bool(set(file_tags) & set(mission_tags))

def _log_security(filepath: str):
    with open("watcher_security.log", "a") as f:
        f.write(f"BLOCKED: {filepath}\n")

def _log_locked(filepath: str):
    with open("watcher_locked_queue.json", "a") as f:
        f.write(f"{filepath}\n")
```

---

## Post-Session Checklist

After D6 completes:

- [ ] All audit sheets saved to `02_SYSTEMS/AUDITS/`
- [ ] `_PENDING_REVIEW/` reviewed and adjudicated by Taylor
- [ ] Watcher smoke test passed
- [ ] `watcher_conflicts.log` is clean
- [ ] `watcher_security.log` reviewed for unexpected blocks
- [ ] All templates in correct pillar folders
- [ ] Council Session Log entry written and saved to `02_SYSTEMS/`
- [ ] This document promoted to `Status: Canon` in Drive if no changes needed

---

## Hard Constraints (always active, every operation)

1. Never delete any file. Propose moves. Taylor executes.
2. Never invent pillar labels. Canonical nine only.
3. Never modify files marked `Status: Canon` or bearing SΔCR3DSPΔCE sigil.
4. Never duplicate files across pillars to satisfy routing — fix the route.
5. Never source a NotebookLM notebook without verifying the Sources panel.
6. Never auto-sync `_PERSONAL/` root — NOTEBOOKLM_SAFE subfolder only.
7. Never ingest files matching `never_ingest` patterns — log to security log only.
8. Never overwrite a `Status: LOCKED` document — add to locked queue, retry in 15 min.

---

*In lakesh alakin. Δ*
