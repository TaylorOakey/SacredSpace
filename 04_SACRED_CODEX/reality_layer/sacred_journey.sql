-- REALITY_LAYER Database Schema
-- SQLite database for shrine + visit tracking
-- Created: 2026-08-04

CREATE TABLE IF NOT EXISTS characters (
    character_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_archetype TEXT DEFAULT 'Fool',
    developing_archetype TEXT,
    shadow_archetype TEXT,
    total_visits INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shrines (
    shrine_id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL,
    name TEXT NOT NULL,
    location_lat REAL,
    location_lon REAL,
    archetype TEXT NOT NULL,
    founding_story TEXT,
    family_scope TEXT DEFAULT 'solo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit_count INTEGER DEFAULT 0,
    FOREIGN KEY (character_id) REFERENCES characters(character_id)
);

CREATE TABLE IF NOT EXISTS visits (
    visit_id TEXT PRIMARY KEY,
    shrine_id TEXT NOT NULL,
    character_id TEXT NOT NULL,
    ritual_type TEXT,
    intention TEXT,
    journal_entry TEXT,
    photo_path TEXT,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archetype_shift_type TEXT,
    archetype_shift_value INTEGER DEFAULT 0,
    synced_to_obsidian BOOLEAN DEFAULT FALSE,
    synced_at TIMESTAMP,
    FOREIGN KEY (shrine_id) REFERENCES shrines(shrine_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id)
);

CREATE TABLE IF NOT EXISTS qr_codes (
    qr_id TEXT PRIMARY KEY,
    shrine_id TEXT NOT NULL UNIQUE,
    qr_payload TEXT NOT NULL,
    qr_image_path TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shrine_id) REFERENCES shrines(shrine_id)
);

CREATE TABLE IF NOT EXISTS sync_log (
    sync_id TEXT PRIMARY KEY,
    shrine_id TEXT,
    visit_id TEXT,
    sync_type TEXT,
    obsidian_path TEXT,
    status TEXT,
    pulse_published BOOLEAN DEFAULT FALSE,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_shrines_character ON shrines(character_id);
CREATE INDEX IF NOT EXISTS idx_visits_shrine ON visits(shrine_id);
CREATE INDEX IF NOT EXISTS idx_visits_character ON visits(character_id);
CREATE INDEX IF NOT EXISTS idx_visits_synced ON visits(synced_to_obsidian);
