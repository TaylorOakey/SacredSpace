# ∆ SACRED MARKET — INCOME, NONPROFIT & GRANTS SYNTHESIS ∆
## Pillar 09 · Survey of every money-related thread in the repo, with suggested actions

**Status:** DISTILLED. This is an organized reading of existing docs plus recommendations. It is **not** a Canon Gate ruling and makes no decisions for Taylor.
**Compiled:** 2026-09-26
**Scope:** everything in the repo that touches the Sacred Market, cash flow, money, grants, the LLC, the 501(c)(3), crowdfunding, or using SacredSpace to bring in income.
**Not legal or tax advice:** Part 4 lists factual errors in the existing plans. Before filing anything, confirm those points with a CPA or nonprofit attorney. The Thomas Hub advisor already named in the plan is a free place to start.

---

## 0. The short version

1. **There is plenty of planning and no recorded income.** Every financial milestone in the repo is still `PENDING`. The newest dated money plan runs **May 12 – Aug 3, 2026**, and those dates have passed. Nothing in the repo says whether the LLC was formed, whether the 501(c)(3) was filed, whether the Kickstarter launched, or whether the Etsy store has made a sale. **Before anything else, Taylor needs to record the actual state** (§5, step 0).
2. **The nonprofit filing plan has real errors.** It names an IRS form that does not exist ("1023-N"). It gives the nonprofit an "operating agreement" with 50/50 ownership, which nonprofits cannot have. It describes POD income as tax-exempt UBI. And the Kickstarter tiers include a revenue share, which Kickstarter does not allow. If none of this has been filed yet, fix it first. If it has been filed, check what actually went in (§4).
3. **The best-paid income lane is barely documented.** `merchant.py` already defines **VaaS clients at a $5,000 setup fee plus a $500/month retainer**, and no doc mentions it anywhere. One VaaS client brings in more than the whole First Flame milestone ($1,111). It also draws directly on Taylor's 15 years in ops plus the AI Engineering work.
4. **Kickstarter is aimed at the wrong product.** The plan crowdfunds "a sovereign personal OS", which is abstract and hard to turn into rewards. The **Sacred Arcana tabletop game** already has a box cover, rules card, mats, token sheet and 78-card deck in `06_AGENT_LAYER/ui_kits/web/`. Tabletop is the kind of project Kickstarter backers expect. It needs playtesting first: its own spec marks **Tested: ✗**.
5. **"Grants" is a label with nothing behind it.** It appears only as "grant pipeline" in the architecture docs and as one phone call to EDPNC. No funders, deadlines or eligibility research exist. The quickest real path is **fiscal sponsorship**, which lets grants flow before any IRS determination letter.

---

## 1. Where the money material lives

