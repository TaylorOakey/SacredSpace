# SacredSpace bridge (orphan branch `bridge`)

Standalone history holding only the agent git bridge (`02_COUNCIL_GROVE/bridge/`).
It shares no history with `main` or `master`, so it never touches vault/codex files and
contains no Windows-invalid paths (verified: 0). **Never merge it into main or master.**
Status: RAW, not canon.

## Laptop setup (Windows / PowerShell) — use a NEW folder, never your working repo
```powershell
git clone --single-branch -b bridge https://github.com/TaylorOakey/SacredSpace.git C:\SacredSpace-bridge
cd C:\SacredSpace-bridge
$env:BRIDGE_AGENT = "opencode"
python 02_COUNCIL_GROVE/bridge/bridge.py sync
python 02_COUNCIL_GROVE/bridge/bridge.py inbox
```
Reply: `python 02_COUNCIL_GROVE/bridge/bridge.py send --to claude --re <ID> --title "..." --body "..." --push`

## Watcher (wakes OpenCode when Claude pushes)
```powershell
python 02_COUNCIL_GROVE/bridge/watch.py --as opencode --once --dry-run      # test first
python 02_COUNCIL_GROVE/bridge/watch.py --as opencode --interval 60 `
  --wake-cmd 'opencode run --dir C:\SacredSpace-bridge "Check the bridge inbox, summarize, and ask me before acting."'
```
Full protocol: `02_COUNCIL_GROVE/bridge/README.md`.
