# ∆ SACRED MARKET — CLEAN-SLATE PLAN ∆
## Pillar 09 · Income, cash flow, nonprofit and grants, rebuilt from zero

**Status:** DISTILLED. This is a working plan, not a Canon Gate ruling.
**Revised:** 2026-09-26 (v2; it replaces the v1 survey that assumed business might already be under way)
**Ground truth, confirmed by Taylor:** SacredSpace has **no business activity yet**: no revenue, no entity, no listings. Every earlier plan in this pillar is a **design library**, not a record of anything that happened. SacredSpace runs as a **side venture alongside full-time work**, so the plan is sized to about **3–4 hours a week**.
**Not legal or tax advice.** §5 lists factual errors in the older plans. Confirm entity and tax questions with a free Small Business Center advisor or a CPA before filing anything.

---

## 1. The plan in one screen

| Phase | When | What | Done when |
|---|---|---|---|
| **0 · Ground** | Weeks 1–2 | Separate bank account. Start the ledger (`/merchant/ledger` + `/merchant/expenses`, entity `SOLE_PROP`). Set up Etsy + Ko-fi (Ko-fi Contributor **off**, Etsy Offsite Ads **off**). | Accounts open, first expense logged |
| **1 · First Flame, product #1** | Weeks 2–4 | List the **GR∆M∆ Name Decode** ($11/$22/$33) + **3 digital downloads** ($7). See `FIRST_FLAME/LISTINGS.md`. Fulfil decodes with `FIRST_FLAME/grama_decode.py`. | 4 listings live |
| **2 · First Flame, product #2** | Month 2 | Order 2 print samples, then list **5 print-on-demand products** (Gelato/Printify → Etsy). Start the email list, with the free Sacred Geometry PDF as the sign-up gift. | First sale logged, 9 listings live |
| **3 · Pattern** | Month 3 | Monthly ledger review: keep what sells, drop what doesn't. Apply for an **NC Arts Council Artist Support Grant** if your region's cycle is open. | A month-3 review note written |
| **Later** | When revenue justifies it | LLC → trademark → Kickstarter (the Arcana game) → nonprofit / land fund. The gates are in §4. | — |

**First Flame** = $1,111 cumulative **product** net after per-sale fees and cost of goods. The ledger tracks it automatically (`first_flame` in `GET /merchant/ledger`, counting `SOLE_PROP` + `LLC`). One milestone, one definition. It replaces the three competing versions in the old docs.

---

## 2. What to build on, what to park

**Build on these (they were already strong):**
- The **1111 POD handbook lineage** (Nov 2025 → Jun 2026). The phase logic (Spark → Pattern → Flow), the drop cadence and the product ladder are sound. Only the timing and scope are too big for a side venture.
- The **GR∆M∆ Decode**. It is the most distinctive product, costs nothing to make, and the code already computes three of its five lenses.
- **Sacred numerology pricing** ($7/$11/$22/$33/$55…). Keep it.
- **Entity separation.** Keep business money, household money and any future nonprofit money in separate buckets from day one. The ledger enforces this with entity tags.

