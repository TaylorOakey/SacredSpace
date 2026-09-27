# ∆ IDEA BANK ∆ — Livelihood Loop

Scoring follows LOOP.md §4: **R**evenue ×2 · **S**peed ×2 · **H**ours · **C**apital · **A**udience · **V** sovereignty/canon, each 1–5, total out of 40.
Statuses: `RAW → SCORED → PROPOSED → EXPERIMENT → LIVE / KILLED / PARKED`. At most **3 EXPERIMENTS**.
Round 0 was seeded by Claude Code on 2026-09-26 from the repo, Drive (read-only) and web research. **Items marked 🔎 need OpenCode to confirm them locally.**

## Active experiments (max 3)

| Slot | Idea | Kill metric (checked at the date) | Review date |
|---|---|---|---|
| 1 | **First Flame (A1 + A2)**: GR∆M∆ Decode + 3 digital downloads on Etsy/Ko-fi | < 3 sales in the first 45 days after listing → rework the listings (photos/titles) once, then kill if still < 3 after another 45 | 45 days after the first listing goes live |
| 2 | **C2 Free Decode web page** as the funnel into paid decodes. Approved 2026-09-26; page built at `FIRST_FLAME/decode_web/` | < 100 visits or 0 paid upgrades in 60 days | publish date + 60 days |
| 3 | **A4 Sovereign Creator Vault template**. Approved 2026-09-26; spec at `A4_VAULT_TEMPLATE/SPEC.md` | < 5 sales in 60 days after launch | launch date + 60 days |

---

## A · Products