| Location | What it is | Signal vs. noise |
|---|---|---|
| `09_SACRED_MARKET/SacredSpace_Revenue_Operations.md` | The **1111 Revenue Engine** manual: revenue paths, 4 phases, product specs, fulfillers, storefronts, ads, cadence, 8 design families | **High.** This is the best operational doc. Three near-duplicates sit in `CASHFLOW_MASTER/` (`SacredSpace_Revenue_Operations.md`, `REVENUE_…`, `SacredSpace_OS_Revenue_Operations.md`), and they differ slightly from this root copy. |
| `CASHFLOW_MASTER/SACREDSPACE_POD_OPERATING_MANUAL_v1.md` | POD brand rules, product ladder, Etsy→Shopify channel map, listing formulas, email flows, KPI schema, 30-day launch, failure modes, **Institutional Lane** | **High.** Duplicate: `_v1_2.md` |
| `CASHFLOW_MASTER/SACREDSPACESHIP_LAUNCH_PROTOCOL_PRINTABLE.md` | Plan dated May 6, 2026, marked CANON: $45k Kickstarter, 501(c)(3) filing path, LLC + 501(c)(3) tax structure, risk register | **High, but see §4.** Contains the legal errors. |
| `CASHFLOW_MASTER/Sacredspace_strategic_roadmap_and_launch_plan.md` | Raw chat export (96 KB) that produced the launch protocol, including the "operating agreement" template and Kickstarter tier copy | Source material. Same errors. |
| `CASHFLOW_MASTER/Financial_Dashboard.md`, `First_Flame_Launch.md`, `A_Sacred_Space_POD.md`, `ECONOMY_Overview.md` | Vault exports: milestone table, First Flame checklist, pricing model | Useful, but the numbers conflict (§3) |
| `CASHFLOW_MASTER/CORE_AXIOM_Nine_Pillar_Architecture_v1.md` §09 | Pillar law: *"Revenue serves the mission — the mission is never sacrificed for revenue."* North Star: **Sacred Little Forest** land | Mission anchor |
| `CASHFLOW_MASTER/GEMINI_SACREDSPACE_ASSIMILATION_v1.md` Part 6 | Two-entity summary, advisor contacts, the delivered "Nonprofit Startup Guide" and "Crowdfunding Operator Manual" HTML builds (these builds are **not in this repo**) | Index |
| `CASHFLOW_MASTER/CROSS_AI_PROTOCOL_v1.md`, `SACREDTAG_PROTOCOL.md` | `NONPROFIT ONLY` / `REVENUE ONLY` session tags | Governance only |
| `CASHFLOW_MASTER/deep-research-report.md` | Generic "8 AI passive income strategies" article | Low. Nothing specific to SacredSpace. |
| `Sacred_Symphony_Architecture.md`, `SacredSpace_OS_Architecture_Manifesto.md` | "Grant pipeline" listed as a LangGraph/Sacred Score workflow | The only grant mentions, and they are aspirational |
| `systems/fastapi/merchant.py` | **Code that runs:** artifact catalog (DRAFT→SEALED), listing generator, gematria/sigil, **VaaS client table** | Real, but it has no Etsy/Printify/Gelato API calls (only enum values) and **no orders or sales table** |
| `economy/studios/forge.py`, `pinterest_engine.py` | Turns lore into social-post signals; Pinterest search helper | Hardcoded `D:/` Windows paths |
| `06_AGENT_LAYER/ui_kits/web/*` and `04_SACRED_CODEX/ARCANA_BOARD_SPEC.md` | Sacred Arcana game: box, rules, mats, tokens, cards | **No doc treats this as a product yet** |
| `09_SACRED_MARKET/NOTEBOOKLM_UPLOAD/` | ~35 copies of the files above, renamed for NotebookLM | Mirror only |

**Corpus health:** `CASHFLOW_MASTER/` holds about 70 files. About 25 are `_2`/`_1` duplicates. Four are 200 KB raw dumps (`Untitled_document*.md`, `SACRED_WEB_SCRAPPER.md`, and `SACREDSPACE_GEMINI_IMAGES.md`, which is mostly base64 images). About 10 are actually about money. The rest are general OS/context docs that the keyword scan swept up because they mention "revenue" once.

---

## 2. The income lanes as the docs describe them

