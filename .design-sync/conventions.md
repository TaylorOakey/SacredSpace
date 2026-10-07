# SacredSpace OS — Design Sync Conventions
**Project:** Sacred Codex Design System  
**Package:** ui_kits/web  
**Shape:** off-script (HTML artboard previews)

## What lives here

All files are standalone HTML artboard previews — not a component library.
No storybook, no dist/, no build step. Pure vanilla HTML/CSS/JS.

Each file carries a `@dsCard` annotation as the first comment:
```html
<!-- @dsCard group="UI Kit — Web" name="..." subtitle="..." viewport="WxH" -->
```

## Design tokens (CODEX-VISUAL-001, sealed 2026-07-17)

```css
--void:   #030508   /* background */
--gold:   #C8A44A   /* sacred gold, primary accent */
--bio:    #72E87A   /* bioluminescent green */
--fire:   #D45A28
--water:  #3878A0
--earth:  #5A8850
--air:    #78A8C8
--aether: #7A5CA5
--bronze: #8B7355
--parch:  #C8C4BB   /* parchment */
--pure:   #EEF6EF   /* near-white text */
```

## Typography

- **Cinzel** — display/ceremonial/headings (Google Fonts)
- **Cormorant Garamond** — body (NOT EB Garamond)
- **JetBrains Mono** — data/cipher/code

## Physical scale

2px/mm — A4 = 420×594px, A3 = 594×840px, 610mm = 1220px

## S∆CR3DS!G∆L cipher

`A→∆  E→3  I→!  O→0  S→$  T→7`

## Groups

| Group | Contents |
|-------|----------|
| UI Kit — Web | All artboards (board game + creative expression layer) |

## Adding a new artboard

1. Add `<!-- @dsCard ... -->` as the first line of the file
2. Place the file in `06_AGENT_LAYER/ui_kits/web/`
3. Add a card to `index.html`
4. Run `/design-sync` to push to Sacred Codex Design System
