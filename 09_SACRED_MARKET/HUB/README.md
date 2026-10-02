# ∆ Business Hub

**The one place to look** for everything SacredSpace has written about cash flow, business, nonprofit and grants, marketing, branding and culture.

| File | What it is | Who writes it |
|---|---|---|
| `INDEX.md` | The hub: a ledger snapshot, recent changes, then one section per topic linking to every matching document | `tools/hub_build.py` (automatic) |
| `index.json` | The same data for agents (Claude, OpenCode, a future `/merchant/hub` route) | automatic |
| `hub_config.json` | Which folders are scanned, and the keywords that define each topic | you |
| `RESEARCH_LEXICON.md` | Keywords, terms, tools, funders and search strings for research | you + the loop |
| `PROMPT_OPENCODE_INSTALL.md` | Paste-in prompt: OpenCode installs, checks and schedules the hub on the Legion | — |

## How it works
- The hub **links** to documents where they live. It never copies or moves them, so each original stays the single source of truth and the hub can't go stale.
- **What it scans:** this repo, `D:\SacredSpace_OS`, both vault locations, and `~/sacredspace*`. It reads the vault but never writes to it.
- **What it skips:** private folders (`_PERSONAL`, `Messages_*`, `NOTEBOOKLM_SAFE`), the 140 GB archive, and `.git`/`.obsidian`.
- **Scoring:** a keyword in a file's name counts 6 (`filename_weight`), and each distinct keyword in its text counts 1. A file belongs to its highest-scoring topic. It is also listed under any other topic that scores at least half as high.
- **What it reads:**
  - `.md`, `.txt` and `.html` files are read in full.
  - PDFs, Word files, spreadsheets and slides are matched by filename only.
  - Files with identical content are folded into one entry.
- **Money snapshot:** the header shows First Flame progress, net income, expenses, cash position and grants due within 30 days. These come live from `merchant.db`, opened read-only.
- `INDEX.md` and `index.json` are **gitignored**, because on the Legion they include vault note titles and first lines. In a cloud session, rebuild them with `--roots .` to cover this repo only.

## Keeping it updated
The hub runs under **Windows Python** or **WSL** Python. Roots in the config can be written either way (`D:/...` or `/mnt/d/...`); each is translated for whichever Python runs it.

**Windows scheduled task (recommended on the Legion).** It sees C: and D: even when WSL is closed or can't mount D:. It uses `pythonw` so no console window flashes. Run in PowerShell, adjusting the path if the repo isn't at `D:\SacredSpace_OS`:
```powershell
schtasks /create /tn "SacredSpace Hub" /sc hourly /mo 3 /tr "pythonw D:\SacredSpace_OS\09_SACRED_MARKET\tools\hub_build.py"
schtasks /run /tn "SacredSpace Hub"      # test it now
schtasks /delete /tn "SacredSpace Hub"   # stop
```
A full scan takes about 6 minutes (≈22k files), so every 3 hours is the default.

**WSL cron (alternative).** It only works while WSL is up, the cron service is running and D: is mounted:
```bash
bash 09_SACRED_MARKET/tools/install_hub_cron.sh            # every 3 h + at WSL start
bash 09_SACRED_MARKET/tools/install_hub_cron.sh --remove   # stop
```
**Rebuild by hand any time:** `python3 09_SACRED_MARKET/tools/hub_build.py` (or `py` on Windows).

**Private or machine-only settings** go in `HUB/hub_config.local.json`, which is gitignored and never committed. Its lists extend the shared config and its single values override it:
```json
{ "skip_dirs": ["PRIVATE_FOLDER_NAME"], "roots": ["G:/My Drive"] }
```

**Google Drive:** if Drive for desktop is installed, add its folder to `roots` in `hub_config.local.json` (e.g. `G:/My Drive`, whatever the real drive letter is), and Drive files join the hub too.

**Reading it in Obsidian:** build a copy into the vault. Writing into the vault is your call, so the command requires `--allow-vault`:
```bash
python3 09_SACRED_MARKET/tools/hub_build.py --out /mnt/d/01_VAULT/SacredSpace_Vault/09_SACRED_MARKET/HUB --allow-vault
```

## Tuning
- **A document lands in the wrong topic:** add or remove keywords for that topic in `hub_config.json`. Prefer phrases ("mission statement") to bare words ("mission"); bare words over-match.
- **A new topic** (e.g. `legal`, `events`): add a block under `domains`, and a new section appears on the next run.
- **Layer:** the hub is a RAW index. Promoting anything it surfaces into CANON still goes through the Canon Gate.
