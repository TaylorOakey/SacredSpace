---
title: "MIGRATION_PLAN"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/00_SACRED_SPINE/MIGRATION_PLAN.md"
keyword_count: 9
keywords_found: []
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 34
---

# SACREDSPACE MIGRATION PLAN
**Date:** 2026-05-21
**Status:** AWAITING TAYLOR CONFIRMATION — do not execute Phase 4+ without approval
**Canonical Truth:**
- ONE VAULT: `/mnt/d/01_VAULT/SacredSpace_Vault/`
- ONE OS ROOT: `/mnt/d/SacredSpace_OS/`

---

## EXECUTION PHASES

| Phase | Scope | Risk | Status |
|---|---|---|---|
| 1 | Create canonical vault folder structure | NONE (additive) | READY |
| 2 | Migrate D: root loose files to vault | LOW (8 files) | READY |
| 3 | Copy C: vault unique files to vault | LOW (6 files, originals stay) | READY |
| 4 | Copy SacredSpace_OS docs to vault | MEDIUM (mirror, no deletion) | NEEDS CONFIRMATION |
| 5 | Rename empty wrong-named vault folders | LOW | READY |
| 6 | SACREDSPACE_OS_2026 content review | HIGH (102GB, 331 .md files) | TAYLOR DECISION |
| 7 | Setup auto-routing (aliases, config) | NONE (additive) | READY |

---

## PHASE 1 — Create Canonical Vault Structure
**Risk: NONE. Creates missing directories only.**

```bash
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"
for PILLAR in \
  "00_SACRED_SPINE" "01_OBSIDIAN_VAULTS" "02_COUNCIL_GROVE" \
  "03_NEURAL_FOREST" "04_SACRED_CODEX" "05_MEMORY_ENGINE" \
  "06_AGENT_LAYER" "07_SOCIAL_MOTHERSHIP" "08_LEARNING_PATH" \
  "09_SACRED_MARKET" "ARCHIVE"; do
  mkdir -p "$VAULT/$PILLAR"
  echo "  ✓ $PILLAR"
done
# Sub-folders
mkdir -p "$VAULT/04_SACRED_CODEX/lore"
mkdir -p "$VAULT/04_SACRED_CODEX/CODE_CANON/entries"
echo "✓ Phase 1 complete"
```

---

## PHASE 2 — Migrate D: Root Loose Files
**Risk: LOW. These are clearly orphaned — no matching file exists in vault.**

