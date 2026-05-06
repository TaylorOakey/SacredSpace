# vault_watcher.py

## Sacred Function
Obsidian vault monitor and sync daemon. Watches `/mnt/d/01_VAULT/SacredSpace_Vault/` for file changes, triggers reconciliation with the SQLite memory layer, and keeps the vault's 176+ notes in sync with the Memory Engine. Exposed via `GET /vault/sync` on the FastAPI spine.

## Pillar
[[05_MEMORY_ENGINE]]

## Sacred System
[[Memory Engine]] · [[01_OBSIDIAN_VAULTS]]

## Canonical Path
`systems/fastapi/vault_watcher.py`

## FastAPI Route
`GET /vault/sync`

## Status
Active

## Canonized
2026-05-06 · Commit: `65653635`

## Change Log
| Date | Change | Commit |
|------|--------|--------|
| 2026-05-06 | Zenith Terminal live — all 5 services UP | `65653635` |
| 2026-05-06 | Entered Code Canon Registry | HEAD |
