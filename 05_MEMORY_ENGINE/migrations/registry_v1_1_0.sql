-- registry_v1_1_0.sql
-- SacredSpace OS — Omni-Ledger Registry Extension
-- Pillar: 05_MEMORY_ENGINE
-- Source: Architect session ruling 2026-09-23
-- Status: READY TO APPLY — additive only, no existing tables touched
-- Apply: sqlite3 omni_ledger.db < registry_v1_1_0.sql
-- All writes via Pulse transaction.manual + MANUAL_ENTRY

PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS registry_identities (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL CHECK(type IN ('human','agent','archetype','character','brand')),
    soul_tone   TEXT,
    description TEXT,
    pillar      TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_projects (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    pillar      TEXT NOT NULL,
    status      TEXT NOT NULL CHECK(status IN ('active','paused','archived','sealed','planning')),
    description TEXT,
    lead_agent  TEXT REFERENCES registry_identities(id),
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_artifacts (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL CHECK(type IN ('document','script','export','design','audio','image','database','config','skill','other')),
    project_id  TEXT REFERENCES registry_projects(id),
    canonical   INTEGER NOT NULL DEFAULT 0 CHECK(canonical IN (0,1)),
    location    TEXT,
    status      TEXT NOT NULL CHECK(status IN ('raw','distilled_candidate','canon_candidate','canon','sealed','archived','superseded')),
    source      TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_agents (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    model           TEXT,
    role            TEXT,
    authority_level TEXT NOT NULL DEFAULT 'L1' CHECK(authority_level IN ('L1','L2','L3')),
    authority_json  TEXT,
    forbidden_json  TEXT,
    status          TEXT DEFAULT 'active',
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_lore (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL CHECK(category IN ('archetype','character','location','faction','artifact','event','concept','sigil')),
    realm       TEXT,
    gematria    INTEGER,
    soul_tone   TEXT,
    pillar      TEXT,
    description TEXT,
    canon       INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_nodes (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    node_type   TEXT NOT NULL CHECK(node_type IN ('service','database','endpoint','drive','vault','script','tool','external')),
    path        TEXT,
    service     TEXT,
    port        INTEGER,
    status      TEXT DEFAULT 'unknown' CHECK(status IN ('active','down','unknown','deprecated','planned')),
    last_seen   TEXT,
    notes       TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS registry_links (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id   TEXT NOT NULL,
    target_id   TEXT NOT NULL,
    relation    TEXT NOT NULL,
    weight      REAL DEFAULT 1.0,
    notes       TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    UNIQUE(source_id, target_id, relation)
);

CREATE INDEX IF NOT EXISTS idx_artifacts_status   ON registry_artifacts(status);
CREATE INDEX IF NOT EXISTS idx_artifacts_project  ON registry_artifacts(project_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_canon    ON registry_artifacts(canonical);
CREATE INDEX IF NOT EXISTS idx_lore_category      ON registry_lore(category);
CREATE INDEX IF NOT EXISTS idx_lore_realm         ON registry_lore(realm);
CREATE INDEX IF NOT EXISTS idx_nodes_status       ON registry_nodes(status);
CREATE INDEX IF NOT EXISTS idx_links_source       ON registry_links(source_id);
CREATE INDEX IF NOT EXISTS idx_links_target       ON registry_links(target_id);

INSERT OR IGNORE INTO registry_nodes VALUES
    ('spine-8888',  'FastAPI Spine',   'service',  'D:/SacredSpace_OS/systems/fastapi/main.py', 'uvicorn', 8888, 'down',    NULL, 'A7 — refused 2026-09-23', datetime('now')),
    ('pulse-8890',  'Sacred Pulse',    'service',  NULL, 'pulse', 8890, 'active', NULL, 'v2.1.0, 8 subs, DLQ 0', datetime('now')),
    ('hermes-mcp',  'Hermes MCP',      'service',  'D:/SacredSpace_OS/02_COUNCIL_GROVE/hermes/hermes_mcp.py', NULL, NULL, 'unknown', NULL, '7-tool set', datetime('now')),
    ('chroma-8001', 'ChromaDB',        'database', 'D:/SacredSpace_OS/05_MEMORY_ENGINE/chroma_db/', NULL, 8001, 'unknown', NULL, '10753 vectors 2026-09-18', datetime('now')),
    ('omni-ledger', 'Omni Ledger DB',  'database', 'D:/SacredSpace_OS/05_MEMORY_ENGINE/omni_ledger.db', NULL, NULL, 'active', NULL, 'v1.0.0, 2.7MB', datetime('now')),
    ('obsidian-c',  'Obsidian Vault (canonical)', 'vault', 'C:/01_OBSIDIAN_VAULTS/SacredSpace_Vault/', NULL, 27123, 'unknown', NULL, 'C: canonical per DQ-10', datetime('now')),
    ('sacredspace-d','D: Mirror', 'drive', 'D:/SacredSpace_OS/', NULL, NULL, 'active', NULL, 'Mirror per DQ-10', datetime('now'));

INSERT OR IGNORE INTO registry_artifacts VALUES
    ('item-13-palette', '3-way Palette Conflict (Item 13)', 'document', NULL, 0, 'C:/04_SACRED_CODEX/SACRED_STORYLINE_CANON.md:50-52', 'distilled_candidate', 'canon_gate', datetime('now'), datetime('now')),
    ('rootbook-unindexed', 'Rootbook (unindexed)', 'document', NULL, 0, 'unknown', 'raw', 'manual', datetime('now'), datetime('now')),
    ('session070-backlog', 'Session 070 Phase 3 Backlog (~720 items)', 'document', NULL, 0, 'C:/00_SYSTEM_CORE/', 'raw', 'session_070', datetime('now'), datetime('now'));
