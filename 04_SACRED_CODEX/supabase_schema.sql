-- SacredSpace OS — Supabase Schema
-- Run this in: Supabase Dashboard → SQL Editor → New Query

-- ── Players ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS players (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name        TEXT NOT NULL,
  school      TEXT NOT NULL CHECK (school IN ('initiation','courage','mystery','creation')),
  soul_tone   INT DEFAULT 0,
  draws_count INT DEFAULT 0,
  spells_count INT DEFAULT 0,
  artifacts_count INT DEFAULT 0,
  joined_at   TIMESTAMPTZ DEFAULT now(),
  last_active TIMESTAMPTZ DEFAULT now()
);

-- ── Tarot Draws ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tarot_draws (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  player_id  UUID REFERENCES players(id) ON DELETE CASCADE,
  card       TEXT NOT NULL,
  npc        TEXT NOT NULL,
  episode    INT NOT NULL,
  soul_tone  INT NOT NULL,
  school     TEXT NOT NULL,
  spell_unlocked TEXT NOT NULL,
  drawn_at   TIMESTAMPTZ DEFAULT now()
);

-- ── Spell Casts ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS spell_casts (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  player_id  UUID REFERENCES players(id) ON DELETE CASCADE,
  spell      TEXT NOT NULL,
  school     TEXT NOT NULL,
  cast_at    TIMESTAMPTZ DEFAULT now(),
  context    TEXT
);

-- ── Node Visits ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS node_visits (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  player_id  UUID REFERENCES players(id) ON DELETE CASCADE,
  node_id    TEXT NOT NULL,
  visited_at TIMESTAMPTZ DEFAULT now()
);

-- ── Artifacts (Sacred Bazaar) ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS artifacts (
  id             UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  player_id      UUID REFERENCES players(id) ON DELETE CASCADE,
  player_name    TEXT NOT NULL,
  title          TEXT NOT NULL,
  description    TEXT NOT NULL,
  gematria_price INT NOT NULL,
  school         TEXT NOT NULL,
  listed         BOOLEAN DEFAULT true,
  created_at     TIMESTAMPTZ DEFAULT now()
);

-- ── Leaderboard view ─────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW leaderboard AS
SELECT
  p.id,
  p.name,
  p.school,
  p.draws_count,
  p.spells_count,
  p.artifacts_count,
  (p.draws_count * 3 + p.spells_count * 2 + p.artifacts_count * 5) AS score,
  p.last_active
FROM players p
ORDER BY score DESC
LIMIT 100;

-- ── RLS (Row Level Security) ──────────────────────────────────────────────────
ALTER TABLE players      ENABLE ROW LEVEL SECURITY;
ALTER TABLE tarot_draws  ENABLE ROW LEVEL SECURITY;
ALTER TABLE spell_casts  ENABLE ROW LEVEL SECURITY;
ALTER TABLE node_visits  ENABLE ROW LEVEL SECURITY;
ALTER TABLE artifacts    ENABLE ROW LEVEL SECURITY;

-- Allow all for now (tighten per-player once auth is added)
CREATE POLICY "public_read_players"   ON players      FOR SELECT USING (true);
CREATE POLICY "public_insert_players" ON players      FOR INSERT WITH CHECK (true);
CREATE POLICY "public_update_players" ON players      FOR UPDATE USING (true);

CREATE POLICY "public_read_draws"     ON tarot_draws  FOR SELECT USING (true);
CREATE POLICY "public_insert_draws"   ON tarot_draws  FOR INSERT WITH CHECK (true);

CREATE POLICY "public_read_spells"    ON spell_casts  FOR SELECT USING (true);
CREATE POLICY "public_insert_spells"  ON spell_casts  FOR INSERT WITH CHECK (true);

CREATE POLICY "public_read_nodes"     ON node_visits  FOR SELECT USING (true);
CREATE POLICY "public_insert_nodes"   ON node_visits  FOR INSERT WITH CHECK (true);

CREATE POLICY "public_read_artifacts" ON artifacts    FOR SELECT USING (true);
CREATE POLICY "public_insert_artifacts" ON artifacts  FOR INSERT WITH CHECK (true);
CREATE POLICY "public_update_artifacts" ON artifacts  FOR UPDATE USING (true);

-- ── Indexes ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_draws_player    ON tarot_draws (player_id);
CREATE INDEX IF NOT EXISTS idx_spells_player   ON spell_casts (player_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_listed ON artifacts (listed, created_at DESC);

-- Done. Copy SUPABASE_URL and SUPABASE_ANON_KEY from:
-- Project Settings → API → Project URL + anon/public key
