# ∆ FIRST FLAME — Launch Listings v1 ∆
## Pillar 09 · Product #1 (GR∆M∆ Decode + digital downloads) · Product #2 (print-on-demand, month 2)

**Status:** DRAFT — ready for Taylor to edit and post. Nothing here is live yet.
**Operating mode:** sole proprietor, around 3–4 hours a week, Etsy + Ko-fi only.
**Ledger:** record every sale with `POST /merchant/ledger` (entity `SOLE_PROP`) and every cost with `POST /merchant/expenses`.

---

## 0. Platform rules that shape the copy (checked 2026-09-26)

- **Etsy allows readings, but not outcome promises.** Etsy's prohibited-items policy bans metaphysical services "that promise or suggest [they] will effect a physical change … or other outcome (e.g., love, revenge)". Readings that come with a physical or digital copy are allowed. So: **never** write "unlock your destiny", "attract", "heal", or "manifest" in Decode copy. Describe it as a creative, reflective reading. The disclaimer is already printed in every generated PDF.
- **AI disclosure.** If AI tools helped make any artwork, say so plainly in the description. This also settles the old "zero AI-generated imagery" vs. "AI-enhanced" contradiction: **be accurate, not absolute.**
- **Etsy fees (US):** $0.20 listing (it renews every 4 months, and again each time a sale uses up quantity), 6.5% transaction fee, and 3% + $0.25 payment processing. Offsite Ads take 15% of a sale they generate. It's optional below $10k/yr, so **opt out at launch.**
- **Ko-fi (free plan):** 0% on tips, **5% on shop and commission sales**, plus about 2.9% + $0.30 processing. **Turn off the "Contributor" programme**; new accounts are opted in by default and it adds another 5%. Gold ($12/mo) only pays off above about $240/mo in Ko-fi sales.
- **Re-checked 2026-10-06 (secondary sources; etsy.com, ko-fi.com and gumroad.com were unreachable from the research sandbox):** Etsy's $0.20 / 6.5% / 3% + $0.25 and Offsite Ads 12–15% ([Checkoutpage](https://checkoutpage.com/blog/etsy-fees)); Ko-fi free plan 5% on shop sales, Contributor on by default ([Ruzuku](https://www.ruzuku.com/learn/articles/ko-fi-pricing)). **Open conflict:** Ko-fi Gold is quoted at $6/mo by some sources and $12/mo by others, so read the live pricing page before relying on the $240 break-even. Nothing else moved.

## 1. Pricing and take-home per sale

The old docs disagreed ($11/$22/$33 vs. $111/$222). **Launch at $11/$22/$33.** It's low friction, earns first reviews, and the Mini is fully automated. Revisit $111+ only after 20+ five-star reviews.

| Product | Price | Etsy net | Ko-fi net (free plan, Contributor off) | Your time per order |
|---|---|---|---|---|
| Mini Decode | $11 | ≈ $9.51 | ≈ $9.83 | ~5 min (fully generated) |
| Full Decode | $22 | ≈ $19.46 | ≈ $19.96 | ~20 min (write lenses I + III) |
| Deep Skry | $33 | ≈ $29.42 | ≈ $30.09 | ~45 min (+ extended reading) |
| Digital download | $7 | ≈ $5.89 | ≈ $6.15 | 0 (instant download) |

Record the fees on each sale row so the ledger nets them out.

## 1b. Sub-$10 fee math (added 2026-10-06; needs checking against live fee pages)

