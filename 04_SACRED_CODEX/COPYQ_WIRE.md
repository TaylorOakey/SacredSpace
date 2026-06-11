## CopyQ Integration

**Pillar:** 02_COUNCIL_GROVE (primary)
**Owner Agent:** AURORA
**Status:** Scripts deployed — awaiting Windows binary install
**Deployed:** 2026-06-09

**Purpose:** Clipboard manager wired into SacredSpace OS as clipboard infrastructure layer

**Inputs:** Any clipboard text; Python calls via copyq_bridge.py; FastAPI POST requests; WSL2 shell aliases

**Outputs:** Pillar-routed tab storage; SACREDTAG-stamped clips; flush files to FORGE_OUTPUT

**Dependencies:**
- CopyQ portable — `D:\SacredSpace_OS\02_COUNCIL_GROVE\tools\copyq\copyq.exe` (manual install required)
- `02_COUNCIL_GROVE/scripts/copyq_bridge.py`
- `02_COUNCIL_GROVE/scripts/copyq_routes.py`
- FastAPI spine :8888 (optional, mount copyq_router with prefix="/copyq")

**Tab Map:**

| Tab | Pillar(s) |
|-----|-----------|
| FORGE | Active session / working buffer |
| CODEX | 04 — Canon text, spells, rituals |
| VAULT | 01, 06 — Obsidian-bound clips |
| COUNCIL | 02, 03 — Prompts, AI outputs, cross-agent context |
| MARKET | 07, 09 — Social posts, listings |
| LEARNING | 08 — Study notes, code snippets |
| MEMORY | 05 — Memory Mote candidates |
| INBOX | Raw catch-all (default capture tab) |

**WSL2 Aliases (in ~/.bashrc):**
```bash
export COPYQ_WIN="/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/tools/copyq/copyq.exe"
alias copyq="$COPYQ_WIN"
copyq_push() { echo "$1" | "$COPYQ_WIN" add -; }
copyq_read() { "$COPYQ_WIN" clipboard; }
```

**Notes:** WSL2 calls Windows binary via /mnt/d path. Spine routes require copyq_router mounted in main.py.
