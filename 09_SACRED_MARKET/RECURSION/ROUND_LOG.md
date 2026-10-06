# ∆ ROUND LOG ∆ — Livelihood Loop
Append-only. Newest entry at the bottom. One entry per agent per round.

### Entry template
```
## Round N · <Claude Code | OpenCode> · YYYY-MM-DD
**Ladder rung:** <from GET /merchant/ledger, or "no sales yet">
**Done from last NEXT list:** ✅ / ⚠ (reason) / ↪ (reason) per item
**Verified / refuted:** <claims checked, with evidence>
**Ideas added:** <IDs> · **Re-scored:** <IDs + reason>
**Experiments:** <slot: status against kill metric>
**Notes for Taylor:** <≤ 3 lines>
**NEXT FOR <other agent>:**
1. …
```

---

## Round 0 · Claude Code · 2026-09-26
**Ladder rung:** no sales yet ($0). No listings live. Entity: `SOLE_PROP` default; the Taylor + Jeanie seller-of-record decision is open (IDEA_BANK E2).
**Done from last NEXT list:** n/a (first round).
**Verified / refuted (web, 2026-09-26):**
- Etsy allows readings delivered as a digital copy and bans outcome-promising metaphysical services ([policy](https://www.etsy.com/legal/prohibited/)).
- Etsy fees: $0.20 + 6.5% + 3% + $0.25. Ko-fi's free plan takes 5% on shop sales, plus a 5% "Contributor" fee unless switched off.
- Hugging Face CPU Gradio Spaces now need a paid plan, but static Spaces are free. So C2 has to be a static JS page.
- GitHub Sponsors charges 0% on personal-account sponsorships. [Quartz](https://github.com/jackyzha0/quartz) and [listmonk](https://github.com/knadh/listmonk) are active.
- Template sellers depend on having their own traffic, and email drives 40–60% of sales. That's why the C-lane scores high on audience even with a low revenue score.

**Ideas added:** A1–A8, B1–B4, C1–C5, D1–D3, E1–E2 (seeded from repo, Drive and web).
**Experiments:** Slot 1 First Flame is approved and not yet listed. Slots 2 (C2) and 3 (A4) are PROPOSED and need Taylor's yes.

**What "main income" takes (illustrative; the real target is Taylor's `TARGET_NET_MONTHLY`):** $1,000/month net would be roughly any one of these, or a mix:
- ~105 Mini Decodes
- ~51 Full Decodes
- ~40 template sales at $29 (after Gumroad's ~13% cut)
- ~163 members at $7 (Ko-fi free plan, Contributor off)

So no single $11 product replaces a paycheck. The route is **audience (C2, C3, C1) → several streams (A1, A4, C5) → one high-ticket service (B1) when time allows**. That's the order the experiments follow.

**Notes for Taylor:**
1. Say yes or no to experiments C2 and A4 (reply "C2 yes, A4 yes" or similar).
2. Set `TARGET_NET_MONTHLY` and `RUNWAY_MONTHS` (they can live in a local-only file).
3. The seller-of-record decision (E2) is still yours.

**NEXT FOR OPENCODE:**
1. **Spine check (plan I-5):** which `main.py` / `app/main.py` actually serves :8888, and does it mount `merchant.router`? If not, report the exact file and line where the router would go. Don't change the live spine without Taylor.
2. **Asset inventory (open-queue P2):** create `09_SACRED_MARKET/asset_inventory.md`. List every sellable image for the 8 design families plus the 2018–22 paintings, with path, pixel size, human-made vs. AI-assisted, and which listing it could fill (LISTINGS.md D1–D3, P1–P5).
3. **Archive mining:** parse the ChatGPT export (`chat.html`, Drive `ChatGPT_Export`, Dec 2025) with `chatgpt_export_parser.py`. List the 10 conversations with the most finished, sellable drafts (products, copy, templates, lore packs). Cite dates and titles only; don't commit the conversation text.
4. **Confirm local claims:** does the 54-card Arcana Grid JSON exist (path, card count)? (This gates A5.) Which parts of the vault could ship as a *de-personalised* template (A4) without anything private or canon-locked?
5. **Smoke test:** run `python3 09_SACRED_MARKET/FIRST_FLAME/grama_decode.py "Taylor Oakey" --tier mini`. Confirm it works on WSL2, and save the render (local only) as the listing demo.

## Round 0 addendum · Claude Code · 2026-09-26: `REVENUE_CONSOLIDATE.md` (uploaded by Taylor)
**Status:** it can't run from the cloud (this container has no D:/C: data; running it here would falsely report "complete" with 0 files). It moves to OpenCode's lane, but the original script was replaced with a hardened version first.
**Hardened:** `09_SACRED_MARKET/tools/revenue_consolidate.py` fixes Step 1 of the original:
- It writes a dry-run manifest by default and copies only with `--copy`.
- Keyword matching is whole-word ("pod" no longer matches "episode", "grant" no longer matches "granted").
- It skips the 140 GB `SACREDSPACE_ARCHIVE`, `_PERSONAL`, `NOTEBOOKLM_SAFE` and `Messages_*`.
- It folds duplicates by content hash, and copy names are collision-safe (the original let every `README.md` overwrite the last one).
- It refuses to write into the Obsidian vault without `--allow-vault`.

Tested on trap files and on this repo's 09 pillar: 127 scanned → 75 unique financial files, 30 duplicates folded.

**Problems found in the original Steps 2–5 (don't run them as written):**
- Step 2 calls `localhost:8888/drive/search`, and no such route exists. Drive was already searched read-only this session (see the plan and PR #10).
- Step 4 appends `revenue_query` to `hermes_mcp.py` using `_chroma_client`, `_ok` and `_err`. Confirm those helpers exist in the live file first. Add it only with Taylor's go-ahead, because it edits the live spine.
- Step 5 uses `chromadb.HttpClient(port=8001)`, but the June ledger says **ChromaDB is embedded and :8001 is OmniParse** (APP_STATUS lists "ChromaDB :8001 NOT CHECKED"). Verify which is true before ingesting. Also chunk the documents instead of embedding 200 KB dumps as single documents, and match the pillar name to the renamed `09_MARKET` if that rename is canon (plan I-6).
- Step 3 (`REVENUE_OPERATIONS_MASTER`): **Claude Code builds it next round, from OpenCode's manifest** plus the existing plan and IDEA_BANK, in Taylor's section template. It goes in the repo pillar, and into the vault only if Taylor says to canonize.

**NEXT FOR OPENCODE (added, item 6):**
6. On the Legion, run `python3 09_SACRED_MARKET/tools/revenue_consolidate.py` (dry run) and commit **only** `MANIFEST.md` (paths + keywords, no file contents) to `09_SACRED_MARKET/RECURSION/local_revenue_manifest.md`. First check that it contains no private paths or names. Report which of Steps 4–5 are safe, based on what the live spine and ChromaDB actually are.

## Round 1 · Claude Code · 2026-09-26
**Ladder rung:** no sales yet ($0).
**Done from last NEXT list:** n/a (Taylor's turn: "yes to both C2 and A4").
**Verified / refuted:**
- The JS engine in the C2 page matches `merchant.calculate_gematria`, `generate_sigil(AETHER)` and `grama_decode.sigilify`. Checked on 300+ names (hyphens, apostrophes, accents, `ß`, emoji, all soul tones 1–9/11/22): **0 mismatches**.
- The page renders at 360px wide with no horizontal scroll. A digits-only input hides the result.
- `SALE_CHANNELS` was missing `GUMROAD`, even though A4 and the fee table plan to sell there. Added.

**Ideas added:** none · **Re-scored:** none.
**Experiments:**
- Slot 1 First Flame: approved, not yet listed.
- Slot 2 **C2**: EXPERIMENT. `FIRST_FLAME/decode_web/index.html` is built and waiting for Taylor to publish it (see its README). The 60-day clock starts at publish.
- Slot 3 **A4**: EXPERIMENT. `A4_VAULT_TEMPLATE/SPEC.md` is written. The 60-day clock starts at launch.

**Notes for Taylor:**
1. C2 is ready to publish. Use a small separate public repo or an HF Static Space, **not** this repo. Fill in `SHOP` URLs once the Full and Deep listings exist.
2. Tag sales so the kill metrics can be counted: add `via:decode_web` or `sku:A4` in the ledger `notes`.
3. Still open: E2 seller of record, `TARGET_NET_MONTHLY`, `RUNWAY_MONTHS`.

**NEXT FOR OPENCODE** (items 1–6 from Round 0 still stand; these are added):
7. **A4 structure map:** write `RECURSION/local_vault_structure.md` with the live vault's folder tree (names and file counts only, no note titles in private areas). Mark each folder `structure` / `private` / `canon-locked`. This replaces Round 0 item 4b.
8. **A4 build:** build `SovereignCreatorVault/` as a **new vault from the spec**, outside the repo, then run the spec's leak check and report the grep output. Never copy files out of the live vault.
9. **C2 smoke test on WSL2:** open `decode_web/index.html?name=Taylor%20Oakey` in Chrome and confirm it matches `grama_decode.py "Taylor Oakey" --tier mini` (sum, tone, sigil).

## Round 1 addendum · Claude Code · 2026-09-27: Business Hub + Research Lexicon (asked for by Taylor)
**Built:**
- `tools/hub_build.py` builds one auto-updated index (`HUB/INDEX.md` + `index.json`) of every cash-flow, business, nonprofit/grant, marketing, brand and culture document across the repo, D: and the vault. It reads everything, copies nothing, and adds a live read-only ledger snapshot.
- `tools/install_hub_cron.sh` schedules the rebuild.
- `HUB/RESEARCH_LEXICON.md` is the research word list.

**Tested:**
- Repo run: 221 scanned, 81 indexed, 28 duplicates folded, in under 2 s.
- Test ledger: First Flame, net, expenses, cash position and due grants all match hand math.
- Private folders skipped; vault output refused without `--allow-vault`.
- Cron install is idempotent and `--remove` works.

**NEXT FOR OPENCODE (added):**
10. Install the hub by following `09_SACRED_MARKET/HUB/PROMPT_OPENCODE_INSTALL.md`. Short form: on the Legion, run `bash 09_SACRED_MARKET/tools/install_hub_cron.sh`. Report the per-topic document counts and the scan time (numbers only, no titles). List any document that landed in the wrong topic, so the keywords in `hub_config.json` can be tuned.

## Round 1 close · Claude Code · 2026-09-27: agenda for Claude's next round (set at Taylor's request)
**NEXT FOR CLAUDE (round 2):** web research only, with a URL for every claim. Focus: make the 3 live experiments launchable.
1. **First Flame listing evidence:**
   - Re-verify Etsy's digital-download and metaphysical-services rules, and the Etsy/Ko-fi fees behind the `FIRST_FLAME/LISTINGS.md` net table. Fix the table if anything moved.
   - Scan ~10 comparable "name meaning" / "name numerology" listings: price, format, review count.
   - Use them to find 3 long-tail keywords with demand and thin competition (Lexicon Q1). Rewrite the 13 tags if the evidence says so.
2. **C2 distribution:** find 3 communities where a free, private name-decode tool is welcome rather than spam, and record each one's self-promotion rule (Lexicon Q8). Confirm GitHub Pages and Hugging Face Static Space are still free for a single static page.
3. **A4 market:** find the price, bundle contents and visible traffic source of the top ~10 Obsidian vault/template sellers (Lexicon Q2). Check whether the Obsidian community or its forum restricts selling templates. Re-score A4 on that evidence.
4. **Grants & nonprofit:**
   - Which council administers the NC Artist Support Grant for Northampton County, and when is the next cycle (Lexicon Q3)? If it's open to individual artists, add it to the merchant grants pipeline as a proposed `POST /merchant/grants` body in the log (don't call any API).
   - Name 2–3 fiscal sponsors that would take an AI-literacy or family-storytelling project, with their fees (Lexicon Q4).
5. **Tax + lexicon upkeep:**
   - Find the source for NC sales tax on digital downloads sold outside Etsy (Ko-fi, Gumroad) (Lexicon Q5). Mark it "verify with an advisor".
   - In `HUB/RESEARCH_LEXICON.md`, resolve every *(verify)* item you checked, citing the date and URL. Add any new search terms that worked.
- **Deferred, conditional:** build `REVENUE_OPERATIONS_MASTER.md`, but **only if** OpenCode has committed `RECURSION/local_revenue_manifest.md` (Round 0 item 6). Otherwise mark it ↪.

## Round 1 · OpenCode · 2026-09-27 (relayed by Taylor; landed by Claude Code because OpenCode's tree was dirty)
**Ladder rung:** no sales yet ($0). No `merchant.db` exists yet (plan I-5 still open).
**Done from last NEXT list:**
- Item 10 (hub install) ✅ as a one-time scan; scheduling ⚠ is waiting on Taylor.
- Items 1–9 ↪ not reached this round.

**Hub results (numbers only):**
- Repo `D:\SacredSpace_OS`; all 4 roots (the D: repo, the C: market folder, both vaults, read-only).
- 22,465 files scanned → 1,901 indexed, 2,422 duplicates folded, in 357 s.
- Per topic: cash flow 178 · business 495 · nonprofit 129 · marketing 691 · branding 347 · culture 61.

**Findings:**
- WSL can't see D: and OpenCode can't start the cron daemon, so the hub runs under Windows Python.
- Two crashes under Windows: a cross-drive `relpath` error, and the cp1252 console failing on `∆`.
- Topic mistakes: culture was polluted by tool docs (`_ARCHIVE_MCP_DOCS`, keyword "discord"); `BUSINESS_PLAN.md` landed in marketing ("launch"/"analytics"); marketing was inflated by mirror copies (`_ABSORBED`, `_INCOMING`, `pillars_backup`).
- Privacy: proposed that two private folders be skipped (names withheld here).

## Round 1 fixes · Claude Code · 2026-09-27
**Verified / fixed** (each reproduced first, then shown passing):
- **cp1252 crash:** reproduced with `PYTHONIOENCODING=cp1252` (`UnicodeEncodeError` on `∆`). Fixed in `hub_build.py`, `revenue_consolidate.py`, `grama_decode.py` and `decode_parity_check.py`; all four now run under cp1252.
- **Cross-drive links:** a document on C: linked from a hub on D: now becomes a `file:///C:/…` link instead of raising `ValueError`.
- **One config for both Pythons:** roots and `ledger_db` accept `/mnt/d/…` or `D:/…`, translated for whichever Python runs. The ledger opens through a portable read-only SQLite URI.
- **`hub_config.local.json`** (gitignored): private skip_dirs and machine-only roots live there and never enter git. Its lists extend the shared config; its single values override it. Tested: a private folder was skipped and an extra root added.
- **Topic tuning (shared config):**
  - Filename keywords now count 6 (`filename_weight`), up from 3.
  - Removed the loose keywords "discord", "launch" and "analytics"; added "product launch", "launch plan" and "audience growth".
  - Added `_ARCHIVE_MCP_DOCS`, `pillars_backup` and `_ABSORBED` to `skip_dirs`.
  - `_INCOMING` stays scanned on purpose: it's where new material arrives. Tell Claude if it's only a mirror.
- **README:** the Windows scheduled task (`pythonw`, every 3 h) is now the recommended scheduler; WSL cron is the alternative.

**NEXT FOR OPENCODE (round 2):** work from a clean checkout. Items 1–9 from earlier rounds stay open; do the ones below first.
1. **Clean worktree, no data loss:** don't stash, reset or commit Taylor's uncommitted changes in `D:\SacredSpace_OS`. Create a separate worktree for loop work: `git worktree add ../SacredSpace_loop claude/sacred-marketplace-income-67t27a` (or `main` if PR #10 merged). Run every step below from there.
2. **Hub re-run with the fixes:**
   - Put the two private folder names (plus `_RAW` if it's private) into `09_SACRED_MARKET/HUB/hub_config.local.json`. Local only; needs no approval, because skipping more is always safe.
   - Re-run `hub_build.py` under Windows Python.
   - Report the new per-topic counts and run time, and confirm there's no crash and that the C: vault links open.
   - Spot-check culture, marketing and business again (folder and topic only).
3. **Schedule it (only if Taylor wrote "Windows task yes" in this session):**
   - Create the task from `HUB/README.md`, pointing at the worktree path.
   - Check that `pythonw` resolves: use its full path or `pyw` if it doesn't.
   - `schtasks /run` it once and confirm `INDEX.md` updated.
   - Without a yes, skip this and say it's still waiting.
4. **Quick smoke tests (items 5 and 9):**
   - `grama_decode.py "Taylor Oakey" --tier mini` under Windows Python.
   - Open `decode_web/index.html?name=Taylor%20Oakey` in Chrome and confirm the sum, tone and sigil match the Python output. Save the render locally only.
5. **Revenue manifest (replaces item 6):** use the hub's `index.json` instead of the old scan. Write `09_SACRED_MARKET/RECURSION/local_revenue_manifest.md` for the cash-flow, business and nonprofit topics only:
   - repo and D: paths with topic and score
   - vault entries as counts only
   - no titles or summaries from the vault

   This unblocks Claude's `REVENUE_OPERATIONS_MASTER` build.

After these, continue with open item 7 (A4 vault structure map), then 1 (spine check), 2 (asset inventory) and 3 (archive mining). End the round with a NEXT FOR CLAUDE list.

## Round 2 · OpenCode · 2026-09-27
**Ladder rung:** no sales yet ($0). No `merchant.db` anywhere (plan I-5 still open).
**Done from last NEXT list:**
- Item 1 (worktree) ✅ — `D:\SacredSpace_loop`, sparse to `09_SACRED_MARKET` (+`systems/fastapi` for merchant.py). Note: the branch tree contains an invalid Windows path (`D:/SacredSpace_OS/archive/memory-motes/sacred.db`) that breaks full checkouts/resets; sparse cone avoids it. D: working tree untouched.
- Item 2 (hub re-run) ✅ — 14,400 scanned → 1,491 indexed, 2,250 dupes folded. Per topic: cash flow 162 · business 402 · nonprofit 101 · marketing 466 · branding 317 · culture 43. No crash (fixes confirmed). C: duplicate links resolve 44/44. Spot-check: culture clean (no more tool docs), `BUSINESS_PLAN.md` now primary business. `hub_config.local.json` holds skip_dirs + machine roots (gitignored, never commit).
- Item 3 (schedule — Taylor: yes) ✅ — `schtasks` "SacredSpace Hub" every 3 h (`pythonw`, full path, worktree tools). `schtasks /run` → Last Result 0, fresh INDEX (header 22:44). Verified `print` works under this `pythonw` first. After PR #10 merges, repoint the task at `D:\SacredSpace_OS`.
- Item 4 (smoke) ✅ — `grama_decode.py "Taylor Oakey" --tier mini` (PYTHONPATH to branch `systems/fastapi`) vs C2 page under node: sum 148, tone 4, The Builder, ✦TAYL4∆, 7∆YL0R 0∆K3Y — 5/5 match. Caveat stands: decode needs `merchant.py` sibling (absent from `FIRST_FLAME/`).
- Item 5 (manifest) ✅ — `RECURSION/local_revenue_manifest.md` (408 lines; vault as counts only: business 180, cashflow 89, nonprofit 40). Privacy-checked (only ICARIS role-name hits, no private content).
- Item 7 (vault map) ✅ — `RECURSION/local_vault_structure.md` (161 folders depth ≤3, names+counts only; 0 private-marked at that depth).
- Earlier chat findings now landed: spine serves from `systems/fastapi/app/main.py:16,32–39` (8 routers, NO merchant.router; :8888 down; `PORTAL/index.html:262` uvicorn target stale); A5 refuted (78 declared, 0 card objects); archive pass (chats/ = stubs; 05-26 prices conflict with bank; notebook files exist; 6 Claude chats never exported).
**Verified / refuted:** all above with paths, counts and outputs in this entry.
**Ideas added:** A9 (Cipher Puzzle Pack, 27) · **Re-scored:** A5 29→**25** (no card objects exist).
**Experiments:** Slot 1 approved-unlisted · Slot 2 C2 (page built, SHOP links empty) · Slot 3 A4 (spec + vault map done).
**Notes for Taylor:**
1. C2/A4 are built but publishable only by you (separate public repo/space; listings don't exist yet).
2. Year-1 letters stay out of every product until you rule explicitly otherwise.
3. The branch has one bad path entry (`archive/memory-motes/sacred.db`) — future Windows checkouts need sparse cone until it's renamed.
**NEXT FOR CLAUDE:**
1. Fold the 05-26 price points ($9–15 map, $15–25 custom decode, $7–12 rulebook) into the listing comp rewrite (your item 1).
2. Comp 5–10 printable puzzle packs (price, page count, sales signals) for A9.
3. Fee math for the sub-$10 tier (A9 at $5–9, A2 at $7) on Gumroad vs Ko-fi.
4. Template license + refund norms for the A4 SPEC (your item 3 covers price; add the legal wrapper).

## Round 2 repair · Claude Code · 2026-09-27
**What happened:**
- OpenCode's round-2 commit (`c389b4b`) also recorded **180 unintended deletions**: `CLAUDE.md`, `AGENTS.md`, `systems/` (including `merchant.py`), and almost every pillar outside `09_SACRED_MARKET`.
- Root cause: the repo tracked an empty file at the path `D:/SacredSpace_OS/archive/memory-motes/sacred.db`, which is invalid on Windows because of the colon. That forced a partial (sparse) Windows worktree, and committing from it staged everything missing as deleted.
- Merging PR #10 in that state would have deleted those files from `main`.

**Fixed:**
- All 179 real files restored in a new commit (no history rewrite).
- The empty `D:/…/sacred.db` stays removed: 0 bytes, committed by accident in April, and it blocks Windows checkouts.
- A full worktree now checks out on Windows, so the sparse workaround is no longer needed.
- OpenCode's intended changes are kept (ROUND_LOG, IDEA_BANK, the two local maps).

**Privacy:** three lines in `local_revenue_manifest.md` / `local_vault_structure.md` named another person (a full name and a profile note). They're redacted to "(personal file — name redacted)". Rule reminder: file and folder names count as personal details.

**Guardrail added to PROMPT_OPENCODE:** stage explicit paths only; check `git diff --cached --stat` before committing and stop on any unexpected deletion.

**NEXT FOR OPENCODE (round 3, first):** in `D:\SacredSpace_loop`, run `git sparse-checkout disable` (if sparse), then `git pull`. Confirm `git ls-files | wc -l` matches `git ls-tree -r HEAD --name-only | wc -l` and that `git status` is clean. Point the "SacredSpace Hub" scheduled task at the full worktree again if its path changed.
## Round 2 addendum · OpenCode · 2026-09-27 (second pass, same round — append-only per loop rule)
**Ladder rung:** no sales yet ($0). No `merchant.db` anywhere (plan I-5 still open).
**Done deltas vs the Round 2 entry above (not a rewrite — corrections + new ground truth):**
- Hub re-run (final, with merged `hub_config.local.json`): **9,028 scanned → 1,304 indexed, 770 folded, 181 s.** Per topic: business 344 · cashflow 143 · nonprofit 85 · marketing 405 · branding 286 · culture 41. NOTE: counts differ from the first Round-2 pass (14,400/1,491) because the local skip list changed mid-round (`_INCOMING_FROM_C` 255 mirror docs + `_SESSION_EXPORTS` now skipped; `FAMILY_RHYTHM_LAYER` + `_RAW` were already skipped). Canonical numbers = latest `index.json`. One handled skip: `SACREDSPACE_BIBLE.md` Errno 22 under Windows (filename issue, no crash).
- Parity harness bug FOUND + FIXED (`tools/decode_parity_check.py`: `subprocess.run` decoded node's UTF-8 stdout as cp1252 → false MISMATCH on every non-ASCII name; added `encoding="utf-8"`): **310 names · 0 mismatches · tones 1–9/11/22.** Taylor Oakey 148/4/Builder/✦TAYL4∆ identical both engines. `grama_decode.py` output bytes verified UTF-8 (∆/✦ present, zero `?`). Chrome interactive open still not done in-session (no interactive browser); node-run of the page's exact ENGINE block is the substantive check.
- Manifest + vault map: KEPT the committed redacted versions from the repair commit — my regen drafts are dropped, not pushed, to avoid reintroducing the 3 redacted personal-name lines. Lesson recorded: file/folder names count as personal details (my earlier scan caught only role-names and missed a full name + profile note). Hub-run numbers (9,028 scanned → 1,304 indexed: business 344 · cashflow 143 · nonprofit 85 · marketing 405 · branding 286 · culture 41) live in this entry and the latest gitignored `index.json` for Claude's master build.
- Spine check: serving file = `D:\SacredSpace_OS\systems\fastapi\app\main.py` (:8888, 8 routers, NO merchant.router); merchant module = `systems/fastapi/merchant.py` (48,978 B, `router = APIRouter(prefix="/merchant")` :988, mount snippet :1186). Insert point = `main.py` after line 39 (`from merchant import router as merchant_router` + `app.include_router(merchant_router)`; needs `systems/fastapi` on path). :8888 dark right now. Live spine untouched per protocol.
- A5 refutation confirmed independently: `arcana_grid/game_data.json` is a 15-key canon companion (character_registry 15 entries), no card-object array.
- Asset inventory (item 2) ⚠ BLOCKED: art not located — `creative-output/` 0 files, `media/` 3 files, `07/avatars` + `07/content` 0 files, `04` images 0. The 8 design families / 2018–22 paintings / 68 Gemini images are UNVERIFIED (not refuted; likely Takeout/Drive/vault-adjacent, out of reach this round).
- Archive mining (item 3) ⚠ BLOCKED: `chatgpt_export_parser.py` exists; no `chat.html` on D: shallow search; G: Drive absent. C: chats = 20 files (vs remembered 18); sampled stub confirmed title-only (386 chars).
**Ideas added:** F1 (claude-project-import mine, 27) · F2 (C: canvas-print plans → A3 pilot, 25) · **Re-scored:** none (A5 correction already scored by prior pass).
**Experiments:** unchanged (Slot 1 approved-unlisted · Slot 2 C2 built/SHOP-empty · Slot 3 A4 spec+mapped, build deferred).
**Notes for Taylor:** (same 3 as prior pass stand) + hub counts move with local skips — judge rounds by `index.json`, not memory.
**NEXT FOR CLAUDE** (standalone, ≤5, research-answerable):
1. `REVENUE_OPERATIONS_MASTER.md` is UNBLOCKED (manifest + vault map committed this round) — build it from those plus plan/IDEA_BANK.
2. First Flame listing evidence: re-verify Etsy digital + metaphysical rules + fees behind `LISTINGS.md`; comp ~10 name/numerology listings; 3 long-tail keywords; rewrite 13 tags if evidence says so.
3. C2 distribution: 3 welcoming communities + self-promo rules; confirm GitHub Pages + HF Static still free for one static page.
4. A4 market: price/bundle/traffic of top ~10 Obsidian template sellers; forum selling restrictions; re-score A4.
5. Grants: NC Artist Support Grant council for Northampton County + next cycle (proposed `POST /merchant/grants` body in log, no API calls); 2–3 fiscal sponsors + fees.

## Round 2 close · Claude Code · 2026-09-27: agenda for OpenCode's round 3 (set at Taylor's request)
**Audit of `4e0651a`:** clean. Three files staged by name, no deletions, no new personal details. The parity-harness UTF-8 fix is correct and re-verified here: 310 names, 0 mismatches.
**Fixed:** `merchant.py` hardcoded `DB_PATH = /mnt/d/...`. Under Windows Python that creates a stray `D:\mnt\d\...` folder and a database the hub never reads. It now defaults to `D:/SacredSpace_OS/...` on Windows and `/mnt/d/...` on WSL, and `MERCHANT_DB` overrides both.

**NEXT FOR OPENCODE (round 3):** do item 1 first, and commit by explicit path only (see the guardrail in PROMPT_OPENCODE).
1. **Worktree repair:**
   - In `D:\SacredSpace_loop`: `git sparse-checkout disable` (if sparse), then `git pull`.
   - Confirm `git ls-files | wc -l` equals `git ls-tree -r HEAD --name-only | wc -l` (≈323) and that `git status` is clean.
   - Repoint the "SacredSpace Hub" task if its path changed, then `schtasks /run` it once.
2. **Ledger bootstrap + spine patch (plan I-5):**
   - Under Windows Python, run `python -c "import sys; sys.path.insert(0,'systems/fastapi'); import merchant; merchant.init_merchant_db()"` from the worktree. This creates an empty `D:\SacredSpace_OS\05_MEMORY_ENGINE\merchant.db`.
   - Confirm the hub's Ledger snapshot now shows First Flame $0.00 of $1,111.
   - Write (don't apply) the two-line mount for `systems/fastapi/app/main.py` as `RECURSION/proposed_spine_patch.diff`.
   - Prove it with FastAPI `TestClient` against a temp DB (`MERCHANT_DB=<temp>`): `GET /merchant/ledger` returns 200 and a sale POST round-trips. Taylor applies it to the live spine.
3. **A4 build (item 8):**
   - Build `SovereignCreatorVault/` fresh from `A4_VAULT_TEMPLATE/SPEC.md`, using `local_vault_structure.md` as the folder guide. Build it outside the repo, and copy no file from the live vault.
   - Run the spec's leak check and report the grep output (it should be empty) plus folder and file counts.
   - Zip it locally. Taylor opens and reads it before anything else happens.
4. **Find the art (unblocks asset inventory, item 2):**
   - Search beyond D: for image folders (`.png/.jpg/.webp/.psd/.kra/.tif`): `C:\Users\*\Pictures`, `Downloads`, `OneDrive`, `Desktop`, any Google Drive for desktop letter, and external drives.
   - Report **folder paths + image counts + largest pixel size only**; no filenames that could be personal.
   - If the 8 design families, the 2018–22 paintings or the 68 Gemini images still aren't found, ask Taylor one question: where do they live?
5. **Find the ChatGPT export (unblocks archive mining, item 3):**
   - Search every drive for `chat.html`, `conversations.json`, `*chatgpt*export*.zip` and `takeout-*.zip`.
   - If found, run `chatgpt_export_parser.py` and list the 10 conversations with the most finished, sellable drafts (date + title only).
   - If not found, write one line for Taylor: "Request a fresh export: ChatGPT → Settings → Data controls → Export data" (Taylor's action).

## Triage · Claude Code · 2026-09-27: external report "Sacred Merchant → Personal Drop Ship Professional" (relayed by Taylor)
**Logged as G1 (17/40, PARKED)** in a new IDEA_BANK section G for external proposals. Evidence is in the row.
- **Salvaged:**
  - A3: POD as the brand-fit dropship model, with order → tracking automation.
  - B1: shop FAQ and abandoned-cart bots are the VaaS service.
  - D2: build the ledger sync as a self-hosted n8n flow.
- **Rejected:** its detection-evasion tactics (anti-detect browsers, AI-altered duplicate photos, bots disguised as humans, undisclosed negotiation bots). They breach platform rules and the plan's honesty guardrails.
- **New fact:** Meta commerce policy bars digital goods, so decodes and downloads stay off Facebook Marketplace.
- **Guardrail for both agents:** don't re-propose generic dropshipping without new evidence and Taylor's ask.

## Round 2 agenda, consolidated · Claude Code · 2026-09-27 (set at Taylor's request)
Three NEXT FOR CLAUDE lists are open (Round 1 close, OpenCode Round 2, OpenCode Round 2 addendum), about 14 items with duplicates. **This list supersedes all three for Claude's round 2.** Mark the older items "→ consolidated" and don't redo them separately.

**NEXT FOR CLAUDE (round 2, consolidated):** web research with a URL for every claim, except item 1.
1. **Build `09_SACRED_MARKET/REVENUE_OPERATIONS_MASTER.md` (now unblocked):**
   - Sources: `RECURSION/local_revenue_manifest.md` + `local_vault_structure.md` (paths and counts only), the plan, IDEA_BANK (including G1) and `LISTINGS.md`.
   - Use the section template from Taylor's REVENUE_CONSOLIDATE (streams, POD, grants, crowdfunding, digital products, costs, timeline, merchant directives, open items). Label it DISTILLED, pending the Canon Gate.
   - Repo only, never the vault. No private names or paths.
2. **First Flame listings — evidence + pricing:**
   - Re-verify Etsy's digital-download and metaphysical rules and its fees, then fix `LISTINGS.md` if anything moved.
   - Comp ~10 name-meaning / numerology listings: price, format, reviews.
   - Find 3 long-tail keywords, and rewrite the 13 tags if the evidence says so.
   - Fold in the 05-26 price points ($9–15 map, $15–25 custom decode, $7–12 rulebook).
   - Add fee math for the sub-$10 tier (A2 $7, A9 $5–9) on Etsy vs Ko-fi vs Gumroad.
3. **Distribution & comps for the other products:**
   - C2: 3 communities where a free, private decode tool is welcome, each with its self-promotion rule. Confirm GitHub Pages and Hugging Face Static Spaces are still free.
   - A4: price, bundle and traffic source of the top ~10 Obsidian template sellers; forum or marketplace selling restrictions; common template licence and refund terms for the SPEC. Re-score A4.
   - A9: comp 5–10 printable puzzle packs (price, pages, sales signals). Score A9.
4. **Grants & nonprofit:**
   - Which council administers the NC Artist Support Grant for Northampton County, and when is the next cycle? If it's open to individual artists, put a proposed `POST /merchant/grants` body in the log (no API calls).
   - 2–3 fiscal sponsors that would take an AI-literacy or family-storytelling project, with their fees.
5. **Tax + lexicon upkeep:**
   - Find the source for NC sales tax on digital downloads sold outside Etsy (Ko-fi, Gumroad), marked "verify with an advisor".
   - Resolve every *(verify)* item you check in `HUB/RESEARCH_LEXICON.md` with a date and URL, and add the search terms that worked.

## Round 2 · Claude Code · 2026-10-06
**Ladder rung:** no sales yet ($0). No ledger exists; OpenCode reported none.
**Environment limit:** etsy.com, ko-fi.com, gumroad.com and ncarts.org were blocked from the cloud runner. Fees, rules and grant dates below come from search-result sources (named in each file) and are labelled secondary. Anything marked "needs browser check" is OpenCode/Taylor's to confirm.
**Done from the consolidated agenda** (this list supersedes the three older Claude lists; each is "→ consolidated"):
1. ✅ **`REVENUE_OPERATIONS_MASTER.md`** built at `09_SACRED_MARKET/`, DISTILLED, repo-only, counts only, no private names or paths.
2. ⚠ **First Flame listings, partly done:**
   - ✅ Etsy fees unchanged ($0.20 / 6.5% / 3% + $0.25; Offsite Ads 12–15%); readings-with-a-copy still allowed, outcome promises banned, AI disclosure required.
   - ✅ Fee math for sub-$10 items on Etsy, Ko-fi and Gumroad, in `LISTINGS.md` §1b. Ko-fi nets most at every price; Gumroad's $0.50 floor is worst at $5.
   - ✅ 05-26 price points folded into `LISTINGS.md` §1c: they bracket the $11/$22 tiers, so no price change.
   - ⚠ **Not done:** the ~10 individual Etsy comps and the 3 long-tail keywords (Etsy was blocked; only aggregate stats were reachable). The 13 tags are unchanged because there is no evidence to rewrite them. Handed to OpenCode below.
   - ⚠ **Conflict:** Ko-fi Gold is quoted at $6/mo and $12/mo by different sources; the $240 break-even in §0 may be wrong.
3. ⚠ **Distribution and comps:**
   - ✅ GitHub Pages is free for public repos (1 GB site, ~100 GB/month soft bandwidth) and HF Static Spaces are free; CPU/Gradio Spaces now need a paid plan ([GitHub docs](https://docs.github.com/en/enterprise-server@3.15/pages/getting-started-with-github-pages/github-pages-limits), [HF docs](https://huggingface.co/docs/hub/en/spaces-overview)).
   - ⚠ C2 communities: only partial. Reddit's general rule is 90/10 participation vs. promotion, and r/SideProject is the promotion-friendly place for indie tools ([Redship](https://redship.io/blog/reddit-self-promotion-rules)). I could not read the rules of numerology or tool-showcase subreddits. Candidates to check by hand: r/SideProject, r/InternetIsBeautiful, a "Show-off Saturday"-style thread; read each sidebar before posting.
   - ✅ A4: price band $15–39 single, ~$49 for Notion+Obsidian bundles; Obsidian allows self-promotion with extra scrutiny on paid content; licence/refund wording drafted in the A4 row. ⚠ I could not open ~10 seller pages, so traffic sources are unverified. A4 stays 33.
   - ✅ A9: 5 Etsy comps, $3.30–5.00 for packs of 21–160 puzzles. $5–9 is above market. Score kept at 27 on a revised plan (Etsy/Ko-fi, ≤$5–6 or bundled).
4. ✅ **Grants:** Granville Arts is the regional partner for Northampton County; the FY26-27 deadline was 2026-08-31 and has **passed**; range $500–$1,000; next cycle unpublished (probably ~June 2027). E1 re-scored 23→19, PARKED. Fiscal sponsors: Fractured Atlas 8% + $10/mo, Hack Club HCB 7%, Open Source Collective 10% (E3, PARKED).
   - Proposed grants body (not sent, no API call): `POST /merchant/grants` `{"funder":"NC Arts Council via Granville Arts","program":"Artist Support Grant","applicant_entity":"SOLE_PROP","amount_requested":1000,"deadline":null,"url":"https://granvilleartsnc.org/en/artist-support-grants/","eligibility":"Individual artist; regional partner covers Northampton; ask about residency and study rules","notes":"FY26-27 closed 2026-08-31; next cycle expected ~June 2027; confirm by email first"}`
5. ✅ **Tax + lexicon:** NC taxes "specified digital products" (digital audio, audiovisual, books); a facilitator collects on what it facilitates; the remote-seller threshold is $100,000 (200-transaction test gone since 2024-07-01). Unresolved: whether a decode PDF, wallpaper or vault template counts, and Taylor's own in-state obligations on non-Etsy sales. **Verify with an advisor.** Lexicon "(verify)" items resolved for sales tax and fiscal-sponsor fees; new grant and search-term notes added.
**Verified / refuted:** *Refuted:* the old "fiscal sponsor fee often 5–10%" (it's 7–14%); Gumroad "10% + 2.9%" in the A4 row (it's 10% + $0.50, with sources split on processing). *Confirmed:* G1 stays parked; nothing new to revisit.
**Ideas added:** A10 (January numerology window, 29) · E3 (fiscal sponsor, 20, PARKED). **Re-scored:** A1 32→30 (S 5→4, review-count wall); E1 23→19 (S 3→1, cycle passed); A4 and A9 unchanged with notes.
**Experiments:** Slot 1 (First Flame): approved, unlisted, not started. Slot 2 (C2): built, unpublished. Slot 3 (A4): spec + map done, build pending. **Kill clocks have not started because nothing is public.**
**Shadow check:** this loop has produced about 20 documents and 0 listings. Cutting scope: no new research round is useful until a listing is live or Taylor makes the decisions below.
**Notes for Taylor:**
1. Deadline for the NC grant passed (Aug 31); next chance is ~June 2027 and needs one email to Granville Arts.
2. The cheapest next step is to publish C2 and the four First Flame listings; January is the numerology demand peak, so the window is about 8 weeks.
3. Open decisions: target monthly net and runway, seller of record (E2), VaaS (B1), nonprofit timing.
**NEXT FOR OPENCODE** (≤5, each checkable on Taylor's machine):
1. In a browser (etsy.com is blocked for me): search "name meaning", "name numerology", "personalized name reading"; record the top 10 listings (price, format, review count) and the 3 best "related searches"; paste into this log as a table.
2. Read the live Etsy, Ko-fi and Gumroad fee pages; confirm Etsy 6.5% / 3% + $0.25 / $0.20, Ko-fi shop 5% and Gold's real monthly price, Gumroad 10% + $0.50 and whether processing is included. Correct `LISTINGS.md` §0–1b if any figure differs.
3. Open ncarts.org's Artist Support page and Granville Arts' page; copy the eligibility lines and the next-cycle date (no application).
4. Confirm whether `_INCOMING_FROM_C` is only a mirror of files already in the repo (spot-check 10 files by hash). If so, record it as "skipped, mirror" in the hub config notes.
5. Continue your round-3 items 1–5 from "Round 2 close" (worktree repair, ledger bootstrap, A4 build, art search, export search).
