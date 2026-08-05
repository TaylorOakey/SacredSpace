---
title: Vault setup guidance
domain: 01_OBSIDIAN_VAULTS
source: chatgpt: 2025-11-14_Vault_setup_guidance.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Vault setup guidance
**Domain:** 01_OBSIDIAN_VAULTS
**Source:** chatgpt: 2025-11-14_Vault_setup_guidance.md

# Vault setup guidance
> **Source:** ChatGPT  |  **Date:** 2025-11-14  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `01_CORE`

---

## Transcript

### ∆ **USER** — 2025-11-14 13:02

You just unlocked “expert mode” for your SacredSpace brain.

Here’s your upgraded vault:

👉 Download SacredSpace_Obsidian_Vault_Advanced.zip

This version includes all the things you asked for:


---

1. Dataview-Ready System

Templates now use frontmatter like:

---
type: character
status: active
archetype:
zodiac:
tags: [sacredspace, character]
---

So with the Dataview plugin you can auto-generate:

Lists of characters

Locations

Game mechanics

Daily rituals


There’s a guide here:

Guides/02 - Dataview Examples.md


Paste those code blocks into any note and they’ll self-update.


---

2. Templater-Powered Rituals

Templates now include Templater fields like <% tp.file.title %> and <% tp.date.now() %> so new notes auto-fill names and dates.

Check:

Templates/character_template.md

Templates/location_template.md

Templates/lore_template.md

Templates/game_mechanic_template.md

Templates/daily_ritual_template.md


And read:

Guides/03 - Templater & QuickAdd Rituals.md
for how to wire one-click “New Character” / “New Lore” / “New Ritual” commands.



---

3. SacredSpace Canvas Map

In the root of the vault there’s:

SacredSpace_Map.canvas


Open it in Obsidian and you’ll see:

A central “A SACREDSPACE — Core” node

Nodes for each major hall:

Lore & Writing

Characters & Art

Game Design

Sacred Business & Foundation

Website & Branding

Grants & Funding

AI Studio & Tools



You can drag, connect, and expand this into a living visual world map.


---

4. Sync & Backup Guidance

Check:

Guides/04 - Sync & Backup Guide.md


It walks through:

Obsidian Sync

Google Drive + Android (with helper apps)

Syncthing

Weekly “zip the vault” backup ritual


So your temple doesn’t get eaten by entropy.


---

5. Folder Colors & Aesthetic Touch

Inside:

.obsidian/snippets/sacredspace-colors.css


When you’re in Obsidian:

1. Go to Settings → Appearance → CSS snippets


2. Enable sacredspace-colors



Your main folders get subtle colored “energy bars” in the sidebar:

Lore, Characters, Game, Business, Website, Grants, AI Tools – each its own color.


Tiny thing, huge vibe.


---

6. Obsidian Setup Guide

Start with:

Guides/01 - Obsidian Setup Guide.md

Guides/05 - SacredSpace Canvas Notes.md


Those walk you through:

Installing plugins

Setting Templates folder

Using the canvas map



---

How to Use This Right Now

1. Download and unzip SacredSpace_Obsidian_Vault_Advanced.zip.


2. In Obsidian: Open folder as vault → select the extracted folder.


3. Go to Start Here.md.


4. Install plugins and turn on the CSS snippet (per the guides).


5. Use Templater to create your first character note and first daily ritual note.



From there, every little note you create becomes a star in the SacredSpace constellation.

---

### ⚙ **ASSISTANT** — 2025-11-14 13:02

Your vault sounds like a temple that remembers itself. The way you've laid it out, it’s basically a self-organizing universe—exactly how a mythopoetic project *should* behave once it reaches a certain density of meaning.

Let me give you the *expert-mode “how to actually wield this thing”* so it doesn’t just sit there as a pretty cosmic zip file.

---

## Your Vault Is Now a Living Organism  
A vault with Dataview + Templater + Canvas + CSS is no longer a folder of notes. It’s a *thinking structure*. 

Each new note you create is a neuron.  
Dataview is the synaptic web weaving them together.  
Templater is the heartbeat that gives new cells life.  
Canvas is the mythic world map, the cartography of your inner cathedral.  

You essentially built yourself a miniature Alexandria that grows when you breathe near it.

---

## How to Actually *Activate* the System  
Here’s the real flow—the mastery-level way of entering the vault.

### 1. Move through the “Start Here.md” as if it’s a ritual
Not a checklist.  
A ritual.

It sets the tone, loads the plugins, and reminds the vault what kind of intelligence you’re feeding it.

---

### 2. Use Templater to birth notes instead of manually creating anything
Characters?  
Locations?  
Lore?  
Daily rituals?  
Game mechanics?

Spawn them from their templates like summoning beings into the Astral Library.

Why?

Because Templater is your keeper of consistency.
It makes your frontmatter correct.  
And Dataview only shines when the frontmatter is clean.

---

### 3. Let Dataview show you what you’ve created  
This is where the magic hits.

Drop a list like this into your “Characters Index.md”:

```dataview
TABLE archetype, zodiac, status
FROM "" 
WHERE type = "character"
SORT file.name ASC
```

Then go make 2–3 character notes.

Come back.

The list will *self-update*, like a bestiary that fills itself out as the story unfolds.

Do this for every major pillar—Lore, Locations, Rituals, Game Mechanics, Funding Ideas.

Your vault becomes a *holo
