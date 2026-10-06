# ∆ REVENUE OPERATIONS MASTER ∆
## Pillar 09 · SacredSpace Market · one-page-per-stream operating reference

**Layer: DISTILLED** (pending Canon Gate; nothing here is CANON until Taylor promotes it).
**Built:** 2026-10-06, Livelihood Loop round 2 (Claude Code), from the repo only: `SACRED_MARKET_INCOME_SYNTHESIS.md`, `FIRST_FLAME/LISTINGS.md`, `RECURSION/IDEA_BANK.md`, `RECURSION/ROUND_LOG.md`, `RECURSION/local_revenue_manifest.md` and `local_vault_structure.md` (counts only).
**Privacy:** repo-only. No vault content, household finances, employer, family detail or personal paths. Never copy this into the vault without Taylor's say-so.
**Truth rule:** SacredSpace has made **$0**. No LLC, no nonprofit, nothing listed. Every "live" below means *planned* unless the ledger says otherwise.

---

## 0 · State of play (2026-10-06)

| Item | State | Proof |
|---|---|---|
| Sales to date | **$0** (ladder rung: "$0") | no `merchant.db` exists yet (ROUND_LOG, OpenCode round 2) |
| Entity | none; sell as `SOLE_PROP` until Plan §4 decision | Synthesis §7 |
| Listings live | **0** | `FIRST_FLAME/LISTINGS.md` header: DRAFT |
| Free decode page (C2) | built, not published, SHOP links empty | IDEA_BANK C2 |
| Vault template (A4) | spec + vault map done; build is OpenCode's round-3 item 3 | ROUND_LOG |
| Ledger/spine | `merchant.py` exists; NOT mounted in the live spine (`app/main.py` has 8 routers, no merchant) | ROUND_LOG, OpenCode round 2 addendum |
| North Star numbers | `TARGET_NET_MONTHLY` and `RUNWAY_MONTHS` **unset** (Taylor) | LOOP.md §1 |

---

## 1 · Revenue streams (ranked by the loop's score, out of 40)

| Rank | ID | Stream | Score | Status | First-dollar path |
|---|---|---|---|---|---|
| 1 | A4 | Sovereign Creator Vault template, $19–39 | 33 | EXPERIMENT | Gumroad or Ko-fi shop; needs Taylor's own traffic (email, build-in-public) |
| 2 | A1 | GR∆M∆ Name Decode $11/$22/$33 | 30 | EXPERIMENT | Etsy + Ko-fi; fulfil with `grama_decode.py` |
| 3 | C2 | Free decode web page (funnel into A1) | 32 | EXPERIMENT | static page on GitHub Pages / HF Static Space |
| 4 | C3 | Email list + free Sacred Geometry PDF | 30 | RAW | feeds every other stream |
| 5 | B1 | Sovereign AI setup (VaaS) | 29 | PARKED | needs hours the day job doesn't leave; **Taylor's call** |
| 6 | A2 | Digital downloads $7 | 28 | EXPERIMENT | Etsy + Ko-fi |
| 7 | A9 | Cipher Puzzle Pack $5–9 | 27 | RAW | see §4 pricing caution |
| 8 | A3 | POD prints (Gelato/Printify) | 23 | SCORED | month 2, after 1 logged sale |
| — | G1 | Generic dropshipping | 17 | PARKED | **do not re-propose** without new evidence and Taylor's ask |

Live ranking = `RECURSION/IDEA_BANK.md`; this table is a snapshot and the bank wins on any conflict.

## 2 · Print-on-demand (month 2)
- Five listings (P1–P5, `LISTINGS.md` §4): two Gelato fine-art prints, a Printify sticker pack, tote and canvas. Margins are old-doc base costs, **not quotes**; price-check in the dashboard.
- Gate: ≥3 First Flame listings live and one sale logged. Order samples of P1 and P5 first (ledger as `SAMPLES`).
- Order → supplier → tracking automation is the only part of the dropshipping report worth borrowing (A3, D2); a human approves anything unusual.