| ID | Idea | R | S | H | C | A | V | Total | Status | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | GR∆M∆ Name Decode, $11/$22/$33 | 2 | 5 | 4 | 5 | 4 | 5 | **32** | EXPERIMENT | `FIRST_FLAME/grama_decode.py` automates the Mini; Etsy allows readings with a digital copy ([policy](https://www.etsy.com/legal/prohibited/)). Round 2: parity with C2 page confirmed on "Taylor Oakey" (148/4/Builder/✦TAYL4∆); needs `merchant.py` on PYTHONPATH (not in `FIRST_FLAME/`) |
| A2 | Digital downloads (cipher print, wallpapers, journal pages), $7 | 1 | 5 | 5 | 5 | 2 | 4 | **28** | EXPERIMENT | Net per sale ≈ $5.88 Etsy / $6.15 Ko-fi (`FIRST_FLAME/LISTINGS.md` §1) |
| A3 | POD prints via Gelato/Printify (month 2) | 2 | 3 | 4 | 4 | 2 | 3 | **23** | SCORED | Crowded category; margin after fees ≈ $8–33 per item (`LISTINGS.md` §4) |
| A4 | **"Sovereign Creator OS" Obsidian vault template + setup guide**, $19–39: a packaged, de-personalised version of Taylor's nine-pillar system | 3 | 4 | 5 | 5 | 4 | 5 | **33** | EXPERIMENT | Templates sell at $5–39; Gumroad takes 10% + 2.9%; sellers need their own traffic source, and email drives 40–60% of sales ([source](https://insightraider.com/en/answers/what-digital-products-sell-best-on-gumroad)). Round 2: vault mapped (`RECURSION/local_vault_structure.md`, 161 folders, 0 private at depth ≤3); notebook source files exist in vault (`00_CUSTOM_INSTRUCTIONS_AND_SACRED_PROMPTS_v2`) |
| A5 | "Read the Grid": Arcana Grid primer PDF + print-and-play mini deck, $11–33 | 2 | 1 | 5 | 5 | 4 | 5 | **25** | RAW | REFUTED 2026-09-27: `09_SACRED_MARKET/arcana_grid/game_data.json` declares 78 cards but contains 0 card objects (major/minor are descriptor dicts). Needs enumeration + art + playtest first |
| A6 | Arcana Grid tabletop game on Kickstarter | 5 | 1 | 1 | 2 | 5 | 5 | **25** | PARKED | MasterPlan v2 needs 10 proof artifacts + a 1,000+ email list; gated by plan §4 |
| A7 | Jenga's Journey as a free webcomic → paid print volume | 3 | 1 | 1 | 3 | 5 | 5 | **22** | RAW | Season 1 script exists; needs an illustration plan (human-made vs. AI-assisted must be decided and disclosed) |
| A8 | Sacred Sprouts lore-tagged plants at local markets | 2 | 3 | 2 | 4 | 3 | 5 | **24** | RAW | Near-zero cost of goods from propagation (Market Master §05). Market-vendor permits and NC sales tax need checking |
| A9 | Cipher Puzzle Pack (printable GR∆M∆ puzzles), $5–9 on Gumroad | 1 | 4 | 5 | 5 | 2 | 5 | **27** | RAW | Round-2 archive find: 05-26 launch plan §1B (unbanked until now); same engine as A1, zero COGS |

## B · Services

| ID | Idea | R | S | H | C | A | V | Total | Status | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | Sovereign AI setup for small businesses (VaaS: $5k + $500/mo, or $333 sessions) | 5 | 3 | 1 | 5 | 3 | 4 | **29** | PARKED | Highest revenue per client; hours clash with the day job. **Taylor's open call** |
| B2 | Sacred Land Assessment (land stewardship + lore reading of a property) | 3 | 3 | 1 | 4 | 2 | 5 | **24** | RAW | Lore-to-Ledger stream 08; weekend-only |
| B3 | Healing Codex art licensing for wellness spaces, $111–333/yr | 2 | 2 | 4 | 5 | 3 | 5 | **25** | RAW | Needs a one-page offer and 5 outreach emails (Market Master §10) |
| B4 | Custom sigil art commissions, $55–111 | 2 | 4 | 2 | 5 | 3 | 5 | **27** | RAW | The natural upsell from a Deep Skry buyer |

## C · Audience & public eye (these feed every other lane)

| ID | Idea | R | S | H | C | A | V | Total | Status | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Build in public: the OS itself as content (short videos of the sigil terminal, decode reveals, the Legion build) | 1 | 4 | 3 | 5 | 5 | 5 | **28** | RAW | Product sellers without a traffic source rarely sell ([source](https://insightraider.com/en/answers/what-digital-products-sell-best-on-gumroad)) |
| C2 | **Free GR∆M∆ Decode web page**: vanilla JS, static, on GitHub Pages or a free HF Static Space; shows the Mini result and upsells Full/Deep | 2 | 4 | 5 | 5 | 5 | 5 | **32** | EXPERIMENT | Static Spaces are free; CPU Gradio Spaces now need a paid plan ([HF docs](https://huggingface.co/docs/hub/en/spaces-overview)). Port `calculate_gematria` to JS; no build tools (CLAUDE.md rule). Round 2: parity with A1 confirmed (same 5 values); SHOP links still empty (listings don't exist) |
| C3 | Sacred Grove email list + free Sacred Geometry PDF | 2 | 4 | 4 | 5 | 5 | 4 | **30** | RAW | Email drives 40–60% of digital-product sales (same source as C1). Tool: MailerLite free, or self-hosted [listmonk](https://github.com/knadh/listmonk) (AGPL, single binary) |
| C4 | Public lore garden: a curated slice of the Codex as a website via [Quartz](https://github.com/jackyzha0/quartz) on GitHub Pages | 1 | 3 | 4 | 5 | 4 | 5 | **26** | RAW | Needs a canon + privacy review of what's public. Quartz needs npm at build time, which conflicts with the CLAUDE.md "no build tools" rule for the browser extension; this is a separate site, so **Taylor decides** |
| C5 | Sacred Messages public edition: monthly letters to "the collective child", Ko-fi membership $7/mo | 3 | 3 | 3 | 5 | 4 | 4 | **28** | RAW | Market Deep Dive idea 03. Guardrail: the public letters are **not** about Iris and Asher; the private archive stays private. Round 2 FLAG: the 05-26 launch plan proposes excerpting Year-1 letters (stated on-disk as Iris+Asher material) into a zine/template pack — GATED on Taylor's explicit ruling before any Messages product advances |

## D · Open source & infrastructure

| ID | Idea | R | S | H | C | A | V | Total | Status | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | Open-source the reusable pieces (gematria/decode engine, merchant ledger, Sacred Chrome) under MIT + GitHub Sponsors | 1 | 3 | 4 | 5 | 4 | 5 | **26** | RAW | 0% fee on sponsorships from personal accounts ([GitHub docs](https://docs.github.com/en/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes)). The main gain is credibility for B1 and A4 |
| D2 | Etsy → `/merchant/ledger` order sync | 1 | 2 | 5 | 5 | 1 | 5 | **22** | PARKED | Only after ~20 manual orders ([etsy-python](https://pypi.org/project/etsy-python/1.2.0/)) |
| D3 | Beancount export from the merchant ledger | 1 | 2 | 5 | 5 | 1 | 5 | **22** | PARKED | Useful at the first tax season with real sales ([Beancount](https://github.com/beancount/)) |

## E · Structures & capital

| ID | Idea | R | S | H | C | A | V | Total | Status | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | NC Arts Council Artist Support Grant (individual artist, usually $500–2,000) | 1 | 3 | 3 | 5 | 2 | 5 | **23** | RAW | Regional deadlines ([NC Arts](https://www.ncarts.org/grants-resources/grants/grants-artists/artist-support-grants)). Funds the gear/art for A1–A5 |
| E2 | Seller-of-record decision: Taylor as sole seller vs. a Taylor + Jeanie two-member LLC | — | — | — | — | — | — | — | **DECISION** | Plan §4. Round 2: Taylor's Step-0 intent = Jeanie co-founder in BOTH entities; LLC not yet formed — record sales as SOLE_PROP until formation |