Etsy = $0.20 listing (renews per sale) + 6.5% + 3% + $0.25. Ko-fi (free plan, Contributor off) = 5% + about 2.9% + $0.30. Gumroad direct = 10% + $0.50 ([Conversion Pro](https://conversionproplus.com/blog/gumroad-fees-in-2026-is-there-a-better-alternative)); sources disagree on whether card processing is already inside that figure, so both cases are shown.

| Price | Etsy net | Ko-fi net | Gumroad net (10% + $0.50 only) | Gumroad net (+ 2.9% + $0.30) |
|---|---|---|---|---|
| $5 | $4.08 (81%) | $4.31 (86%) | $4.00 (80%) | $3.56 (71%) |
| $7 | $5.89 (84%) | $6.15 (88%) | $5.80 (83%) | $5.30 (76%) |
| $9 | $7.70 (86%) | $7.99 (89%) | $7.60 (84%) | $7.04 (78%) |

**Read:** Ko-fi wins at every price; Gumroad's flat $0.50 hurts most at $5. Gumroad is also 30% on Discover sales. Its one advantage is acting as merchant of record for sales tax (see the NC tax note in the ROUND_LOG). Launch A9 on Ko-fi/Etsy, not Gumroad.

## 1c. Market evidence for the Decode listing (2026-10-06)

- Aggregator data ([ListifyAI "numerology"](https://www.listifyai.net/keyword/numerology), [Kupkaike "name meaning download"](https://kupkaike.com/niche/name-meaning-download)): "numerology" has about 18,300 listings with a median price near $9.50 and page-one shops holding a median of ~1,400 reviews; "name meaning download" has about 6,500 listings at $5–13, flagged as a crowded head market. Demand peaks in January.
- **Implication:** the $11 Mini sits just above the median for plain name-meaning PDFs. It needs the sigil art and the visible differentiator in the first photo, and you have no reviews against incumbents holding 1,000+. Don't compete on the head term.
- **05-26 price points** (from OpenCode's archive pass: $9–15 map, $15–25 custom decode, $7–12 rulebook) bracket the $11/$22 tiers, so no change is forced. The $33 Deep Skry has no market comp yet.
- **Not done:** I could not open individual Etsy listings (etsy.com blocked), so there is no 10-listing comp table and no evidenced long-tail keywords. The 13 tags stay as drafted. OpenCode/Taylor: open Etsy search for "name meaning", "name numerology" and "personalized name reading" and record the top 10 (price, reviews, format) and the "related searches" suggestions.

---

## 2. Listing — GR∆M∆ Name Decode (one listing, 3 variations)

**Title (140 max):**
`Personalized Name Numerology Reading · Gematria Name Meaning PDF · Custom Sigil Art · Digital Name Decode Gift`

**Variations:** Mini Decode $11 · Full Decode $22 · Deep Skry $33
**Personalization field (required):** "Full name as you want it decoded (and a nickname if you'd like one included)"

**Description:**
```
Every name carries a pattern. The GR∆M∆ Name Decode reads the letters of your
name through five lenses and returns it to you as a keepsake PDF — part
numerology, part art, part story.

WHAT YOU RECEIVE
• MINI ($11) — Gematria Pulse (your letter-by-letter number map and soul tone),
  Archetypal Thread (the archetype your number carries, and its shadow), and your
  Core Identity Sigil in the S∆CR3DS!G∆L cipher.
• FULL ($22) — everything in Mini, plus Root Meaning (the history of your name)
  and Elemental Image (the element and image your name evokes).
• DEEP SKRY ($33) — everything in Full, plus a hand-written extended reading.

HOW IT WORKS
1. Choose your tier and type your name in the personalization box.
2. Your PDF is made from that name — Mini within 2 days, Full/Deep within 5.
3. It's delivered as a digital file. Nothing ships.

GOOD FOR: name-meaning gifts, baby-name keepsakes, journaling prompts, altar or
desk art, anyone who loves numerology, symbols and story.

Please note: this is a creative and reflective reading for inspiration and
self-reflection. It does not predict events or promise any outcome.

Made by hand by ∆∆∆O∆K3YTREE∆∆∆ · SacredArcana Studios.
```

**13 tags:** `name meaning` · `numerology reading` · `gematria` · `name numerology` · `personalized gift` · `custom sigil` · `name meaning gift` · `numerology gift` · `baby name meaning` · `spiritual gift` · `digital download` · `sacred geometry` · `personalized pdf`

**Fulfillment SOP (per order):**
```bash
python3 09_SACRED_MARKET/FIRST_FLAME/grama_decode.py "<Name>" --tier mini --out "<name>_mini.html"
# Full/Deep: add --element AIR --meaning "..." --image "..." [--narrative-file reading.md]
# Open the .html → Print → Save as PDF → attach to the order.
# Then log it: POST /merchant/ledger {sale_date, entity:"SOLE_PROP", channel:"ETSY",
#   kind:"SERVICE", gross_usd:11, fees_usd:1.50, external_ref:"<Etsy order #>"}
```
(Decodes are services, so use `kind: SERVICE`. First Flame counts **products** only; that's deliberate, so the milestone measures the product engine.)

**Proof content for the listing photos:** run your own OAK9 self-decode through the generator and screenshot it. That is the demo the Deep Dive called for.

---

## 3. Listings — three digital downloads (instant download, $7 each)

Each needs one art file Taylor already has, plus 3 mockup images made in Canva.

| # | Product | Source asset | Title |
|---|---|---|---|
| D1 | **S∆CR3DS!G∆L Cipher Alphabet Print** | cipher table (A→∆ E→3 I→! O→0 S→$ T→7) set as a printable 8×10 / A4 | `Sacred Cipher Alphabet Printable · Mystic Symbol Wall Art · Altar Decor Digital Print · 8x10 A4` |
| D2 | **Auroric Mandala Wallpaper Pack** | 3 mandalas → phone (1170×2532) + desktop (3840×2160) | `Sacred Geometry Mandala Wallpaper Pack · Phone & Desktop Background · Spiritual Aesthetic Digital Download` |
| D3 | **Elemental Glyph Journal Pages** | 4 element glyphs as printable journal or prompt pages | `Elemental Journal Pages Printable · Earth Water Fire Air Prompts · Spiritual Journaling Digital Download` |

Description skeleton (reuse for each):
```
[One sentence: what it is.] [One sentence: what it's for.]
INCLUDED: [files, sizes, formats]. Instant download — nothing ships.
Personal use only. [If AI tools assisted any artwork: "Designed by me with
the help of digital and AI tools."]
Part of the SacredSpace world by ∆∆∆O∆K3YTREE∆∆∆.
```
Mirror all three on Ko-fi Shop. Keep the free Sacred Geometry PDF as the **email sign-up gift** instead of a listing (month 2).

---

## 4. Month 2 — Product #2: print-on-demand prints (5 listings)

**Only start once at least 3 listings from sections 2 and 3 are live and one sale is logged.**

| # | Product | Fulfiller | Price | Rough margin* |
|---|---|---|---|---|
| P1 | Auroric Mandala fine art print 8×10 | Gelato | $33 | ~$20 |
| P2 | Auroric Mandala fine art print 16×20 | Gelato | $55 | ~$33 |
| P3 | OakeyTree Sigil sticker pack | Printify | $14 | ~$8 |
| P4 | Elemental Glyph tote | Printify | $22 | ~$10 |
| P5 | Auroric Mandala canvas 12×16 | Gelato | $55 | ~$29 |

\*Margin after fulfillment and Etsy fees, **before** shipping differences. Price-check every product in the Gelato/Printify dashboard before listing; these are the old docs' base costs, not quotes.

**Order one sample of P1 and P5 first** (log them as `SAMPLES` expenses). They double as photo props. Don't list what you haven't seen printed.

---

## 5. Weekly rhythm (fits around a day job)

| When | What | Time |
|---|---|---|
| Once a week | Fulfil decode orders · log sales and expenses · check Etsy stats | 60–90 min |
| Once a week | One new listing **or** one improvement (photos, tags, title) | 60 min |
| 2–3× a week | One short post (decode reveal, sigil close-up, mandala process) | 15 min each |
| Monthly | Read `/merchant/ledger` · keep what sells, drop what doesn't | 30 min |

*Creation is Sacred · Commerce is Mechanical*