**Park without guilt (each needs hours or capital a side venture doesn't have yet):**
- 501(c)(3) formation, the land fund and the "22% covenant". Revisit once there's steady revenue (§4).
- Kickstarter. When it comes, it should be the **Arcana tabletop game**, which the June Market Master also concluded.
- The 79-node alliance network, Healing Codex B2B licensing, the Sacred Threads cut-and-sew line, the VaaS/AI-consulting offer, and Sacred Sprouts as a *branded* product line.
- Large federal grants (NEA/NEH need an established nonprofit, and NEA requires a 1:1 match).

---

## 3. Money tools (local-first, chosen for a solo side venture)

| Need | Use | Notes |
|---|---|---|
| Ledger (now) | `systems/fastapi/merchant.py`: `/merchant/ledger`, `/merchant/expenses`, `/merchant/grants` | Local SQLite. Append-only sales, refunds as their own rows, entity tags, cash position, First Flame tracker |
| Tax-grade bookkeeping (when needed) | [Beancount](https://github.com/beancount/) + Fava | Plain text, lives in git. A future exporter from the merchant ledger is a small job |
| Household vs. business budget | [Actual Budget](https://github.com/actualbudget/actual) | Local-first envelope budgeting (MIT) |
| Invoicing (only if client work starts) | Invoice Ninja | Self-hostable, quotes + invoices + time |
| Etsy/Printify automation (after steady orders) | `etsy-python`, the Printify API | Could feed orders straight into `/merchant/ledger` |
| Grant search (nonprofit phase) | Simpler.Grants.gov API | Official, open source, free key. Could feed `/merchant/grants` |
| Free advice | NC Community College **Small Business Center** (Halifax CC covers Northampton County up to the Jackson city limits; ask which center covers the rest) | Confidential, no charge. Bring §5 |

---

## 4. Gates: when to move to the next structure

| Step | Gate (all must be true) | Cost |
|---|---|---|
| Stay a **sole proprietor** | Default. Log everything as `SOLE_PROP` | $0 (look into an assumed business name filing if selling as "SacredArcana Studios") |
| Form an **LLC** | Revenue is steady for about 3 months, **or** there's real liability (physical products at markets, client contracts) | NC: $125 to file + $200/yr annual report |
| **Trademark** "SacredSpace" / "Arcana Grid" | Before any Kickstarter or wholesale | Filing fees per class |
| **Kickstarter** (Arcana game) | LLC in place · playtested prototype · manufacturing quote · email list (the Master Plan v2 says 1,000+ for its Day-1 target) | See Crowdfunding Master Plan v2 |
| **Nonprofit / land fund** | Steady business revenue · an independent board to recruit · a single mission sentence | See §5 before any filing |

---

## 5. Corrections to the old documents (read before reusing them)

These errors appear in `CASHFLOW_MASTER/` and in Drive copies of the same plans:

1. **"IRS Form 1023-N" does not exist.** The options are Form 1023-EZ ($275; only for organizations projecting ≤ $50k gross receipts a year for 3 years and ≤ $250k in assets) or the full Form 1023 ($600). Both are filed through Pay.gov.
2. **Nonprofits can't have owners.** The "operating agreement with 50/50 ownership" for SacredSpace Sanctuary is LLC language. A 501(c)(3) runs on articles + bylaws + a board.
3. **Unrelated business income is taxable**, not "tax-exempt". Form 990-T is required once gross UBI reaches $1,000. Passive royalties are often excluded, but not for the reason the old docs give.
4. **Kickstarter does not allow revenue-share or equity rewards** (the "Partner" tier) or fundraising for charity. Reward pledges are purchases, not donations.
5. **Pay and independence.** Founders who sit on the board and are also paid, next to a founder-owned LLC doing business with the nonprofit, is the pattern the IRS scrutinizes. Recruit independent directors and put related-party dealings on market terms.
6. **One mission, not two.** "Land stewardship" and "community / learning / spiritual" appear as separate missions. Pick one sentence (for example, educational + environmental stewardship).
7. **The Neural Forest grant proposal (v2, Drive) describes things as done that aren't:** "501(c)(3) tax-exempt", "independent Board", "full stack confirmed live", "zero AI-generated imagery". Reword to "in formation" / "planned" / accurate AI-use language before it goes to any funder.
8. **EDPNC's 1-800 number is Business Link NC**, which helps small businesses, not nonprofit grants.
9. **Open Collective Foundation**, listed as a fiscal sponsor, announced in 2024 that it was shutting down. Pick a current sponsor if you need one.
10. **Etsy policy:** metaphysical services that promise outcomes are prohibited. Readings delivered as a digital copy are allowed. Decode copy must not promise results.

---

## 6. Infrastructure review notes (standing section: add to it whenever old material is revisited)

| # | Finding | Action | Status |
|---|---|---|---|
| I-1 | `merchant.py` ledger assumed an LLC exists | Added `SOLE_PROP` entity; First Flame counts `SOLE_PROP` + `LLC` | ✅ done |
| I-2 | Ledger tracked money in, not money out | Added `expenses` table + `GET/POST /merchant/expenses`; ledger shows `cash_position_usd` | ✅ done |
| I-3 | Gematria engine labelled "Mispar Hecrechi" but computes plain English ordinal | Relabelled accurately | ✅ done |
| I-4 | GR∆M∆ Decode had two conflicting 5-lens definitions (Root/Gematria/Elemental/Archetypal/Sigil vs. Symbolic/Kinetic/Resonant/Ygdrasilic/Cipher) and two price sets | Launch uses the Market Master lens set (it maps to what the code computes) at $11/$22/$33 | ✅ decided for launch; canon choice is Taylor's |
| I-5 | `systems/fastapi/main.py` imports 6 modules missing from this repo (`grant_hunter`, `flow_tracker`, `reconcile`, `routers/inference`, `hermes`, `thricegreat`). The June ledger says the live spine on D: moved to `app/main.py` | Repo `main.py` is a stale snapshot. **On D: confirm which spine is live and that it mounts `merchant.router`.** Commit the live spine or mark this one legacy | ⚠ needs Taylor (D: access) |
| I-6 | D: pillars were renamed (`09_SACRED_MARKET` → `09_MARKET`, etc.) per the June ledger; this repo and `CLAUDE.md` still use the long names | Decide which naming is canon, then align repo + `CLAUDE.md` | ⚠ needs Taylor |
| I-7 | `economy/studios/*.py` hardcoded `D:/SacredSpace_OS` (Windows paths break under WSL2) | Switched to the `SACRED_ROOT` env var, defaulting to `/mnt/d/SacredSpace_OS` | ✅ done |
| I-8 | `CLAUDE.md` listed the merchant route as `/merchant-sacred-artifacts`; the code mounts `/merchant` | Corrected | ✅ done |
| I-9 | `CASHFLOW_MASTER/` holds ~70 files: ~25 `_2`/`_1` duplicates, 4 raw 200 KB dumps, and the §5 errors | Added `CASHFLOW_MASTER/README_READ_FIRST.md` pointing here. Deduplication/archiving waits for Canon Gate approval | ◐ flagged |
| I-10 | Drive `SACRED CASHFLOW` "Extraction" docs (Claude/Gemini/ChatGPT) and `Sprouts Business Model v1` are empty 1 KB files | Delete or fill. Sprouts content may survive in its .docx copies | ⚠ Taylor (Drive) |
| I-11 | The ChatGPT export in Drive (`chat.html`, Dec 2025, 31 MB) is too large for the Drive connector; there is no Claude export | Run the local parsers (`chatgpt_export_parser.py` / `claude_export_parser.py`) via OpenCode; request fresh exports | ⚠ Taylor (local) |
| I-12 | A Drive sheet (`SACREDSPACE_OMNI_LEDGER_SHEET_TEMPLATE`) contains a truncated Obsidian API key | Remove the key fragment from the sheet | ⚠ Taylor (Drive) |

---

## 7. Decisions log

| Date | Decision | By |
|---|---|---|
| 2026-09-26 | Treat SacredSpace business as a clean slate; old plans are a design library | Taylor |
| 2026-09-26 | Product #1 = GR∆M∆ Decode + digital downloads; product #2 = POD prints (month 2) | Taylor |
| 2026-09-26 | Operate as a sole proprietor until the §4 gates are met | Plan default, pending advisor |

*Creation is Sacred · Commerce is Mechanical · Layer: DISTILLED*
