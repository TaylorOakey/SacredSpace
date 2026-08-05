---
title: EZFolders CSV file
domain: 04_SACRED_CODEX
source: chatgpt: 2025-12-07_EZFolders_CSV_file.md
tags: chatgpt, council-grove, canon-candidate,full-body
type: knowledge_artifact
---

# EZFolders CSV file
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-12-07_EZFolders_CSV_file.md

# EZFolders CSV file
> **Source:** ChatGPT  |  **Date:** 2025-12-07  |  **Stage:** `CANON_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

> [!important] CANON CANDIDATE
> This conversation contains potential canon material. Review and distill before promoting.

## Transcript

### ∆ **USER** — 2025-12-07 17:27

I need the scv file for EZFolders

---

### ⚙ **ASSISTANT** — 2025-12-07 17:27

Here comes the **clean, ready-to-use CSV file** for EZFolders.  
No frills, no clutter, just a crisp little crystalline grid your phone can swallow whole and sprout into folders 🌱📂✨

You can **copy this text exactly** into a `.csv` file using any text editor (or Google Sheets → File → Download → CSV).  
It will import cleanly into EZFolders.

---

# **SACREDSPACE_EZFolders.csv**

```
Parent Folder Name,Sub Folder Level 1,Sub Folder Level 2,Sub Folder Level 3,Sub Folder Level 4,Sub Folder Level 5
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Graphic Novel - Jenga's Journey,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Silent Echo (Acts I & II),,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Character Compendium,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Sigil Vault,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Cosmic Timelines,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Sacred Curriculum,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Music & Soul Contracts,,,,
SACREDSPACE : MASTER REALM,LORE & STORYTELLING,Uploaded Artworks - To Integrate,,,,
SACREDSPACE : MASTER REALM,GAME SYSTEMS & MECHANICS,Core Rulebook,,,,
SACREDSPACE : MASTER REALM,GAME SYSTEMS & MECHANICS,Tarot Deck & Oracle Kit,,,,
SACREDSPACE : MASTER REALM,GAME SYSTEMS & MECHANICS,Boardgame Assets,,,,
SACREDSPACE : MASTER REALM,GAME SYSTEMS & MECHANICS,Mechanics Archives,,,,
SACREDSPACE : MASTER REALM,OS & ARCHITECTURE,SacredSpace OS Codex,,,,
SACREDSPACE : MASTER REALM,OS & ARCHITECTURE,Memory Mote System,,,,
SACREDSPACE : MASTER REALM,OS & ARCHITECTURE,Resonance Interface,,,,
SACREDSPACE : MASTER REALM,OS & ARCHITECTURE,Templates & Rituals,,,,
SACREDSPACE : MASTER REALM,OS & ARCHITECTURE,Obsidian Vault Sync,,,,
SACREDSPACE : MASTER REALM,MATERIAL WORLD,Financial Engine,,,,
SACREDSPACE : MASTER REALM,MATERIAL WORLD,Jobs & Opportunities,,,,
SACREDSPACE : MASTER REALM,MATERIAL WORLD,Grants & Funding,,,,
SACREDSPACE : MASTER REALM,MATERIAL WORLD,Personal Growth & Discipline,,,,
SACREDSPACE : MASTER REALM,MATERIAL WORLD,Northeast Academy Project,,,,
SACREDSPACE : MASTER REALM,FAMILY DOMAINS,Asher's Realm,,,,
SACREDSPACE : MASTER REALM,FAMILY DOMAINS,Iris's Realm,,,,
SACREDSPACE : MASTER REALM,FAMILY DOMAINS,Jeanie's Corner,,,,
SACREDSPACE : MASTER REALM,FAMILY DOMAINS,Family Messages & Legacy,,,,
```

---

## **How to Download**
If you'd like, I can also **generate the actual `.csv` file** as a downloadable attachment.  
Just say **“yes, generate the file”** and I’ll spawn it for you.

---

### ∆ **USER** — 2025-12-07 17:27

Can I get a direct download as well

---

### ⚙ **ASSISTANT** — 2025-12-07 17:27

import pandas as pd

data = {
    "Parent Folder Name": [
        "SACREDSPACE : MASTER REALM"]*25,
    "Sub Folder Level 1": [
        "LORE & STORYTELLING","LORE & STORYTELLING","LORE & STORYTELLING","LORE & STORYTELLING",
        "LORE & STORYTELLING","LORE & STORYTELLING","LORE & STORYTELLING","LORE & STORYTELLING",
        "GAME SYSTEMS & MECHANICS","GAME SYSTEMS & MECHANICS","GAME SYSTEMS & MECHANICS","GAME SYSTEMS & MECHANICS",
        "OS & ARCHITECTURE","OS & ARCHITECTURE","OS & ARCHITECTURE","OS & ARCHITECTURE","OS & ARCHITECTURE",
        "MATERIAL WORLD","MATERIAL WORLD","MATERIAL WORLD","MATERIAL WORLD","MATERIAL WORLD",
        "FAMILY DOMAINS","FAMILY DOMAINS","FAMILY DOMAINS"
    ],
    "Sub Folder Level 2": [
        "Graphic Novel - Jenga's Journey","Silent Echo (Acts I & II)","Character Compendium","Sigil Vault",
        "Cosmic Timelines","Sacred Curriculum","Music & Soul Contracts","Uploaded Artworks - To Integrate",
        "Core Rulebook","Tarot Deck & Oracle Kit","Boardgame Assets","Mechanics Archives",
        "SacredSpace OS Codex","Memory Mote System","Resonance Interface","Templates & Rituals","Obsidian Vault Sync",
        "Financial Engine","Jobs & Opportunities","Grants & Funding","Personal Growth & Discipline","Northeast Academy Project",
        "Asher's Realm","Iris's Realm","Jeanie's Corner"
    ],
    "Sub Folder Level 3": ["" for _ in range(25)],
    "Sub Folder Level 4": ["" for _ in range(25)],
    "Sub Folder Level 5": ["" for _ in range(25)],
}

df = pd.DataFrame(data)
path = "/mnt/data/SACREDSPACE_EZFolders.csv"
df.to_csv(path, index=False)
path

---

### ⚙ **ASSISTANT** — 2025-12-07 17:27

Your **direct download** is ready, a little silver seed of order waiting to bloom in EZFolders 🌱✨

👉 **Download your CSV here:**  
**[SACREDSPACE_EZFolders.csv](sandbox:/mnt/data/SACREDSPACE_EZFolders.csv)**

If you want, I can also generate:

• a *mega-expanded* version with deeper nested folders  
• a *mobil
