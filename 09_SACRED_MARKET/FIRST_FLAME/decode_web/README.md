# C2 · Free GR∆M∆ Mini Decode page

This is the Mini Decode (lenses II, IV and V) as one static file, `index.html`, and it is the funnel into the paid Full and Deep decodes.
- No build step, no tracking, no network calls. The name the visitor types never leaves the browser.
- **Link format:** `index.html?name=Ada%20Lovelace` fills in the name and renders the reading straight away. Use this for social posts and listing demos.
- **Engine parity:** the code between `ENGINE-START` and `ENGINE-END` must give the same results as `systems/fastapi/merchant.py` (`calculate_gematria`, `generate_sigil` with AETHER) and `grama_decode.sigilify`. It was checked against 300+ names, including hyphens, apostrophes, accents and emoji, and every soul tone (1–9, 11, 22) appeared. If you change either engine, run the check again: `python3 09_SACRED_MARKET/tools/decode_parity_check.py`.

## Before publishing (Taylor)
1. Once the Full and Deep listings are live, paste their URLs into `const SHOP = { full: "", deep: "" }`. Until then both cards say "Opening soon."
2. Choose a host. Both are free, and you click publish yourself:
   - **GitHub Pages:** create a small public repo (e.g. `grama-decode`) that holds only this `index.html`. Then go to Settings → Pages → Deploy from branch → `main` / root. Don't publish the SacredSpace repo itself, because the page would expose the whole repo.
   - **Hugging Face Static Space:** create a new Space with SDK set to *Static*, then upload `index.html`. Static Spaces are free; Gradio Spaces now need a paid plan.
3. Put the page link in the Etsy/Ko-fi shop bio, the Instagram link-in-bio and the listing descriptions ("try the free Mini first").

## Kill metric (IDEA_BANK slot 2)
If the page has fewer than 100 visits or zero paid upgrades within 60 days of publishing, kill it. There is no analytics by design, so count visits from GitHub Pages traffic (repo Insights → Traffic) or the Space's visitor count. Count upgrades from ledger rows whose `notes` field contains `via:decode_web`.
