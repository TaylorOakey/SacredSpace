---
tags:
  - systems
  - infrastructure
  - stack
  - hardware
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Infrastructure Stack

## Hardware

**Primary Machine: Lenovo Legion Y520**
- OS: Windows 10 (host) + WSL2 Ubuntu 24.04
- GPU: GTX 1060 6GB (CUDA for local inference)
- Storage: Internal SSD + Toshiba external HDD (SacredArchive)

**SacredArchive (Toshiba External HDD)**
- Primary: THIS VAULT (Obsidian)
- Backup: SacredSpace OS snapshots
- Archive: Chat exports, code zips, media

## Software Stack

### Inference Layer
```
Ollama v0.x          â†’ port 11434
  Models: llama3, mistral, nomic-embed-text, mxbai-embed-large
  GPU offload: GTX 1060 6GB
```

### Vector Storage
```
ChromaDB             â†’ port 8000   (RAW tier embeddings)
PostgreSQL + pgvector â†’ port 5432  (CANON tier embeddings)
```

### Interface
```
Open WebUI           â†’ port 8080   (post-ChromaDB fix)
Sacred Fiahfox v2.0  â†’ Firefox extension + local HTTP bridge
```

### Orchestration
```
LangGraph + FastAPI  â†’ spine layer
  inference â†’ memory â†’ presentation
SacredBootstrap.ps1 v2 â†’ 7 modes, PowerShell bootstrap
```

### Cloud / Sync
```
Supabase             â†’ relational config + episodic memory
Tailscale            â†’ mesh networking, node 100.117.9.101
```

## Network Map

```
Legion Y520 (WSL2) â”€â”€â”€â”€ Tailscale â”€â”€â”€â”€ [future nodes]
     â”‚
     â”œâ”€â”€ Ollama :11434
     â”œâ”€â”€ ChromaDB :8000
     â”œâ”€â”€ Open WebUI :8080
     â”œâ”€â”€ PostgreSQL :5432
     â””â”€â”€ Toshiba SacredArchive (USB)
```
