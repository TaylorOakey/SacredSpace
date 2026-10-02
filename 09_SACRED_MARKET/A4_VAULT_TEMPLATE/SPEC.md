# A4 · Sovereign Creator Vault: template spec
**Layer:** DISTILLED (a working spec, not CANON). **Experiment slot:** 3, approved 2026-09-26.
**Kill metric:** fewer than 5 sales within 60 days of launch.

## What it is
A packaged, **de-personalised** Obsidian vault based on the nine-pillar structure, plus a setup guide. It's for solo creators who want one local-first home for their ideas, their lore/IP, their products and their money.
Price: $19 for the vault alone, $39 for the vault plus the guide PDF and the merchant ledger starter. Sell on Gumroad or Ko-fi (see the fee table in `FIRST_FLAME/LISTINGS.md`).

## The build rule: generate the template from nothing, never copy the vault
The template is **built from scratch as a new vault**, following the live vault's *structure*. No file is ever copied out of `01_VAULT/SacredSpace_Vault/`. That rules out leaking family, day-job, health or financial notes, and canon-locked lore, by construction, so there's nothing to scrub afterwards.

| Keep (structure) | Replace with a neutral example | Never include |
|---|---|---|
| Nine-pillar folder tree, renamed to generic names (below) | Lore → one sample "world bible" page for a fictional project | Anything about Iris, Asher or Jeanie, and family messages |
| RAW → DISTILLED → CANON workflow and its note templates | Market → a sample product card and price sheet | Day-job, household, insurance or fire notes |
| Canon Gate checklist (process only) | Codex → a sample codex entry | Canon-locked Jenga / Arcana content |
| Daily and weekly review templates | Learning → a sample course-tracking page | API keys, `.env`, personal paths (`/mnt/d/…`) |
| Dataview/Templater queries (if the plugins are free and MIT/GPL) | Agent layer → a "prompts I reuse" page | ICARIS internals, unless Taylor opts in |

Generic pillar names (a proposal; Taylor has the final say on naming):
`01 Vault Home · 02 Council (decisions) · 03 Research · 04 Codex · 05 Memory · 06 Agents & Prompts · 07 Social · 08 Learning · 09 Market`

## Deliverables
1. `SovereignCreatorVault/` is the finished vault folder, zipped for sale. It is built on the Legion by OpenCode, **outside the repo** until Taylor has reviewed it.
2. `SETUP_GUIDE.md`, then PDF: install Obsidian, open the vault, a 10-minute tour of the RAW → DISTILLED → CANON workflow, and the weekly review.
3. Optional $39 tier: `merchant_starter/`, a ledger CSV template matching the `/merchant/ledger` columns, so buyers can track sales without the FastAPI spine.
4. Listing copy and 5 screenshots, which Claude drafts once the structure exists.

## Leak check before any zip leaves the machine
- `grep -riE "iris|asher|jeanie|oakey|/mnt/|api[_-]?key|sk-|@gmail" SovereignCreatorVault/` returns nothing.
- `.obsidian/` contains only the plugin list and settings. No workspace history, no `workspace.json` recent files.
- Taylor opens the vault in Obsidian and reads every page once. **Taylor signs off; no agent does.**

## Order of work
- **OpenCode:**
  1. Map the live vault's folder tree (names and counts only) into `RECURSION/local_vault_structure.md`. Mark each folder as structure-worthy, private, or canon-locked.
  2. Build the fresh template vault from this spec.
  3. Run the leak check.
- **Claude:** write SETUP_GUIDE.md and the listing copy from OpenCode's structure map.
- **Taylor:** review, then publish the listing. Record sales as `POST /merchant/ledger` with `kind=PRODUCT`, `channel=GUMROAD` or `KOFI`, and `notes` set to `sku:A4`.
