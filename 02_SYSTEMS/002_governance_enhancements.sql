-- Migration 002: Governance enhancements, SPI history, dedup index

-- ── SPI history (track progress over time) ────────────────────────────────
CREATE TABLE IF NOT EXISTS forest_spi_log (
  id           BIGSERIAL PRIMARY KEY,
  spi          NUMERIC(5,1) NOT NULL,
  components   JSONB NOT NULL DEFAULT '{}'::jsonb,
  stats        JSONB NOT NULL DEFAULT '{}'::jsonb,
  recorded_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_spi_log_recorded ON forest_spi_log(recorded_at DESC);

-- ── Dedup fingerprint table ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ingest_fingerprints (
  fingerprint  TEXT PRIMARY KEY,
  source_url   TEXT NOT NULL,
  node_id      TEXT REFERENCES forest_nodes(id) ON DELETE SET NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Repair log index ───────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_repair_log_session ON sacred_repair_log(session_id, created_at DESC);

-- ── Forest node: add last_accessed_at if missing ──────────────────────────
ALTER TABLE forest_nodes ADD COLUMN IF NOT EXISTS last_accessed_at TIMESTAMPTZ;

-- ── Dead link view ─────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW v_dead_links AS
  SELECT id, title, source_url, updated_at
  FROM forest_nodes
  WHERE tags ? 'dead_link';

-- ── Archived node view ────────────────────────────────────────────────────
CREATE OR REPLACE VIEW v_archived_nodes AS
  SELECT id, title, node_type, resurrection_score, updated_at
  FROM forest_nodes
  WHERE tags ? 'archived'
  ORDER BY resurrection_score DESC;

-- ── Sealed node view ─────────────────────────────────────────────────────
CREATE OR REPLACE VIEW v_sealed_nodes AS
  SELECT id, title, source_url, license, created_at
  FROM forest_nodes
  WHERE tags ? 'sealed';

-- ── Active forest view (shortcut for healthy nodes) ──────────────────────
CREATE OR REPLACE VIEW v_active_forest AS
  SELECT id, title, node_type, source_url, tags, license,
         resurrection_score, updated_at
  FROM forest_nodes
  WHERE NOT (tags ? 'archived')
    AND NOT (tags ? 'sealed')
    AND NOT (tags ? 'dead_link');
