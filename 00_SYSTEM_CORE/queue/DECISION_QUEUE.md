---
title: "DECISION QUEUE — Mission 04-SCAFFOLD Phase 0"
source: "Workstream 2 ASHER graveyard — read-only log"
created: 2026-08-29
status: pending — no rulings attempted
---

# DECISION QUEUE (Phase 0 — logged, not resolved)

> ASHER role: log conflicts, do not resolve. No consolidation, no architecture choice. All items pending VALEN/AURORA/Taylor at CHECKPOINT 3 or File-Org D0/D1/D2 gate.

## DQ-01 — CONFLICT-16 (pending)
- **Status:** logged, unresolved
- **Context:** Referenced in Phase 0 brief as a conflict to log but not resolve. No new information added here. Retained as named placeholder per mission constraints.
- **Action:** Route to CHECKPOINT 3 review. No resolution attempted.

## DQ-02 — Elara / Fable5 Naming Collision (pending)
- **Status:** logged, unresolved
- **Context:** Mission 04-SCAFFOLD notes "Mission 03/OSTack remains unconfirmed — reconcile both against SACRED_LEDGER session log on next cleanup, not blocking this." Elara and Fable5 appear in same naming contention set as OSTack-adjacent candidates. No source file on disk declares a winner; both remain candidate strings in chat/Drive exports.
- **Action:** Do not pick. Record both as candidate aliases pending Taylor's Word (Seal 5). Candidate location: `05_MEMORY_ENGINE/akashic_bridge/` alias table (future) — not written now.

## DQ-03 — OSTack Write-Path (pending)
- **Status:** logged, unresolved
- **Context:** Competing write-path definitions for OSTack/SacredStack/Mission Control: (a) `PILLAR_ROOT=/mnt/c` (SacredSpine `sacred_spine.py:580`), (b) `PULSE_DB_DIR` env-overridable (`/mnt/c/06_AGENT_LAYER/pulse_events/` `pulse_server.py`), (c) Akashic Bridge `catalog.db` as THE catalog target (`/mnt/c/05_MEMORY_ENGINE/akashic_bridge/catalog.db`), (d) `05_MEMORY_ENGINE/vector_store` vs file-based ChromaDB. `FILE_ORG_PHASE1_PLAN.md` S3 documents move-impact per service; all write-paths gated on endpoint before/after inventory.
- **Action:** No path chosen. Preserved as checklist for File-Org Phase 1 D0/D1/D2 rulings + AURORA Fusion. All writes remain read-only in Phase 0.

## DQ-04 — Four Pipeline Definitions Overlap (side-by-side, no ruling)
- **Status:** logged, explicitly *not* reconciled here per "no ruling" constraint
- **Context:** Graveyard S2 lays the four definitions verbatim (SKC 9-stage vs Multi-Source 6-layer vs PEE 8-step vs SSKI 10-module). Reconciliation designated for AURORA Fusion at CHECKPOINT 3.

## DQ-05 — Pillar Canon Divergence (D0) — `06_AGENT_LAYER` vs `06_AGENT_GROVE`
- **Status:** logged, from `FILE_ORG_PHASE1_PLAN.md` S0. Disk HERE says `06_AGENT_LAYER`; Hermes on other device reported `06_AGENT_GROVE`. Gated on user ruling before any DB write.

## DQ-06 — `02_SYSTEMS` Collision (D1)
- **Status:** logged. C:\ has both `02_COUNCIL_GROVE` and `02_SYSTEMS`. Unknown if `02_SYSTEMS` is a real pillar or mis-named dup of `00_SYSTEM_CORE`.

## DQ-07 — Sacred Phoenix Authorization (D2)
- **Status:** logged. No prior artifact; if authorized as unified-interface rebuild, starts at RAW per File-Org S2. Default: deferred.

## DQ-08 — Storyline Board Primacy: 9×9 vs 12×12 (resolved by PR — pending ratification)
- **Status:** resolved by landed PR `claude/sacred-arcana-game-data-fih0uo` @ `2eaf7ad0` (2026-08-18); awaiting Taylor's ratification
- **Context:** `_Sacred_Storyline_Canon.md` Part V asserted "12×12 Vector Grid — not 9×9, not hexagonal"; a later chat correction said both coexist as layers. The PR's §0 item 4 resolves it as an *engineering*, not canon, split: a **9×9 tactical board** (`04_SACRED_CODEX/game/arcana_board.py` — encounter placement / Throne seeding) layered under a **12×12 vector grid** (`game/grid.py` — Node Wells / Ley Lines / Flow Shapers) for the Confluence phase. Source: `arcana_board.py:562` — *"Why 9×9 and not 12×12 — an engineering ruling, NOT a canon ruling."* Machine-readable: `09_SACRED_MARKET/arcana_grid/game_data.json` → `board_resolution`. The unrelated 7×7/9×9 "Blueprint" quadrant sample is explicitly a separate draft.
- **Action:** No outstanding doc/code conflict. Route to Taylor for ratification or amendment. Do not re-open as a conflict.

## DQ-09 — Five Primal Spirit Paths Set Divergence (partially resolved — residual inconsistency)
- **Status:** open — the PR resolved the *naming* but not its *document body*
- **Context:** Two incompatible five-fold sets: (a) **Seer / Warrior / Heart / Guardian / Shapeshifter** (Deep Innerstanding §VII; used for character assignments), vs (b) **Wanderer / Healer / Builder / Seeker / Weaver** (`_Sacred_Storyline_Canon.md` Part V, attributed SESSION-016). The PR's §0 item 6 and "Open Reconciliation Items" #2 declare **(b) canonical** (*"Wanderer/Healer/Builder/Seeker/Weaver… confirmed"*). **But the PR's own body still uses (a):** `SACRED_STORYLINE_CANON.md` §8 (lines 147–162) and §11 (line 205) assign Seer/Warrior/Heart/Guardian/Shapeshifter, and `09_SACRED_MARKET/arcana_grid/game_data.json` → `five_primal_spirit_paths` still carries Shapeshifter/Heart/Guardian/Warrior/Seer values. Also open: whether the five Paths map onto the Grid's 4 Elements × 3 Primes or run as an independent axis.
- **Action:** Fix `SACRED_STORYLINE_CANON.md` §8/§11 and `game_data.json` to the canonical (b) set — or, if (a) is intended for characters and (b) for the system axis, state that split explicitly. Then route to Taylor. Do not pick silently.

---

Logged: 2026-08-29 by ASHER (read-only) — no rulings attempted. Next: AURORA Fusion at CHECKPOINT 3.

Logged: 2026-09-11 by opencode (read-only reconciliation pass against PR `claude/sacred-arcana-game-data-fih0uo` @ `2eaf7ad0`) — DQ-08/DQ-09 logged; no Taylor ruling attempted.
