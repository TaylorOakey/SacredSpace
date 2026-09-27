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
