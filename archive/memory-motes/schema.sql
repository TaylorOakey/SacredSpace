-- SacredSpace OS Canon Schema v2.0
CREATE TABLE IF NOT EXISTS memory_motes (
    id        TEXT PRIMARY KEY,
    content   TEXT NOT NULL,
    pillar    TEXT NOT NULL,
    tier      TEXT NOT NULL DEFAULT 'RAW',
    agent     TEXT NOT NULL DEFAULT 'SYSTEM',
    sigil_tag TEXT,
    ts        INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS pillars (
    name      TEXT PRIMARY KEY,
    status    TEXT NOT NULL DEFAULT 'ACTIVE',
    notes     TEXT
);

CREATE TABLE IF NOT EXISTS canon_events (
    id        TEXT PRIMARY KEY,
    title     TEXT NOT NULL,
    pillar    TEXT NOT NULL,
    ts        INTEGER NOT NULL,
    payload   TEXT
);

INSERT OR IGNORE INTO pillars (name) VALUES
    ('CORE'),('SYSTEMS'),('LEARNING'),('ECONOMY'),
    ('HABITAT'),('CREATION'),('COUNCIL'),('LINEAGE'),('ARCHIVE');
