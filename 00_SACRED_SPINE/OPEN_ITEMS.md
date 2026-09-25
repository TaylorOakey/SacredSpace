# SacredSpace — Open Items Tracker
**Date:** 2026-09-25
**Sources:** Data Unification Work Order (2026-09-17) + Architect session (2026-09-23)
**Maintained by:** Update after each session; archive completed items to 04_SACRED_CODEX/

---

## LEGEND
`✓ DONE` · `⚡ SOLVED HERE` · `🔴 BLOCKED` · `🟡 NEEDS TAYLOR` · `⬜ OPEN`

---

## PHASE 0 — FOUNDATION (start here, no dependencies)

| # | Item | Status | Notes |
|---|---|---|---|
| A7 | **Spine :8888 down** | 🔴 OPEN | Refused connection 2026-09-23. Run `boot_sacred.sh` from Legion WSL. |
| P0a | Fix `/etc/wsl.conf` automount + `wsl --shutdown` | ⬜ OPEN | CLAUDE.md P0 item. |
| P0b | Kill :8082 ghost: `lsof -ti:8082 \| xargs kill -9` | ⬜ OPEN | CLAUDE.md P0 item. |
| F0 | **Index Rootbook into Akashic** | ⬜ OPEN | Zero hits in Akashic. Run `sacred_ingest_core.py` against Rootbook path once located. |

---

## PHASE 1 — DECISIONS (Taylor's word required)

| # | Item | Status | Notes |
|---|---|---|---|
| A6 | **Pillars-as-schema ruling (DQ-11)** | 🟡 TAYLOR | Proposal: keep 9-pillar filesystem + add semantic channel tags (ledger/rootbook/sigil/notebooklm). Check DECISION_QUEUE.md first — may already be covered by DQ-01 through DQ-10. |
| D1 | **Item 13: 3-way palette conflict** | 🟡 TAYLOR | Earthy (repo) vs V∆SH∆ freq vs new sacred-codex-design. Recommend option (d): three scopes — repo-earthy for OS chrome, V∆SH∆ for ritual/game, codex-skill for publishing. Needs Seal-5. |
| D2 | **Rootbook canonical location** | 🟡 TAYLOR | Where does Rootbook live? Once confirmed, index it (F0 above). |

---

## PHASE 2 — RECONCILIATION (after Phase 1 decisions)

| # | Item | Status | Notes |
|---|---|---|---|
| R1 | **C:/D: mirror drift check** | ⬜ OPEN | C:\ is canonical (DQ-10). Run `rsync --dry-run -av /mnt/c/SacredSpace_OS/ /mnt/d/SacredSpace_OS/` to surface drift. Session 141 already found+fixed one divergence — drift is recurring. |
| R2 | **Resolve dual-naming** | ⬜ OPEN | C:\ has both `02_COUNCIL_GROVE` and `02_SYSTEMS`; `04_CODEX` vs `04_SACRED_CODEX`. Resolve once canonical tree confirmed. |
| R3 | **D:\SACREDSPACE_ARCHIVE status** | ⬜ OPEN | Third pillar tree. Confirm: intentional snapshot or active duplication? Archive if snapshot. |

---

## PHASE 3 — CLOSE THE BACKLOG

| # | Item | Status | Notes |
|---|---|---|---|
| B1 | **Session 070 Phase 3 manual review (~720 items)** | ⬜ OPEN | Open since 2026-08-07. CANON_DECISIONS.md explicitly deferred these. Smaller now than it will ever be. |
| B2 | **Parse 4 remaining export categories** | ⚡ SOLVED | `claude_export_parser_v2.py` written. Run: `python claude_export_parser_v2.py --category all --input /path/to/export/ --output ./_RAW/` |

---

## PHASE 4 — FINISH TODAY'S EXPORT

| # | Item | Status | Notes |
|---|---|---|---|
| E1 | **Parse projects.json** | ⚡ READY | Parser v2 handles this. |
| E2 | **Parse memories.json** | ⚡ READY | Parser v2 handles this. |
| E3 | **Parse design_chats.json** | ⚡ READY | Parser v2 handles this. |
| E4 | **Parse frames.json** | ⚡ READY | Parser v2 handles this. New category — saved Claude Artifacts. |
| E5 | **Link 720 conversations → Map of Content** | ⬜ OPEN | claude_sessions_2026-09-17.zip extracted. Next: build MOC in Obsidian. |

---

## PHASE 5 — HARVEST ADDITIONAL SOURCES

| # | Item | Status | Notes |
|---|---|---|---|
| H1 | **OpenCode sessions (144 sessions / 14,700 msgs)** | ⬜ OPEN | `dump_all_sessions.py` already exists. Run it. Export-20260910/ (652-session count) unverified — locate before trusting. |
| H2 | **VS Code / Copilot Chat (24 workspaceStorage entries)** | ⬜ OPEN | No harvest script yet. Key dirs: D:\ root (~190KB), sski (~214KB), sacredspace.code-workspace (~161KB). |
| H3 | **Google Takeout archives (D:\Takeout_Download\)** | ⬜ OPEN | Several hundred GB. Use `sacredspace-gdrive` skill — not a new script. Needs file-type triage pass first. |
| H4 | **GitHub vault repo** | ✓ DONE | TaylorOakey/SacredSpace-Vault, 2,070+ files, PR #1 merged. |

---

## PHASE 6 — HYPERLINK PASS

| # | Item | Status | Notes |
|---|---|---|---|
| X1 | **Cross-link full corpus** | ⬜ OPEN | End state. Depends on Phases 3–5 complete. |

---

## POLICY FILES — WRITTEN THIS SESSION

| File | Path |
|---|---|
| FORGE_RULES.yaml | `04_SACRED_CODEX/governance/FORGE_RULES.yaml` |
| registry_v1_1_0.sql | `05_MEMORY_ENGINE/migrations/registry_v1_1_0.sql` |
| claude_export_parser_v2.py | `04_SACRED_CODEX/scripts/claude_export_parser_v2.py` |

**Apply registry migration (Legion WSL):**
```bash
sqlite3 /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/omni_ledger.db \
  < /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/migrations/registry_v1_1_0.sql
```

---

## SEALED RULINGS (not open)

| Item | Ruling | Source |
|---|---|---|
| Canonical root | C:\ canonical; D:\ mirror | DQ-10 |
| Redis | Already removed — Pulse on SQLite | Architect confirmed |
| MCP tool count | 7 tools, not 31 | Architect confirmed |
| Memory hierarchy | Tier 1-6 + OpenHuman → RAW_CAPTURE | Architect ruling 2026-09-23 |
| Omni-ledger | v1.0.0 exists — v1.1.0 additive only | Architect ruling 2026-09-23 |

---

*In lakesh alakin. ∆*