```bash
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"

# 00_SACRED_SPINE
cp "/mnt/d/SACREDTAG_PROTOCOL.md" "$VAULT/00_SACRED_SPINE/SACREDTAG_PROTOCOL.md"
ls -la "$VAULT/00_SACRED_SPINE/SACREDTAG_PROTOCOL.md" && \
  rm "/mnt/d/SACREDTAG_PROTOCOL.md" && echo "  ✓ SACREDTAG_PROTOCOL.md"

# 03_NEURAL_FOREST (NotebookLM upload kit)
cp "/mnt/d/LORE_VAULT_upload_kit.md" "$VAULT/03_NEURAL_FOREST/LORE_VAULT_upload_kit.md"
ls -la "$VAULT/03_NEURAL_FOREST/LORE_VAULT_upload_kit.md" && \
  rm "/mnt/d/LORE_VAULT_upload_kit.md" && echo "  ✓ LORE_VAULT_upload_kit.md"

# 04_SACRED_CODEX/lore (Jenga's Journey)
cp "/mnt/d/jengas_journey_chapters_1_2.md" "$VAULT/04_SACRED_CODEX/lore/jengas_journey_chapters_1_2.md"
ls -la "$VAULT/04_SACRED_CODEX/lore/jengas_journey_chapters_1_2.md" && \
  rm "/mnt/d/jengas_journey_chapters_1_2.md" && echo "  ✓ jengas_journey_chapters_1_2.md"

cp "/mnt/d/jengas_journey_chapter_3.md" "$VAULT/04_SACRED_CODEX/lore/jengas_journey_chapter_3.md"
ls -la "$VAULT/04_SACRED_CODEX/lore/jengas_journey_chapter_3.md" && \
  rm "/mnt/d/jengas_journey_chapter_3.md" && echo "  ✓ jengas_journey_chapter_3.md"

# 08_LEARNING_PATH
cp "/mnt/d/SACREDCODEX_Invocation_Ledger_v3.md" "$VAULT/08_LEARNING_PATH/SACREDCODEX_Invocation_Ledger_v3.md"
ls -la "$VAULT/08_LEARNING_PATH/SACREDCODEX_Invocation_Ledger_v3.md" && \
  rm "/mnt/d/SACREDCODEX_Invocation_Ledger_v3.md" && echo "  ✓ SACREDCODEX_Invocation_Ledger_v3.md"

# ARCHIVE (completed mission briefs + duplicate)
cp "/mnt/d/HERMES_MOUNT.md" "$VAULT/ARCHIVE/HERMES_MOUNT.md"
ls -la "$VAULT/ARCHIVE/HERMES_MOUNT.md" && \
  rm "/mnt/d/HERMES_MOUNT.md" && echo "  ✓ HERMES_MOUNT.md → ARCHIVE"

cp "/mnt/d/HERMES_WIRE.md" "$VAULT/ARCHIVE/HERMES_WIRE.md"
ls -la "$VAULT/ARCHIVE/HERMES_WIRE.md" && \
  rm "/mnt/d/HERMES_WIRE.md" && echo "  ✓ HERMES_WIRE.md → ARCHIVE"

cp "/mnt/d/LORE_VAULT_upload_kit(1).md" "$VAULT/ARCHIVE/LORE_VAULT_upload_kit_duplicate.md"
ls -la "$VAULT/ARCHIVE/LORE_VAULT_upload_kit_duplicate.md" && \
  rm "/mnt/d/LORE_VAULT_upload_kit(1).md" && echo "  ✓ LORE_VAULT_upload_kit(1).md → ARCHIVE"

echo "✓ Phase 2 complete"
```

**Note:** `/mnt/d/SACREDSPACE_AUDIT.md` — left at D: root (this is the active audit doc).

---

## PHASE 3 — Copy C: Vault Unique Files to D: Vault
**Risk: LOW. COPY only — originals stay on C: until confirmed.**

```bash
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"
C_VAULT="/mnt/c/01_OBSIDIAN_VAULTS/SacredSpace_Vault"

# Lore poems (test1–4 contain real lore content despite "test" names)
for t in test1 test2 test3 test4; do
  cp "$C_VAULT/$t.md" "$VAULT/04_SACRED_CODEX/lore/$t.md"
  ls -la "$VAULT/04_SACRED_CODEX/lore/$t.md" && echo "  ✓ $t.md → 04_SACRED_CODEX/lore/"
done

# Archive items
mkdir -p "$VAULT/ARCHIVE/c_vault_imports"
cp "$C_VAULT/01_Chats/Imported/test_chat.md" "$VAULT/ARCHIVE/c_vault_imports/test_chat.md"
echo "  ✓ test_chat.md → ARCHIVE"

# NOTE: .obsidian/ configs NOT touched — Obsidian manages these
# NOTE: 02_Ideas/ content is IDENTICAL between C: and D: — skipped
# NOTE: Untitled.canvas — skipped (empty Obsidian canvas, no content to preserve)

echo "✓ Phase 3 complete"
```

---

## PHASE 4 — Mirror SacredSpace_OS Docs to Vault
**Risk: MEDIUM. COPY only — originals stay in OS. Requires Taylor confirmation.**
**Reason for confirmation: these docs live in the code root and may be actively referenced by CLAUDE.md paths.**

