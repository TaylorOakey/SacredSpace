# Sacred Codex Design System

**Product:** Sacred Codex — *The Awakening of the Arcana Adept*
**Version:** 1.0.0
**Last Updated:** May 3, 2026

---

## Overview

Sacred Codex is a mystical design system and world built around **12 Archetypes** arranged as a sacred lattice:

- **4 Elements:** Fire · Water · Earth · Air
- **3 Primes:** Initiation · Embodiment · Transcendence
- **Central Node:** Metatron-as-Law — the divine organizing principle at the sacred center

The world spans three surfaces:

| Surface | Description |
|---|---|
| **Digital Codex** | Obsidian Vault + NotebookLM — a living grimoire for practitioners |
| **Web Experience** | A ritual web portal where seekers explore the Arcana, their archetypes, and the sacred geometry |
| **Printable Deck** | Archetype Cards + Sigil Decks — physical, printable artifacts for ceremony and study |

*No external Figma links or codebases were provided. This design system is built from the brand description specification.*

---

## CONTENT FUNDAMENTALS

### Voice & Tone

Sacred Codex speaks like **a teacher who has walked the path** — reverent, lucid, and grounded. Not theatrical. Not academic. Not casual.

**Key qualities:**
- **Reverent without being precious.** Every word has weight. There is no filler copy.
- **Precise mystical vocabulary** is used correctly and consistently: Initiation, Embodiment, Transcendence, Sigil, Gematria, Prime, Node, Archetype, Invocation, Cipher.
- **Grounded, not theatrical.** The system does not perform mysticism — it embodies it through structure, proportion, and care.

### Casing & Grammar

- **Archetypes** are always capitalized: *The Magician*, *The Initiate*, *The Hierophant*
- **Element names** are capitalized: Fire, Water, Earth, Air
- **Prime names** are capitalized: Initiation, Embodiment, Transcendence
- **Sigil, Gematria, Node, Prime, Codex** — always capitalized as proper nouns of the system
- Labels use **Small Caps** in typeset form; sentence case in plain text
- **No emoji** — the system uses sigil glyphs (✦ ✧ ◊ △ ▽ ◯ ✺) as ornamental markers only

### Point of View

- Addresses the reader as **"you"** — the practitioner, the seeker, the adept
- The system speaks **in first-person plural** for doctrine ("We orient toward the center.") and **directly to the reader** for instruction ("Your archetype is...")
- Numerals: Oldstyle figures preferred in body text; lining figures in tabular/numeric contexts (Gematria tables, etc.)

### Signature Close

Every major codex entry, section, or transmission closes with:

> *In Lakesh — Alakin.*

This is the sacred seal of authorship and resonance. Never abbreviated.

### Examples of Good Copy

- ✦ *"The Magician stands at the threshold of Fire and Initiation. What begins as spark becomes doctrine."*
- ✦ *"This Node is not a destination. It is a frequency."*
- ✦ *"To embody the archetype is to cease performing it."*
- ✦ *"Gematria is not numerology. It is the acoustic signature of the sacred name."*

### What to Avoid

