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