```bash
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"
OS="/mnt/d/SacredSpace_OS"

# 00_SACRED_SPINE
cp "$OS/04_SACRED_CODEX/SACREDSPACE_PROJECT_INSTRUCTIONS.md" "$VAULT/00_SACRED_SPINE/"
cp "$OS/04_SACRED_CODEX/SacredSpace_OS_Architecture_v1_1.md" "$VAULT/00_SACRED_SPINE/"
echo "  ✓ 00_SACRED_SPINE: 2 files"

# 02_COUNCIL_GROVE
cp "$OS/04_SACRED_CODEX/SACREDSPACE_COMPLETE_COUNCIL_SYNTHESIS.md" "$VAULT/02_COUNCIL_GROVE/"
cp "$OS/02_COUNCIL_GROVE/HANDOFFS/HANDOFF_02_SYSTEMS_2026-05-15_002643.md" "$VAULT/02_COUNCIL_GROVE/HANDOFFS/" 2>/dev/null || true
cp "$OS/02_COUNCIL_GROVE/LATEST_HANDOFF.md" "$VAULT/02_COUNCIL_GROVE/" 2>/dev/null || true
echo "  ✓ 02_COUNCIL_GROVE: 3 files"

# 06_AGENT_LAYER
cp "$OS/04_SACRED_CODEX/HERMES_AGENT_INTEGRATION.md" "$VAULT/06_AGENT_LAYER/"
cp "$OS/04_SACRED_CODEX/agents/HERMES.md" "$VAULT/06_AGENT_LAYER/"
cp "$OS/04_SACRED_CODEX/agents/THRICEGREAT.md" "$VAULT/06_AGENT_LAYER/"
cp "$OS/04_SACRED_CODEX/tools.md" "$VAULT/06_AGENT_LAYER/"
cp "$OS/AGENTS.md" "$VAULT/06_AGENT_LAYER/"
echo "  ✓ 06_AGENT_LAYER: 5 files"

# 08_LEARNING_PATH
cp "$OS/04_SACRED_CODEX/SACREDCODEX_Invocation_Ledger_v2.md" "$VAULT/08_LEARNING_PATH/"
echo "  ✓ 08_LEARNING_PATH: 1 file"

# 09_SACRED_MARKET
cp "$OS/09_SACRED_MARKET/SacredSpace_Revenue_Operations.md" "$VAULT/09_SACRED_MARKET/"
echo "  ✓ 09_SACRED_MARKET: 1 file"

# ARCHIVE
cp "$OS/RECONCILE_INSTRUCTION.md" "$VAULT/ARCHIVE/" 2>/dev/null || true
cp "$OS/_INBOX/CLAUDE_CODE_MISSION_BRIEF.md" "$VAULT/ARCHIVE/" 2>/dev/null || true
cp "$OS/archive/GENESIS_REPORT_MARCH_2026.md" "$VAULT/ARCHIVE/" 2>/dev/null || true
echo "  ✓ ARCHIVE: 3 files"

# SACREDSPACE_MASTER_CONTEXT — resolve version conflict first
# Current: vault version (4088b) = OS version (4088b) < DISTILLED version (4603b)
# ACTION: update vault with DISTILLED (newer) version
cp "$OS/04_SACRED_CODEX/DISTILLED/SACREDSPACE_MASTER_CONTEXT.md" "$VAULT/04_SACRED_CODEX/SACREDSPACE_MASTER_CONTEXT.md"
echo "  ✓ SACREDSPACE_MASTER_CONTEXT updated to DISTILLED version"

echo "✓ Phase 4 complete"
```

**SKIPPED (Taylor decision needed):**
- `04_SACRED_CODEX/CODE_CANON/` (9 files) — closely tied to code structure; mirror to vault?
- `04_SACRED_CODEX/DISTILLED/` (14 files) — large batch; review for vault-worthy content
- `03_NEURAL_FOREST/skills/` — skill .md files; mirror to vault/03_NEURAL_FOREST/?

