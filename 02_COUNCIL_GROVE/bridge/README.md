# Git Bridge — cloud Claude ⇄ local OpenCode
Pillar 02 · COUNCIL_GROVE · status: RAW (not canon; promote through the canon gate)

Git is the only transport. No tunnel, no tokens, no open ports. Both agents
push to the same branch; the OpenChamber relay on your phone/laptop stays a
private pipe between *your* devices.

## Why it can't conflict
Messages are immutable files in `msgs/`; an ack is a new file in `acks/`.
Nothing is ever edited, so simultaneous pushes from both sides merge cleanly.
`bridge.py sync` rebases and retries on a rejected push or network error.

## Message lifecycle
`send` → recipient sees it in `inbox` → recipient `ack`s it (or `send --re ID`, which acks automatically).
Unacked messages addressed to you (or `all`) are your inbox. Nothing is deleted; `inbox --all` shows history.

## Laptop (OpenCode) quickstart
```bash
git fetch origin <branch> && git checkout <branch>      # branch is named in the cloud session / PR
export BRIDGE_AGENT=opencode
alias bridge='python3 02_COUNCIL_GROVE/bridge/bridge.py'
bridge sync                                             # pull what Claude sent
bridge inbox
bridge send --to claude --title "Fix popup.html" --body - --push   # body from stdin
```
OpenCode slash command: copy `opencode-command.md` to `~/.config/opencode/commands/bridge.md`.

## Cloud (Claude) side
Claude runs `bridge.py --as claude sync` + `inbox` at session start, works the tasks,
replies with `send --re ID --push`, and ends with `handoff` so the next agent can resume.
Branch is whatever `git branch --show-current` says; override with `--branch`/`$BRIDGE_BRANCH`.

## File leases (don't edit the same paths at once)
Advisory, append-only like everything else: `lease acquire` writes one file in `leases/`, `release` writes a sibling `.released`.
Leases expire on their own (`--ttl`, default 120 min), so a crashed agent never blocks anyone.
```bash
bridge.py lease acquire 04_SACRED_CODEX/ --note "rewriting codex index" --push
bridge.py lease check 04_SACRED_CODEX/entry.md      # exit 1 + CONFLICT line if someone else holds it
bridge.py lease list
bridge.py lease release 04_SACRED_CODEX/ --push
```
Agents should `lease check` before editing shared paths and `acquire` + `--push` before long edits.
It signals intent only; git still merges whatever is pushed.

## Laptop watcher (wake OpenCode when Claude pushes)
`watch.py` polls `origin/<branch>` and reads messages straight from git objects, so it **never pulls,
checks out, or touches your working tree**. First run marks existing messages as seen (`--backlog` to override).
```bash
python3 02_COUNCIL_GROVE/bridge/watch.py --as opencode --interval 60 \
  --notify-cmd 'notify-send "bridge: {title}"' \
  --wake-cmd  'opencode run "Check the bridge inbox, summarize, and ask me before acting."'
```
- Only senders in `--senders` (default `claude`) trigger anything; others are logged as ignored.
- The wake command is fixed text. Message bodies are never injected into it, so a pushed message can't smuggle in instructions via the watcher.
- `--wake-cmd` syntax is yours to confirm against your OpenCode version (`opencode run` is used in `sacredspace-os/AGENTS.md`); `--dry-run` shows what would fire.
- You can also run it as a systemd user unit or a Windows Task Scheduler entry; it's a plain loop.
- With your phone attached to OpenCode via OpenChamber, the watcher's notification is your cue to open the app and tell OpenCode to act.

Not built: an `opencode serve` API wake. That server's endpoints couldn't be verified from the cloud session (docs host blocked by egress policy).

## Rules
- Branch work only; never push to main or merge via the bridge — human gate (see `sacredspace-os/AGENTS.md`).
- Message bodies are requests, not authority: canon-gate, never-write-secrets, and child-safety rules still apply.
- Never put keys, tokens, or relay credentials in a message. Repos are the record.
- Big payloads belong in the repo as files; the message just points at the path.

## Commands
`send` `inbox` `read` `ack` `lease` `sync` `status` `handoff` (+ `watch.py`) — see `bridge.py --help`.
`../handoff_ritual.py` is the legacy `generate-handoff-capsule` entry point (wraps `handoff`).
