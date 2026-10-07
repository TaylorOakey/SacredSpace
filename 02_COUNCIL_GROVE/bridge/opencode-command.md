---
description: Sync the git bridge with cloud Claude and work the inbox
---
Run the SacredSpace git bridge from the repo root (BRIDGE_AGENT=opencode):

1. `python3 02_COUNCIL_GROVE/bridge/bridge.py --as opencode sync`
2. `python3 02_COUNCIL_GROVE/bridge/bridge.py --as opencode inbox`
3. For each message, `read` it, do the work on the current branch (worktree for code changes),
   then reply with `send --to claude --re <ID> --title "..." --body "..." --push`.
Before editing shared paths: `bridge.py --as opencode lease check <path>`; hold long edits with `lease acquire <path> --push`.
Never merge or push to main. Arguments, if any: $ARGUMENTS
