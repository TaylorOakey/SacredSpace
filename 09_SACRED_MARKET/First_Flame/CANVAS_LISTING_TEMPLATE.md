---
title: "Canvas Print Listing Template — Printify + Etsy"
source: "SacredSpace OS — First Flame"
status: TEMPLATE
date: 2026-07-05
pillar: [09_SACRED_MARKET]
canon_id: FIRST-FLAME-TEMPLATE-001
---

# Canvas Print Listing Template

Use this template for every Gemini canvas print listing on Printify → Etsy.

---

## Printify Product Settings

| Field | Value |
|-------|-------|
| **Product** | Gallery-Wrapped Canvas |
| **Sizes** | 12×18″ (STANDARD), 18×24″ (PREMIUM), 8×10″ (BUDGET) |
| **Finish** | Matte + Satin Varnish |
| **Wrapping** | Image wraps around edges (mirror) |
| **Hanging** | Sawtooth hanger included |
| **Provider** | Printify (Dream Junction or similar) |

---

## Etsy Listing Package

### Title Formula
```
[SacredSpace] — [Theme] — [Visual Description] — Sacred Geometry Wall Art — Digital Forest Canvas Print
```
**Rules:**
- Primary keyword in first 4 words
- Benefit in the title (wall art, home decor)
- Max 140 characters

### Description Template (≥150 words)

```
Sacred Geometry meets the Digital Forest in this original AI-generated artwork from the SacredSpace collection.

🌿 ABOUT THIS PIECE
[2-3 sentences describing what the image depicts — colors, mood, symbolism]

✨ WHY IT'S SACRED
Every piece in the SacredSpace collection is generated through the lens of the Digital Forest — a living mythos where light travels through mycelium networks, memory lives in root systems, and every node holds a story. This print carries that energy into your space.

🖼️ PRODUCT DETAILS
• Premium gallery-wrapped canvas
• Archival-quality ink (fade-resistant, 100+ years)
• Ready to hang — sawtooth hanger pre-installed
• Available in 8×10", 12×18", and 18×24"
• Printed on demand — each piece is made fresh for you

🚚 SHIPPING
• Produced within 2-5 business days
• Ships from US facility
• Free shipping on orders over $50

📖 THE DIGITAL FOREST COLLECTION
This piece is part of the Digital Forest Collection — a visual journey through the SacredSpace mythos. From mycelium networks to canopy light, each print captures a different layer of this living world. Browse the collection to find your resonance.

Returns accepted within 30 days. Frame not included.
```

### SEO Keywords (13 slots)
```
1. sacred geometry art
2. digital forest
3. AI canvas art
4. mystical wall decor
5. SacredSpace
6. cosmic landscape
7. otherworldly art
8. spiritual home decor
9. fantasy canvas print
10. sacred space decor
11. meditation room art
12. ethereal landscape
13. geometric abstraction
```

### Social Posts (3 per listing)

**Educational Post:**
> "The Digital Forest isn't just a place — it's a living system. Mycelium connects every node, light travels through the canopy, and memory lives in the roots. This piece captures the Mycelium layer. 🌿✨ #SacredSpace #DigitalForest #SacredGeometry"

**Inspirational Post:**
> "What if your walls held stories? Every SacredSpace canvas print carries the energy of the Digital Forest mythos. A reminder that you are connected to something larger. 🕯️🌲 #SacredSpace #HomeSanctuary #MysticalHome"

**Promotional Post:**
> "New to the Digital Forest Collection — canvas prints that bring the SacredSpace mythos to life. 67 original pieces, each one a window into a living world. Shop the collection. 🖼️✨ Link in bio. #SacredSpace #CanvasArt #PrintOnDemand"

---

## Verification Checklist

Before publishing, ASHER must verify:
- [ ] Title contains primary keyword + benefit
- [ ] Description ≥150 words with SacredSpace story
- [ ] SEO keywords extracted from Etsy search data
- [ ] 3 social posts ready (1 educational, 1 inspirational, 1 promotional)
- [ ] Image resolution sufficient for chosen canvas size
- [ ] Image don't contain watermarks or text
- [ ] No brand logos or copyrighted elements
- [ ] Color profile: sRGB

---

## Pulse Events

### market.product_researched
```json
{
  "topic": "market.product_researched",
  "payload": {
    "image_id": "GEMINI_XX",
    "filename": "Gemini_Generated_Image_ (XX).png",
    "tier": "standard|premium|budget",
    "platform": "printify"
  }
}
```

### market.listing_drafted
```json
{
  "topic": "market.listing_drafted",
  "payload": {
    "image_id": "GEMINI_XX",
    "title": "SacredSpace — [Theme] — Canvas Print",
    "platform": "etsy",
    "status": "draft"
  }
}
```