---

## PHASE 5 — Rename Empty Wrong-Named Vault Folders
**Risk: LOW. All these folders are confirmed empty. Moving empty dirs.**

```bash
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"

# These are empty old-style folders — remove after creating canonical names
for old in "01_CORE" "02_SYSTEMS" "03_NEURAL" "04_CODEX" \
           "05_MEMORY" "06_AGENTS" "07_SOCIAL" "08_LEARNING" \
           "09_MARKET" "_ARCHIVE"; do
  if [ -d "$VAULT/$old" ]; then
    count=$(find "$VAULT/$old" -type f 2>/dev/null | wc -l)
    if [ "$count" -eq 0 ]; then
      rmdir "$VAULT/$old" && echo "  ✓ Removed empty: $old"
    else
      echo "  ⚠ $old has $count files — skipping, needs manual review"
    fi
  fi
done

# _PERSONAL has no canonical equivalent — flag for Taylor
echo "  · _PERSONAL: left in place — no canonical pillar mapping. Taylor: keep or move to ARCHIVE?"

echo "✓ Phase 5 complete"
```

---

## PHASE 6 — SACREDSPACE_OS_2026 (TAYLOR DECISION)
**Risk: HIGH. 102GB, 331 real .md files. Do NOT auto-migrate.**

### What was found:
- `/mnt/d/SACREDSPACE_OS_2026/` — 102GB total (mostly .venv bloat inside `06_AGENT_LAYER/interfaces/sigil_magic_coder/.venv`)
- Contains a COMPLETE nine-pillar structure (older version of SacredSpace OS)
- Includes: old Obsidian vault, exported chat history, legacy Python codebase, sacredspace_ritual_deck
- Also found: `/mnt/d/SACREDSPACE_OS_2026/00_SYSTEM_CORE/.env` — **DO NOT COPY** (may contain API keys)

### Taylor needs to decide:
1. Should we extract the 331 .md files from SACREDSPACE_OS_2026 to the canonical vault?
2. Should the SACREDSPACE_OS_2026 itself be kept, archived, or deleted?
3. Should we extract `sacredspace_ritual_deck_v3.2__history.json` to the vault?

### Safe extraction command (if Taylor says yes):
```bash
# Extract only .md files, excluding venv, git, and temp dirs
DEST="/mnt/d/01_VAULT/SacredSpace_Vault/ARCHIVE/sacredspace_os_2026_docs"
mkdir -p "$DEST"
find /mnt/d/SACREDSPACE_OS_2026 \
  -name "*.md" \
  -not -path "*/.venv/*" \
  -not -path "*/venv/*" \
  -not -path "*/.git/*" \
  -not -path "*/site-packages/*" \
  2>/dev/null | while read f; do
    rel=$(echo "$f" | sed 's|/mnt/d/SACREDSPACE_OS_2026/||')
    dest_dir="$DEST/$(dirname "$rel")"
    mkdir -p "$dest_dir"
    cp "$f" "$dest_dir/"
done
echo "Done. Review $DEST before deciding what to promote to active pillars."
```

---

## PHASE 7 — Setup Auto-Routing
**Risk: NONE. Additive only.**

### 7a — Bash aliases in ~/.bashrc