| # | Lane | Entity | Status in the docs | Upside | Effort to first dollar |
|---|---|---|---|---|---|
| A | **POD, "A SACRED SPACE" / 1111 Flow Engine**: Etsy → Printify/Gelato/Printful, 8 design families, 3 drops | LLC | Fully specified. "Etsy live" is claimed once, but First Flame is still "execution pending" | $111–$444/mo steady state (the docs' own target) | Low cost, slow to build |
| B | **Kickstarter, $45k**: "Sovereign Personal OS" | Unclear (the plan mixes LLC and nonprofit) | Planned for June 9 – July 9, 2026. Outcome unknown | $45k one-time | High. Needs an audience first |
| C | **Open Grove**: membership/cohort tuition, 50 creators over 6 months | 501(c)(3) | Kickstarter line item only ($18k) | Recurring | Medium |
| D | **VaaS**: sovereign-vault setup plus retainer | LLC | **Code only**: `merchant.py` `vaas_clients` table, $5,000 setup + $500/mo | **Highest per unit** | Low. Sells existing skills |
| E | **Institutional / Healing Codex**: wellness-space installation sets, $500–$2,000 each | LLC | "Seed planted" and deferred until after $1,111 | Medium, B2B | Medium |
| F | **Signed limited editions**: 11 units at $250–$333 | LLC | Planned for Drop 03 | ~$3k per drop | Low |
| G | **Sacred Arcana tabletop game** | LLC | Design artifacts exist, but it is not yet framed as a product | High, via crowdfunding | High. Needs playtesting and manufacturing quotes |
| H | **Grants** | 501(c)(3), fiscal sponsor, or Taylor as an individual artist | A word in two architecture docs | Varies | Medium, and depends on the calendar |
| I | **Affiliate / licensing**: Healing Codex licensing, 10–20% affiliates | LLC | Phase 3–4 | Passive add-on | Low |

---

## 3. Numbers that don't reconcile

Resolve these once, in one ledger, before any public figure goes out.

| Claim | Where | Conflict |
|---|---|---|
| First Flame = **$1,111 cumulative profit** | Revenue Ops, POD Manual | — |
| First Flame = **$736 net (~32 sales)** | `Financial_Dashboard.md`, `First_Flame_Launch.md` | Same name, different number. 32 canvases × $35 margin = $1,120 gross margin, not net |
| Canvas 12×16 margin **$35** at $55–70 | Revenue Ops | `A_Sacred_Space_POD.md`: 12×16 at $55 → **$37**. `First_Flame_Launch` uses Printify for canvas, while Revenue Ops says Gelato |
| Margins | All POD docs | None say whether Etsy fees are included (listing $0.20 + 6.5% transaction + payment processing, plus Offsite Ads on some sales). On a $55 canvas, that is about $5–6 per sale before ads. **Check each margin after fees.** |
| Kickstarter tiers | Launch Protocol | The 5 tiers add up to **184 backers = $31,874**, which is **$13k short** of the $45k goal. The text then says "150 backers → $36.7k", which contradicts its own table |
| Nonprofit revenue | Roadmap | Year 1 projected at **$50k–$100k**, which rules out Form 1023-EZ (see §4) |
| Milestones | `Financial_Dashboard.md` | $500/mo → $1k/mo → $2.5k reinvest → **$10k Sacred Forest Fund**. The land stretch goal in the Kickstarter plan assumes a **~$100k parcel** |

---

## 4. Nonprofit and legal: what's wrong in the current plan

The plan is **SacredArcana Studios LLC** (commercial) plus **SacredSpace Sanctuary, Inc.**, an NC 501(c)(3) run with co-creator Jeanie Leaf, with advisors at Thomas Entrepreneurship Hub and EDPNC. The two-entity idea is sound. Several details are wrong:

| # | What the docs say | What's actually true | Why it matters |
|---|---|---|---|
| 1 | File **"IRS Form 1023-N"**: 8 pages, $275, approval in 2–4 weeks | **No Form 1023-N exists.** The options are **Form 1023-EZ** ($275; only for organizations projecting ≤ $50k annual gross receipts in each of the next 3 years and ≤ $250k in assets) or the full **Form 1023** ($600). Both are filed online through Pay.gov. ("990-N" is the small-org *annual* e-Postcard, which is probably where the confusion started.) | The plan's own Year 1 projection ($50–100k) plus a $45k Kickstarter **fails the 1023-EZ eligibility test**, so the full 1023 is the likely form. Filing an EZ you don't qualify for risks the exemption later. |
| 2 | An "**Operating Agreement**" giving Taylor and Jeanie **50% ownership** each of the nonprofit | **Nonprofits have no owners.** A 501(c)(3) is governed by **Articles + Bylaws + a Board**. Operating agreements belong to **LLCs**. | Ownership language in nonprofit documents is a red flag at the IRS. If Jeanie is meant to co-own something, that belongs in the **LLC's** operating agreement, which is a separate decision for Taylor. |
| 3 | "Unrelated Business Income (POD sales): **tax-exempt status**" | UBI is **taxable**. Form 990-T is required once gross UBI reaches $1,000. Passive **royalties** are generally excluded from UBTI, but not because they are "tangential to mission" as the doc argues, and there are control-based exceptions. | This is the core of the LLC↔nonprofit money flow. Have a CPA design it: a plain donation from the LLC is simplest, and royalty or licensing arrangements need proper structuring. |
| 4 | Board = Taylor + Jeanie + 1 advisor; founders paid $18k (50% FTE each) from campaign funds | Insider-controlled boards that pay their own members, next to a founder-owned LLC doing business with the nonprofit, raise **private benefit / excess benefit** issues. Form 1023 asks about compensation and related-party dealings directly. | Add **independent** directors, set founder pay through the conflict-of-interest policy with interested members abstaining, and put every LLC↔nonprofit agreement in writing at market terms. |
| 5 | The Kickstarter "Partner" tier ($500) includes **revenue share**; the "Legacy" tier offers **first right of refusal on land** | Kickstarter's rules **prohibit financial returns or revenue sharing** and prohibit raising money for charities. Reward pledges are purchases, not donations. | Run the Kickstarter under the **LLC** for a **concrete product**, and remove the revenue-share and land-rights promises. Nonprofit donations go through a donation platform or a fiscal sponsor. When a gift over $75 gets something back, the donor must be told in writing how much is deductible. |
| 6 | The mission is "**land stewardship**" in some docs (`CORE_AXIOM`, `PROJECT_INSTRUCTIONS`, `GEMINI_ASSIMILATION`) and "**community, learning, spiritual stewardship**" in others (Launch Protocol, Roadmap) | The IRS evaluates **one** stated purpose, so the charitable/educational purpose has to be coherent. | Unify it into one mission sentence. Suggested frame: *educational + environmental stewardship*, with Open Grove / Learning Spine as the education program and Sacred Little Forest as the land program. |
| 7 | NC Articles fee "$50 + $25 expedited" | Not verified against the current NC Secretary of State fee schedule | Check sosnc.gov. NC also has **charitable solicitation licensing** rules (with a small-organization exemption); confirm before any public fundraising. |
| 8 | EDPNC is the "grant/funding angle" | The EDPNC number in the docs (1-800-328-8443) is **Business Link NC**, a small-business support line. It is good for the **LLC** (free counseling, NC Small Business Center referrals) and is not a nonprofit grant source. | Keep the call, but aim it at the LLC. |

---

## 5. Recommended actions, in order

### Step 0 — Record what actually happened (1 hour, blocks everything else)
Answer these in the ledger (`CLAUDE.md` Open Queue or a new `09_SACRED_MARKET/STATUS.md`):
- [ ] Does **SacredArcana Studios LLC** exist? State, EIN, and business bank account?
- [ ] Was anything filed for **SacredSpace Sanctuary**? Which form, on what date, current status?
- [ ] Did the **Kickstarter** launch? What was the result?
- [ ] Is the **Etsy** shop live? How many listings, and lifetime sales?
- [ ] Is **Jeanie Leaf** still a co-founder, and in which entity: the LLC, the nonprofit, or both?
- [ ] Monthly burn today: Maestro tuition, tools, APIs.

### Step 1 — Cash in the next 30–60 days: lead with VaaS, keep POD running
- **Productize VaaS.** Write a one-page offer: *"Sovereign AI Vault — local-first knowledge system + agent layer, set up in 2 weeks."* Target solo practitioners, small studios, and ops-heavy small businesses. The schema already prices it at **$5,000 + $500/mo**. Consider **2–3 discounted pilot clients** in exchange for case studies. A single client is worth more than First Flame. This is the lane that pays for the Maestro path.
- **POD: finish First Flame instead of redesigning it.** The manuals are complete, so follow `SACREDSPACE_POD_OPERATING_MANUAL_v1.md` Part VIII as written. Use one First Flame definition ($1,111 **profit after platform fees**) and one tracking sheet.
- **Pull the Institutional Lane forward.** One Healing Codex installation ($500–$2,000) equals about 15–60 poster sales. A PDF lookbook and 10 outreach emails to local yoga, therapy and integrative-medicine spaces is a small test.

### Step 2 — Fix the structure before filing (or before amending)
- Hold a 1-hour review with Thomas Hub or a CPA using the §4 table as the agenda.
- Choose **1023 vs. 1023-EZ** using honest 3-year projections.
- Replace the "operating agreement" with **bylaws + conflict-of-interest policy + board roster**, including ≥ 1–2 independent directors.
- Write the **one-sentence mission**.
- Decide the LLC→nonprofit flow. A simple **annual % donation** is the easiest to defend.
- Keep the entities separate in practice: separate bank accounts, and tag every revenue record with its entity.

### Step 3 — Grants, starting with lanes that don't need a determination letter
- **Fiscal sponsorship:** an existing 501(c)(3) (arts, environmental, or community-foundation sponsor) takes in grants and donations for the project, usually for a 5–10% fee. This unblocks grants **now**, while the IRS application is pending or even before it is filed.
- **Taylor as an individual artist:** artist-support grants (for example the NC Arts Council's regional artist programs and local arts councils) often fund individuals directly, with no nonprofit needed. This fits Jenga's Journey, Sacred Messages, and the Arcana art.
- **After the determination letter:** the local community foundation (in NE NC, the NC Community Foundation's county affiliates), environmental/land-stewardship funders for Sacred Little Forest, and education funders for Open Grove.
- **Build the pipeline the architecture describes:** a `grants` table (funder, program, entity eligible, amount, deadline, status, docs) in the local merchant DB, surfaced through FastAPI. That makes the "grant pipeline" in the Sacred Score layer real and keeps it local-first.
- Check every funder, deadline and eligibility rule against the funder's site. None of this is verified in the repo yet.

### Step 4 — Re-scope crowdfunding around the game
- Move the Kickstarter to the **Sacred Arcana tabletop game** (LLC): starter set, Oracle deck, mats, tokens. Most of the visual assets exist.
- First: playtest (the spec says Tested ✗), get manufacturing and fulfillment quotes, and build a pre-launch follower list.
- Make the tiers add up: they should cover the goal **after** Kickstarter fees, manufacturing, shipping and VAT.
- The OS, Open Grove and land fund become the story, **not** the rewards.

### Step 5 — System work (AURORA can do this on request)
- [x] Add a `sales` table and `GET/POST /merchant/ledger` to `merchant.py`. Every row is tagged by entity (`LLC | NONPROFIT | PERSONAL | FISCAL_SPONSOR`), channel and kind. The table is append-only: reversals are `REFUND` rows, and a duplicate platform order id is rejected. `net_usd` is computed as gross − fees − COGS. The GET response includes First Flame progress, measured as cumulative LLC product net against $1,111.
- [x] Add a `grants` table plus `GET/POST /merchant/grants` and `POST /merchant/grants/{id}/status`, covering the pipeline from RESEARCH to AWARDED/DECLINED, open deadlines coming due, and requested vs. awarded totals.
- [ ] **Found while wiring the above:** `systems/fastapi/main.py` imports `grant_hunter` and `flow_tracker` (routes `/grant-hunter`, `/flow-tracker`, `/flow-dashboard`), but neither module exists in this repo or its git history. So `main.py` can't start from a fresh clone. They probably exist only on D:. Commit them, or decide whether `/merchant/grants` and `/merchant/ledger` replace them, so there aren't two grant pipelines and two money ledgers.
- [ ] Consolidate `CASHFLOW_MASTER/`: keep about 8 canonical money docs and move duplicates and raw dumps to `archive/`. This is a Canon Gate call, so it needs Taylor's go-ahead.
- [ ] Fix the `D:/` hardcoded paths in `economy/studios/*.py` (same pattern as the 2026-05-29 spine fix).
- [ ] Correct `CLAUDE.md`'s merchant route: it lists `/merchant-sacred-artifacts`, but the code mounts `/merchant`.

---

## 6. Open questions only Taylor can answer

1. Is the nonprofit still a priority now, or does it wait until the LLC brings in steady cash? (The docs' own risk register already allows the LLC to go first.)
2. Is VaaS something Taylor wants to sell? It's the strongest financial lane, but it is service work, not creative work.
3. What is Jeanie's current role, and in which entity?
4. Does the Sacred Little Forest land goal stay the 5-year North Star, and at what budget?

---

*Creation is Sacred · Commerce is Mechanical · Layer: DISTILLED*
*Ground. Consolidate. Deploy. Document. Repeat.*
