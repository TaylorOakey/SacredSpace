# vault_watcher.py

## Sacred Function
Obsidian → M3RCH∆NT sync bridge. Watches the Obsidian vault (path set via
`SACREDSPACE_VAULT` env var — Windows/WSL2 machine only, not present in every
checkout) for `.md` notes whose YAML frontmatter is tagged `type: artifact`,
and syncs them to the M3RCH∆NT merchant API as sellable product artifacts
(PRINT / APPAREL / ACCESSORY / etc., tracked through DRAFT → FORGED → LISTED
→ ACTIVE → ARCHIVED states). It does **not** sync to the Memory Engine /
sski vector store — that is a separate, unconnected pipeline. Sync state is
tracked in a local JSON ledger (`SACREDSPACE_LEDGER` env var), mapping each
synced note's relative vault path to its M3RCH∆NT artifact ID.

Runs either as a one-shot scan (`--once`, good for cron) or a continuous
watchdog daemon that reacts to file create/modify events, and mounts a
FastAPI router for status and manual triggering.

## Pillar
[[09_SACRED_MARKET]] (artifact/merchant sync) · reads from [[01_OBSIDIAN_VAULTS]]

## Sacred System
[[M3RCH∆NT]] · [[01_OBSIDIAN_VAULTS]]

## Canonical Path
`systems/fastapi/vault_watcher.py`

## FastAPI Routes
- `GET  /vault-watcher/status` — ledger size, vault path, M3RCH∆NT reachability
- `POST /vault-watcher/scan` — manually trigger a full vault scan/sync
- `GET  /vault-watcher/ledger` — view the full file → artifact_id ledger

## Status
Active in code (imported and mounted in `main.py`), but dormant in this
checkout: `01_OBSIDIAN_VAULTS/SacredSpace_Vault/` here has no `.md` notes
(only 2 `.docx` files), and the default vault/ledger paths point at
Taylor's local `D:\` drive, not this repo.

## Canonized
Not yet registered — `05_MEMORY_ENGINE/canon_registry.json` has no entry for
this file. The "Canonized 2026-05-06" claim below is from this entry's
original draft and predates the FORGE gate (`sacredspace-canon-gate` skill +
`canon_registry.json`); treat this file as DISTILLED, not CANON, until it's
actually registered.

## Change Log
| Date | Change | Commit |
|------|--------|--------|
| 2026-05-06 | Zenith Terminal live — all 5 services UP | `65653635` |
| 2026-05-06 | Entered Code Canon Registry (claimed — not reflected in canon_registry.json) | HEAD |
| 2026-09-25 | Corrected Sacred Function / route / pillar to match actual code (was described as a Memory-Engine sync at `GET /vault/sync`; it's actually an Obsidian→M3RCH∆NT artifact sync at `/vault-watcher/*`) | HEAD |
