---
tags:
  - systems
  - ai-triad
  - sync
  - protocol
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# AI Triad Sync Protocol

> Files: `sacredspace_ai_config.yaml` + `sacred_sync.py` CLI

The protocol that keeps Claude, Gemini, ChatGPT, and NotebookLM synchronized on the SacredSpace OS knowledge state.

## Config Structure (sacredspace_ai_config.yaml)

```yaml
sacredspace_ai_triad:
  version: 1.0
  activation: "S@CREDSOURC3, unfurl the scroll"
  
  seats:
    reasoning_narrative: claude
    deep_research: gemini
    systems_architect: chatgpt
    archivist: notebooklm
    
  sync_protocol:
    canon_source: obsidian_vault
    distill_source: supabase_pgvector
    raw_source: chromadb
    
  session_handoff:
    include: [active_tasks, canon_state, pillar_scores, open_decisions]
    exclude: [raw_embeddings, session_transcripts]
```

## sacred_sync.py â€” Key Commands

```bash
python sacred_sync.py --pull          # Pull canon state from Supabase
python sacred_sync.py --push          # Push local changes to Supabase
python sacred_sync.py --report        # Generate council briefing
python sacred_sync.py --handoff       # Prepare cross-model handoff doc
python sacred_sync.py --audit         # Run Canon Gate integrity check
```
