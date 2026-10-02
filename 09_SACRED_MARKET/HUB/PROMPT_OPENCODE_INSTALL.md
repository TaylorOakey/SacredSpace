# TASK: install the SacredSpace Business Hub (local, Legion / WSL2)

You are OpenCode working on Taylor's machine. Goal: install and schedule the Business Hub, then check what it finds. The hub is one auto-updated index of every cash-flow, business, nonprofit/grant, marketing, branding and culture document across the repo, D: and the Obsidian vault.

## Rules
- The Obsidian vault (`/mnt/d/01_VAULT/SacredSpace_Vault`, `/mnt/c/01_OBSIDIAN_VAULTS/...`) is read-only. Never pass `--allow-vault` unless Taylor says so in this session.
- Never commit `09_SACRED_MARKET/HUB/INDEX.md` or `index.json`. They are gitignored because they contain vault note titles. Check with `git status` before any commit.
- In your report, give counts and folder names only. No note titles and no file contents from the vault.
- Ask Taylor before creating any Windows scheduled task, changing `/etc/wsl.conf`, or committing anything.

## Steps
1. **Find the repo and get the code.** Find the SacredSpace clone. Check `/mnt/d/SacredSpace_OS` first, then `~/sacredspace*`, using `git remote -v`. Then:
   `git fetch origin && git checkout claude/sacred-marketplace-income-67t27a && git pull`
   Use `main` instead if PR #10 has been merged. Confirm these exist:
   - `09_SACRED_MARKET/tools/hub_build.py`
   - `09_SACRED_MARKET/tools/install_hub_cron.sh`
   - `09_SACRED_MARKET/HUB/hub_config.json`
2. **Check prerequisites.**
   - D: is mounted (`ls /mnt/d/`; if not, `sudo mkdir -p /mnt/d && sudo mount -t drvfs D: /mnt/d`).
   - `/usr/bin/python3` exists.
   - `crontab` is installed (`sudo apt install cron` if missing).
3. **Privacy check before the first scan.**
   - List the top-level folders of each root in `hub_config.json` → `roots`.
   - If any folder holds private material (family, kids' messages, health, household or insurance papers, the day job) and isn't already in `skip_dirs`, add its name to `skip_dirs` in your local copy.
   - Tell Taylor which names you added. Don't commit that change without their OK, because folder names can be revealing.
4. **Run it once.** From the repo root: `python3 09_SACRED_MARKET/tools/hub_build.py`
   - Record: roots scanned or skipped, files scanned, documents indexed, duplicates folded, run time (`time`), and whether the Ledger snapshot found `merchant.db`.
   - Open `09_SACRED_MARKET/HUB/INDEX.md` and check that the links resolve.
5. **Spot-check the topics.** For each of the 6 topics, look at the top 10 entries. Note any document that is clearly in the wrong topic. Report the folder and topic only, plus the keyword that probably caused the match (shown in the Keywords column).
6. **Schedule it.** Run `bash 09_SACRED_MARKET/tools/install_hub_cron.sh`, then:
   - Confirm with `crontab -l | grep sacredspace-business-hub`. You should see exactly 2 lines: the 3-hourly run and the `@reboot` run.
   - If cron isn't running: try `sudo service cron start`. If systemd is off (`ps -p 1 -o comm=` isn't `systemd`), tell Taylor that cron stops whenever WSL shuts down. Offer the two options from `09_SACRED_MARKET/HUB/README.md` and apply neither without a yes:
     - (a) enable systemd in `/etc/wsl.conf`
     - (b) the Windows `schtasks` line. Adjust its path if the repo isn't at `D:\SacredSpace_OS`.
   - Check the log after the first scheduled run: `tail ~/.sacred_hub.log`.
7. **Log it.** Append a short OpenCode entry to `09_SACRED_MARKET/RECURSION/ROUND_LOG.md`, using the template at the top of that file. Mark item 10 ✅ and include:
   - per-topic counts, scan time, and ledger found yes/no
   - which roots exist on this machine
   - topic mistakes and suggested keyword edits for `hub_config.json`
   - any `skip_dirs` additions (the names, for Taylor to approve)
   - cron status (running / needs systemd / Windows task chosen)

   Commit only `ROUND_LOG.md` and any `hub_config.json` change Taylor approved. Then push.

## Report back to Taylor (≤ 8 lines)
```
∆ HUB INSTALL — COMPLETE | BLOCKED
- Repo path · roots found · scanned / indexed / duplicates · run time
- Per-topic counts (cash flow / business / nonprofit / marketing / branding / culture)
- Ledger snapshot: found / not found
- Cron: installed + running | installed, needs systemd or a Windows task (your call)
- Topic mistakes → proposed keyword changes
- Privacy: skip_dirs added (awaiting OK) | none needed
- NEXT: one concrete action
```
