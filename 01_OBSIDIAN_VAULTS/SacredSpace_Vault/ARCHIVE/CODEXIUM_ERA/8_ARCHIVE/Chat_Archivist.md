---
tags:
  - archive
  - chat-archivist
  - chrome-extension
  - pgvector
pillar: ARCHIVE
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Chat Archivist â€” Chrome Extension

> Status: CANON â€” sacredarchive_v1.zip deployed.

The Chat Archivist is a Chrome extension that captures ChatGPT conversation history and archives it into the SacredSpace memory system.

## Components

| Component | Description |
|-----------|-------------|
| Chrome extension | Sidebar UI, capture triggers, keyboard shortcut (Cmd+K) |
| Supabase pgvector backend | Stores embeddings of all captured conversations |
| OpenAI embeddings | Generates 1536-dim embeddings for semantic search |
| Python bulk importer | Batch imports from ChatGPT `conversations.json` export |
| Cmd+K search HUD | Semantic search across entire chat history |

## The Codexium Connection

The Chat Archivist is the ingestion pipeline for ChatGPT-generated artifacts (like the Codexium vâˆž design session) into the SacredSpace memory system. 

Workflow:
1. Export ChatGPT history â†’ `conversations.json`
2. Run bulk importer â†’ Supabase pgvector
3. Tag technical content â†’ RAW tier
4. Canon Gate review â†’ promote to DISTILLED
5. CANON documents written to vault

## Cmd+K Search

Semantic search across all archived conversations. Query: "Codexium entropy worker" â†’ returns all relevant conversation segments, ranked by cosine similarity.