```bash
cat >> ~/.bashrc << 'BASHEOF'

# ─── SACREDSPACE PATH ROUTING ─────────────────────────────
export SACRED_VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"
export SACRED_OS="/mnt/d/SacredSpace_OS"
export SACRED_SPINE="$SACRED_VAULT/00_SACRED_SPINE"
export SACRED_CODEX="$SACRED_VAULT/04_SACRED_CODEX"
export SACRED_GROVE="$SACRED_VAULT/02_COUNCIL_GROVE"
export SACRED_AGENTS="$SACRED_OS/systems/fastapi"

alias vault="cd $SACRED_VAULT"
alias spine="cd $SACRED_SPINE"
alias codex="cd $SACRED_CODEX"
alias grove="cd $SACRED_GROVE"
alias agents="cd $SACRED_AGENTS"
alias obscheck="bash $SACRED_OS/02_COUNCIL_GROVE/check_obsidian.sh"

sacred_note() {
  PILLAR="${1:-04_SACRED_CODEX}"
  NAME="${2:-note_$(date +%Y%m%d_%H%M%S)}"
  FILE="$SACRED_VAULT/$PILLAR/$NAME.md"
  mkdir -p "$(dirname $FILE)"
  echo "# $NAME" > "$FILE"
  echo "**Created:** $(date)" >> "$FILE"
  echo "**Pillar:** $PILLAR" >> "$FILE"
  echo ""
  echo "✓ Created: $FILE"
}
# ──────────────────────────────────────────────────────────
BASHEOF
source ~/.bashrc
echo "✓ Aliases loaded"
```

### 7b — SACRED_ROUTER.md
Written to: `/mnt/d/01_VAULT/SacredSpace_Vault/00_SACRED_SPINE/SACRED_ROUTER.md`

### 7c — sacred_router.json
Written to: `/mnt/d/SacredSpace_OS/.claude/sacred_router.json`

---

## OPEN CONFLICTS REQUIRING TAYLOR DECISION

| # | Conflict | Options |
|---|---|---|
| 1 | `SACREDSPACE_MASTER_CONTEXT.md` — 3 versions (vault=OS < DISTILLED) | Use DISTILLED as canonical (already in Phase 4 plan) |
| 2 | `test1.md`–`test4.md` — named "test" but contain real lore | Migrate as lore (Phase 3 plan) OR leave on C: if these are scratch |
| 3 | `_PERSONAL/` folder in vault — no canonical pillar | Rename to `10_PERSONAL/` or move to `ARCHIVE/` |
| 4 | `CODE_CANON/` docs in OS root | Mirror to vault `04_SACRED_CODEX/CODE_CANON/` or keep OS-only |
| 5 | `SACREDSPACE_OS_2026/` — 102GB archive | Extract .md files to ARCHIVE?, keep whole, or delete? |

---

## WHAT IS NOT BEING MIGRATED

| Location | Reason |
|---|---|
| `/mnt/d/SacredSpace_OS/**/*.py` | Code stays in OS root — routing law |
| `C:/02_Ideas/.obsidian/` | Never touch `.obsidian/` plugin configs |
| `D:/01_VAULT/.obsidian/` | Never touch `.obsidian/` plugin configs |
| `SACREDSPACE_OS_2026/.env` | May contain API keys — DO NOT COPY |
| `SACREDSPACE_OS_2026/**/.venv/` | Package directories — not content |
| `/mnt/d/SACREDSPACE_AUDIT.md` | This audit doc — leave at D: root |

---

## SUCCESS CRITERIA (from SACREDSPACE_AUDIT.md)

- [ ] Audit report → 00_SACRED_SPINE/AUDIT_REPORT.md **DONE**
- [ ] Migration plan → 00_SACRED_SPINE/MIGRATION_PLAN.md **DONE**
- [ ] All nine pillar folders exist in canonical vault (Phase 1)
- [ ] Orphaned files migrated (Phases 2–3)
- [ ] SACRED_ROUTER.md → 00_SACRED_SPINE/ (Phase 7b)
- [ ] sacred_router.json → .claude/ (Phase 7c)
- [ ] Bash aliases loaded (Phase 7a)
- [ ] ChromaDB sync attempted (Phase 6 in audit doc — after migration)
- [ ] UNIFICATION_COMPLETE.md written
- [ ] Taylor decisions: _PERSONAL, CODE_CANON, DISTILLED, SACREDSPACE_OS_2026

---

*ELIAS analysis complete. Ready for AURORA execution on Taylor confirmation.*
*In lakesh alakin. ∆*