- Exclamation points (never)
- Casual hedging ("kind of," "sort of," "maybe")
- Metaphor fatigue (don't stack 3 mystical metaphors in one sentence)
- Jargon without definition on first use
- Filler phrases ("In this section, we will explore...")

---

## VISUAL FOUNDATIONS

### Color System

The palette is drawn from historical pigments, illuminated manuscripts, and alchemical tradition.

| Token | Value | Usage |
|---|---|---|
| `--parchment` | `#F4ECD8` | Primary background — the page, the codex leaf |
| `--ink` | `#1A1614` | Primary text — iron gall ink |
| `--gold` | `#C9A14A` | Metatron / Law / dividers / corner flourishes / gold leaf accents |
| `--fire` | `#B7472A` | Fire Element — vermillion / cinnabar |
| `--water` | `#2E5C7E` | Water Element — lapis blue |
| `--earth` | `#5C6E3C` | Earth Element — verdant moss |
| `--air` | `#B8A7C9` | Air Element — smoky violet / lavender |
| `--void` | `#0B0A0F` | Metatron core / deepest shadow |
| `--ivory` | `#E8DFC4` | Aged ivory — secondary surface, card backgrounds |

**Color rules:**
- Never use more than two element colors in a single composition unless representing the full Arcana Grid
- Gold is the binding color — it appears on every surface as the thread of divine order
- Backgrounds: Parchment (`#F4ECD8`) for primary; Ivory (`#E8DFC4`) for secondary surfaces
- Text: Always Ink on Parchment, never reversed unless in a full Void/dark context

### Typography

**Display / Archetype Titles**
- Primary: **Cinzel** (Google Fonts) — engraved, ceremonial, Roman
- Alternate: **IM Fell English** — hand-press, humanist, imperfect
- Use: Archetype names, section headers, card titles, sacred labels
- Features: Small caps, lining numerals; generous letter-spacing (+0.05em to +0.1em)

**Body / Codex Entries**
- Primary: **EB Garamond** (Google Fonts) — warm, oldstyle, scholarly
- Alternate: **Lora** — slightly more modern humanist serif
- Use: All body text, codex entries, descriptions, invocations in paragraph form
- Features: Oldstyle numerals, ligatures, generous line height (1.7–1.8)

**Mono / Cipher / Sacred Words**
- Primary: **JetBrains Mono** (Google Fonts)
- Use: S∆CR3D words, ciphers, gematria tables, invocation blocks
- Features: Tracked (+0.15em), small size (0.85em), uppercase preferred

### Spacing & Layout

- **Margins:** Generous. Outer margins wider than inner — evokes manuscript codex
- **Proportion:** Golden ratio governs column widths and card proportions (1 : 1.618)
- **Grid:** 3×4 Arcana lattice with central Metatron node; 12-fold radial symmetry for ceremonial layouts
- **Dividers:** Hairline rules (1px, gold tint), never heavy bars
- **Section markers:** Sigil glyphs — ✦ ✧ ◊ △ ▽ ◯ ✺ — never bullets or dashes
- **Spacing scale:** 4px base unit; major steps at 8, 16, 24, 32, 48, 64, 96

### Backgrounds & Texture

- **Paper grain:** Subtle CSS noise/texture overlay on parchment backgrounds (~5% opacity)
- **Gold leaf accents:** Thin gold lines, corner flourishes, concentric ring ornaments
- **No gradients** with high saturation; only very subtle warm-to-ivory fades permitted
- **No photography** — the world is manuscript, not photographic
- **Full-bleed parchment** is the default; dark Void backgrounds reserved for Metatron/center compositions

### Borders & Cards

- **Cards:** 1px gold border (`#C9A14A` at 60% opacity), element-color inner rule, no border-radius (0px — manuscripts don't have rounded corners)
- **Corner flourishes:** SVG or unicode ornaments at card corners in gold
- **Inner shadow:** Very subtle inset shadow on parchment surfaces to suggest physical depth
- **No drop shadows** — use hairline borders instead

### Animation & Motion

- **Pace:** Slow, breath-paced — 400–700ms, `ease-in-out` exclusively
- **Transitions:** Opacity fades, subtle scale (0.98→1.0), never translate-heavy or bouncy
- **Hover states:** Reveal sigils or numerical correspondences as soft fades (opacity 0→1)
- **Page transitions:** Evoke turning pages or candle flicker — CSS opacity + slight brightness
- **No spring animations, no bounce, no elastic**

### Corner Radius

- **Cards, panels, borders:** `0px` — sharp corners. Manuscripts are rectangular.
- **Sacred Node badges:** `50%` — perfect circles only, for circular ceremonial forms
- **Buttons:** `0px` or `2px` maximum — minimal, not rounded

### Iconography

See **ICONOGRAPHY** section below.

---

## ICONOGRAPHY

Sacred Codex does **not** use a conventional icon library (no Lucide, no Heroicons, no Material Icons). The system's visual language is built from:

**1. Sigil Glyphs (Unicode)**
Used as section markers, dividers, and ornamental punctuation:
`✦ ✧ ◊ △ ▽ ◯ ✺ ⬡ ✶ ❋ ◈ ⊕`

**2. Alchemical & Astrological Unicode**
For element and prime representation:
- Fire: △ (upward triangle)
- Water: ▽ (downward triangle)
- Earth: ▽ with bar (⊕ or custom)
- Air: △ with bar

**3. Custom Sigil Assets**
Each of the 12 Archetypes has a unique Sigil — a symbolic mark combining element geometry with prime encoding. These are SVG files stored in `assets/sigils/`.

**4. No Emoji**
Emoji are never used in Sacred Codex. The system considers them tonally incompatible with the grimoire aesthetic.

**5. Decorative Assets**
- `assets/ornaments/` — gold corner flourishes, hairline rules, geometric frames
- `assets/geometry/` — Metatron's Cube, Vesica Piscis, sacred geometry SVGs

---

## FILE INDEX

```
/
├── README.md                          ← This file
├── SKILL.md                           ← Agent skill definition
├── colors_and_type.css                ← CSS design tokens (colors, type, spacing)
├── assets/
│   ├── sigils/                        ← 12 Archetype sigil SVGs
│   ├── ornaments/                     ← Corner flourishes, dividers
│   └── geometry/                      ← Sacred geometry SVGs
├── preview/
│   ├── colors-primary.html            ← Primary color palette card
│   ├── colors-element.html            ← Element color palette card
│   ├── colors-semantic.html           ← Semantic color usage card
│   ├── type-display.html              ← Display / Archetype type specimen
│   ├── type-body.html                 ← Body / Codex type specimen
│   ├── type-mono.html                 ← Cipher / Mono type specimen
│   ├── type-scale.html                ← Type scale overview
│   ├── spacing-tokens.html            ← Spacing & geometry tokens
│   ├── spacing-sacred-grid.html       ← Sacred Arcana grid layout
│   ├── component-archetype-card.html  ← Archetype Card component
│   ├── component-sacred-node.html     ← Sacred Node badge component
│   ├── component-codex-entry.html     ← Codex Entry layout
│   ├── component-cipher-block.html    ← Cipher Block component
│   └── component-buttons.html        ← Button states
└── ui_kits/
    └── web/
        ├── README.md                  ← Web UI kit documentation
        └── index.html                 ← Interactive web experience prototype
```

---

*In Lakesh — Alakin.*