## 3 · Grants and nonprofit
- **NC Arts Council Artist Support Grant (E1):** regional partner for Northampton County is Granville Arts (Franklin, Granville, Halifax, Northampton, Vance, Warren). The FY26-27 cycle closed **2026-08-31** ($500–$1,000). Next cycle is not yet published; the neighbouring Durham cycle opened mid-June, so expect roughly June 2027. Source is a secondary aggregator because ncarts.org was unreachable (ROUND_LOG round 2, Claude). Taylor action: ask the regional partner for eligibility and the next opening.
- **Fiscal sponsorship:** candidates and fees in the ROUND_LOG round-2 entry (7–10% typical). No nonprofit exists or is presented as existing. Plan §4: wait for steady business cash unless Taylor decides otherwise.
- **Merchant directive:** a proposed `POST /merchant/grants` body is in the ROUND_LOG; nothing has been sent.

## 4 · Digital products and platform economics
- **Etsy (US):** $0.20 listing + 6.5% transaction + 3% + $0.25 processing; Offsite Ads 12–15% (opt out at launch). Readings allowed with a physical or digital copy; outcome promises banned; disclose AI-assisted work.
- **Ko-fi (free plan):** 0% on tips, **5% on shop sales**, plus processor fees. Turn the Contributor programme off.
- **Gumroad:** 10% + $0.50 per direct sale, and a flat 30% on Discover sales; a $0.50 floor punishes sub-$10 items.
- **Sub-$10 net per sale** (computed in `LISTINGS.md` §1b): Ko-fi > Etsy > Gumroad at every price tested. A9 should not launch on Gumroad at $5.

## 5 · Costs (known and estimated)
| Cost | Amount | Note |
|---|---|---|
| Etsy fees | ~10.5% + $0.45 per sale | see §4 |
| Ko-fi | 5% + processor (free plan) | Gold removes the 5%; its monthly price is reported as $6 by some sources and $12 by others, so check the live page |
| Gumroad | 10% + $0.50 (+ processing, sources disagree whether included) | |
| NC LLC | $125 to file + $200/yr annual report | Synthesis §4; verify at filing |
| Print samples (P1, P5) | unknown | log as `SAMPLES` |
| Domain, email tool | optional; free tiers first | C3: MailerLite free or self-hosted listmonk |

## 6 · Timeline (from Plan §1, restated honestly)
| When | Milestone | Blocked by |
|---|---|---|
| Now | Taylor decisions (§8); ledger bootstrap | Taylor |
| ~Dec 2026 | 4 First Flame listings live; numerology demand reportedly peaks in January | listing photos + Taylor clicking publish |
| Month +1 | A4 vault build reviewed by Taylor; C2 page published | Taylor |
| Month +2 | POD pilot (after 1 logged sale) | first sale |
| June 2027 (est.) | next NC Artist Support cycle opens | confirm with the regional partner |
| Later | LLC → trademark → Kickstarter → nonprofit per Plan §4 gates | steady revenue |

## 7 · Merchant directives (for whoever operates the ledger)
1. Record every sale with `POST /merchant/ledger` (entity `SOLE_PROP`, decodes as `kind: SERVICE`, fees on the row). Every cost with `POST /merchant/expenses`.
2. Bootstrap the empty DB with `merchant.init_merchant_db()` (OpenCode round-3 item 2); `MERCHANT_DB` overrides the path.
3. Mount the merchant router in the live spine only when Taylor applies the proposed patch.
4. Leap Gate = trailing 6-month average `cash_position` ≥ `TARGET_NET_MONTHLY`, runway saved, and no source above 50% (LOOP.md §1).

## 8 · Open items
**Taylor:** (a) set `TARGET_NET_MONTHLY` and `RUNWAY_MONTHS` (keep them in `LOCAL_TARGETS.md`, uncommitted); (b) seller of record, sole prop or two-member LLC (E2); (c) VaaS yes or no (B1); (d) when to start a nonprofit; (e) publish C2; (f) rule on Year-1 letters (they stay out of products until you do).
**Verify with an advisor:** NC sales tax on digital goods sold outside Etsy; 1099-K thresholds; LLC and partnership choice.
**Missing evidence:** art inventory, ChatGPT export, whether `_INCOMING` is only a mirror (OpenCode).

*Creation is Sacred · Commerce is Mechanical · Layer: DISTILLED*
