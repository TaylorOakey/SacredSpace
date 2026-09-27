#!/usr/bin/env python3
"""
bootstrap_db.py — SacredSpace OS · Memory Engine Bootstrap
Pillar: 05_MEMORY
Owner Agent: IRIS (vault) + ELIAS (knowledge)
Status: Canon
Purpose: Initialize the 13-table SQLite schema for the Holographic Memory Engine.
Run once to seed. Safe to re-run — uses CREATE TABLE IF NOT EXISTS.

Usage:
    python3 archive/memory-motes/bootstrap_db.py
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

# ─── CANON PATH ────────────────────────────────────────────────────────────────
DB_PATH = Path(os.environ.get(
    "SACRED_DB",
    "/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/sacred_memory.db"
))

# ─── SCHEMA ────────────────────────────────────────────────────────────────────
SCHEMA = """
-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 01 · memory_motes  (atomic memory unit)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS memory_motes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    mote_id     TEXT UNIQUE NOT NULL,          -- sacred-{uuid4}
    content     TEXT NOT NULL,
    layer       TEXT NOT NULL                  -- RAW | DISTILLED | CANON
                CHECK(layer IN ('RAW','DISTILLED','CANON')),
    pillar      TEXT,                          -- 01_CORE … 09_MARKET
    tags        TEXT,                          -- JSON array of strings
    agent_id    TEXT,                          -- ELIAS | AURORA | ASHER | IRIS
    chroma_id   TEXT,                          -- ChromaDB vector ID (if embedded)
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
    is_canon    INTEGER NOT NULL DEFAULT 0     -- 0=draft, 1=canon
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 02 · agents  (ICARIS Quartet registry)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS agents (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id    TEXT UNIQUE NOT NULL,          -- ELIAS | AURORA | ASHER | IRIS
    role        TEXT NOT NULL,                 -- knowledge | code | entropy | vault
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK(status IN ('active','dormant','suspended')),
    last_seen   TEXT,
    config_json TEXT                           -- JSON blob for agent-specific config
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 03 · sessions  (Council/operator session log)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT UNIQUE NOT NULL,          -- {YYYY-MM-DD}-{slug}
    opened_at   TEXT NOT NULL DEFAULT (datetime('now')),
    sealed_at   TEXT,
    operator    TEXT NOT NULL DEFAULT 'OAKTREE',
    intent      TEXT,                          -- session intent declaration
    ledger      TEXT,                          -- JSON: actions completed
    commit_hash TEXT,                          -- git commit at seal
    status      TEXT NOT NULL DEFAULT 'open'
                CHECK(status IN ('open','sealed','canon'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 04 · codex_entries  (canon operations, spells, rituals)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS codex_entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id    TEXT UNIQUE NOT NULL,
    title       TEXT NOT NULL,
    pillar      TEXT NOT NULL,
    agent_id    TEXT,
    status      TEXT NOT NULL DEFAULT 'Draft'
                CHECK(status IN ('Draft','Active','Canon')),
    purpose     TEXT,
    inputs      TEXT,
    outputs     TEXT,
    dependencies TEXT,
    notes       TEXT,
    content     TEXT,                          -- full markdown body
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 05 · canon_log  (immutable audit trail — never update, only insert)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS canon_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type  TEXT NOT NULL,                 -- CANONIZED | PURGED | SEALED | ACTIVATED
    entity_type TEXT NOT NULL,                 -- mote | codex | session | agent | skill
    entity_id   TEXT NOT NULL,
    operator    TEXT NOT NULL DEFAULT 'OAKTREE',
    timestamp   TEXT NOT NULL DEFAULT (datetime('now')),
    notes       TEXT
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 06 · skills  (Claude/system skill registry)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id    TEXT UNIQUE NOT NULL,          -- sacredspace-system-builder, etc.
    name        TEXT NOT NULL,
    path        TEXT,                          -- SKILL.md path on disk
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK(status IN ('active','locked','deprecated')),
    origin_commit TEXT,                        -- git hash when locked
    activated_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes       TEXT
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 07 · artifacts  (scripts, docs, files produced each session)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS artifacts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_id TEXT UNIQUE NOT NULL,
    name        TEXT NOT NULL,
    artifact_type TEXT NOT NULL,               -- script | doc | codex | config | skill
    pillar      TEXT,
    path        TEXT,                          -- local filesystem path
    drive_id    TEXT,                          -- Google Drive file ID if synced
    session_id  TEXT,
    is_canon    INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    notes       TEXT
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 08 · lore_entries  (narrative/worldbuilding registry)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS lore_entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lore_id     TEXT UNIQUE NOT NULL,
    title       TEXT NOT NULL,
    category    TEXT,                          -- arcana | character | location | event
    tags        TEXT,                          -- JSON array
    content     TEXT NOT NULL,
    linked_mote TEXT,                          -- FK → memory_motes.mote_id
    is_canon    INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 09 · scout_observations  (Neural Forest Scout agent output)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS scout_observations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    obs_id      TEXT UNIQUE NOT NULL,
    source      TEXT NOT NULL,                 -- URL | file | stream
    raw_content TEXT NOT NULL,
    summary     TEXT,
    spi_score   REAL,                          -- Signal-Potential-Index (Gardener)
    tags        TEXT,                          -- JSON array
    session_id  TEXT,
    processed   INTEGER NOT NULL DEFAULT 0,    -- 0=raw, 1=gardener-processed
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 10 · gardener_distillations  (processed Scout output → Memory Motes)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS gardener_distillations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    distill_id  TEXT UNIQUE NOT NULL,
    obs_id      TEXT NOT NULL,                 -- FK → scout_observations.obs_id
    mote_id     TEXT,                          -- FK → memory_motes.mote_id (if promoted)
    distilled   TEXT NOT NULL,                 -- condensed insight
    layer       TEXT NOT NULL DEFAULT 'DISTILLED'
                CHECK(layer IN ('DISTILLED','CANON')),
    promoted_at TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 11 · context_tags  (controlled vocabulary for tag system)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS context_tags (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tag         TEXT UNIQUE NOT NULL,
    category    TEXT,                          -- pillar | agent | project | ritual
    description TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 12 · pillar_registry  (nine-pillar manifest)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS pillar_registry (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pillar_code TEXT UNIQUE NOT NULL,          -- 01_CORE … 09_MARKET
    full_name   TEXT NOT NULL,
    owner_agent TEXT,
    local_path  TEXT,
    drive_path  TEXT,
    status      TEXT NOT NULL DEFAULT 'active',
    notes       TEXT
);

-- ════════════════════════════════════════════════════════════════════════════
-- TABLE 13 · market_items  (MERCHANT agent — Sacred Artifacts commerce)
-- ════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS market_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id     TEXT UNIQUE NOT NULL,
    title       TEXT NOT NULL,
    description TEXT,
    category    TEXT,                          -- print | digital | ritual-kit
    price_usd   REAL,
    platform    TEXT,                          -- Etsy | Printify | Gelato | Gumroad
    listing_url TEXT,
    status      TEXT NOT NULL DEFAULT 'draft'
                CHECK(status IN ('draft','listed','sold','archived')),
    lore_id     TEXT,                          -- FK → lore_entries.lore_id
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# ─── SEED DATA ─────────────────────────────────────────────────────────────────
SEED_AGENTS = [
    ("ELIAS",  "knowledge", "active"),
    ("AURORA", "code",      "active"),
    ("ASHER",  "entropy",   "active"),
    ("IRIS",   "vault",     "active"),
]

SEED_PILLARS = [
    ("01_CORE",       "Core",          "Council",  "/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS"),
    ("02_COUNCIL",    "Council Grove", "Council",  "/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE"),
    ("03_NEURAL",     "Neural Forest", "AURORA",   "/mnt/d/SacredSpace_OS/03_NEURAL_FOREST"),
    ("04_CODEX",      "Sacred Codex",  "IRIS",     "/mnt/d/SacredSpace_OS/04_SACRED_CODEX"),
    ("05_MEMORY",     "Memory Engine", "ELIAS",    "/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE"),
    ("06_AGENTS",     "Agent Layer",   "ASHER",    "/mnt/d/SacredSpace_OS/06_AGENT_LAYER"),
    ("07_SOCIAL",     "Social Mothership","AURORA", "/mnt/d/SacredSpace_OS/07_SOCIAL_MOTHERSHIP"),
    ("08_LEARNING",   "Learning Path", "ELIAS",    "/mnt/d/SacredSpace_OS/08_LEARNING_PATH"),
    ("09_MARKET",     "Sacred Market", "ASHER",    "/mnt/d/SacredSpace_OS/09_SACRED_MARKET"),
]

SEED_SKILLS = [
    ("sacredspace-canon-gate",     "Canon Gate",     "03_NEURAL_FOREST/skills/sacredspace-canon-gate/SKILL.md",     "locked", "65653635..93c02acd"),
    ("sacredspace-opening-ritual", "Opening Ritual", "03_NEURAL_FOREST/skills/sacredspace-opening-ritual/SKILL.md", "locked", "65653635..93c02acd"),
    ("sacredspace-arcana-grid",    "Arcana Grid",    "03_NEURAL_FOREST/skills/sacredspace-arcana-grid/SKILL.md",    "locked", "65653635..93c02acd"),
]

SEED_TAGS = [
    ("canon",      "ritual",  "Immutable, truth-locked artifact"),
    ("draft",      "ritual",  "Work in progress, not yet reviewed"),
    ("neural",     "pillar",  "03_NEURAL_FOREST pillar tag"),
    ("memory",     "pillar",  "05_MEMORY_ENGINE pillar tag"),
    ("codex",      "pillar",  "04_SACRED_CODEX pillar tag"),
    ("ELIAS",      "agent",   "Knowledge agent"),
    ("AURORA",     "agent",   "Code agent"),
    ("ASHER",      "agent",   "Entropy agent"),
    ("IRIS",       "agent",   "Vault agent"),
    ("jenga",      "project", "Jenga's Journey graphic novel"),
    ("merchant",   "project", "MERCHANT commerce agent"),
    ("kethras",    "project", "KETHRAS learning gate agent"),
]


def bootstrap():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"  DB path  : {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("  Building schema (13 tables)...")
    conn.executescript(SCHEMA)

    print("  Seeding ICARIS Quartet...")
    cur.executemany(
        "INSERT OR IGNORE INTO agents (agent_id, role, status) VALUES (?,?,?)",
        SEED_AGENTS
    )

    print("  Seeding Nine Pillars...")
    cur.executemany(
        "INSERT OR IGNORE INTO pillar_registry (pillar_code, full_name, owner_agent, local_path) VALUES (?,?,?,?)",
        SEED_PILLARS
    )

    print("  Seeding locked skills...")
    cur.executemany(
        "INSERT OR IGNORE INTO skills (skill_id, name, path, status, origin_commit) VALUES (?,?,?,?,?)",
        SEED_SKILLS
    )

    print("  Seeding context tags...")
    cur.executemany(
        "INSERT OR IGNORE INTO context_tags (tag, category, description) VALUES (?,?,?)",
        SEED_TAGS
    )

    # ── Canon log entry for the bootstrap itself ────────────────────────────
    cur.execute(
        "INSERT INTO canon_log (event_type, entity_type, entity_id, notes) VALUES (?,?,?,?)",
        ("CANONIZED", "schema", "bootstrap_db.py", "13-table Holographic Memory Engine schema initialized")
    )

    conn.commit()
    conn.close()

    print("\n  ✅ Sacred Memory Engine bootstrapped successfully.")
    print(f"     Tables : 13")
    print(f"     Agents : {len(SEED_AGENTS)} seeded")
    print(f"     Pillars: {len(SEED_PILLARS)} seeded")
    print(f"     Skills : {len(SEED_SKILLS)} seeded (locked to origin)")
    print(f"     Tags   : {len(SEED_TAGS)} seeded")
    print(f"\n  S∆CR3DSP∆CE Memory Engine — online.")


if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════╗")
    print("║   S∆CR3DSP∆CE OS · Memory Bootstrap      ║")
    print("║   Pillar: 05_MEMORY  · Agent: IRIS        ║")
    print("╚══════════════════════════════════════════╝\n")
    bootstrap()
