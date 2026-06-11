---
tags:
  - systems
  - storage
  - sync
  - design
  - drive-linked
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
drive_url: https://docs.google.com/document/d/1SY8buYFJpM-8n34ZEQL6DKwIJiw0ovK0l6yqJm0b4XA/export?format=pdf
---

# Storage & Sync Design

> Drive document â€” full text at frontmatter URL.

## Storage Hierarchy

```
SacredSpace OS Storage

Tier 1: Active (Hot)
  â””â”€â”€ Internal SSD (WSL2 /home)
      â”œâ”€â”€ Ollama models
      â”œâ”€â”€ ChromaDB data
      â””â”€â”€ Active project files

Tier 2: Canon (Warm)
  â””â”€â”€ Toshiba SacredArchive (USB HDD)
      â”œâ”€â”€ Obsidian Vault (THIS VAULT)
      â”œâ”€â”€ SacredSpace OS snapshots
      â””â”€â”€ Chat history archives

Tier 3: Cloud (Cold)
  â””â”€â”€ Supabase
      â”œâ”€â”€ Episodic memory (pgvector)
      â”œâ”€â”€ Config tables
      â””â”€â”€ Event log
```

## Sync Protocols

- **Vault â†’ Toshiba**: SacredBootstrap Mode 7 (manual trigger)
- **Supabase â†’ Local**: `sacred_sync.py` CLI (pull mode)
- **Local â†’ Supabase**: LangGraph agent events (push on CANON promotion)
- **Future â†’ GitHub**: Codexium Git crossover (pending)
