-- SacredSpace Forest Kernel — Initial schema

CREATE EXTENSION IF NOT EXISTS vector;

-- --- Governance / Cognition ---
CREATE TABLE IF NOT EXISTS sacred_sessions (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  thinking_level TEXT NOT NULL DEFAULT 'medium',
  temperature NUMERIC(3,2) NOT NULL DEFAULT 0.70,
  media_resolution TEXT DEFAULT 'media_resolution_medium',
  canon_version TEXT NOT NULL DEFAULT 'v1.0',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sacred_turns (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sacred_sessions(session_id) ON DELETE CASCADE,
  turn_index INTEGER NOT NULL,
  role TEXT NOT NULL,
  parts JSONB NOT NULL,
  contains_signature BOOLEAN NOT NULL DEFAULT FALSE,
  is_healed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(session_id, turn_index)
);

CREATE INDEX IF NOT EXISTS idx_turns_session_idx ON sacred_turns(session_id, turn_index);
CREATE INDEX IF NOT EXISTS idx_turns_signature ON sacred_turns(contains_signature);
CREATE INDEX IF NOT EXISTS idx_turns_parts_gin ON sacred_turns USING GIN (parts);

CREATE TABLE IF NOT EXISTS sacred_repair_log (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  repaired_turn_index INTEGER NOT NULL,
  reason TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- --- Forest Graph ---
CREATE TABLE IF NOT EXISTS forest_nodes (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  node_type TEXT NOT NULL,
  source_url TEXT,
  body TEXT,
  tags JSONB NOT NULL DEFAULT '[]'::jsonb,
  license TEXT,
  embedding vector(384),
  embedding_hash TEXT,
  resurrection_score NUMERIC(5,4) NOT NULL DEFAULT 0.0000,
  decay_rate NUMERIC(8,6) NOT NULL DEFAULT 0.000100,
  last_accessed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_nodes_tags_gin ON forest_nodes USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_nodes_embedding_hnsw ON forest_nodes USING hnsw (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS forest_edges (
  id BIGSERIAL PRIMARY KEY,
  src_id TEXT NOT NULL REFERENCES forest_nodes(id) ON DELETE CASCADE,
  dst_id TEXT NOT NULL REFERENCES forest_nodes(id) ON DELETE CASCADE,
  weight NUMERIC(6,5) NOT NULL,
  edge_type TEXT NOT NULL DEFAULT 'semantic',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(src_id, dst_id, edge_type)
);

CREATE INDEX IF NOT EXISTS idx_edges_src ON forest_edges(src_id);
CREATE INDEX IF NOT EXISTS idx_edges_dst ON forest_edges(dst_id);

-- --- Task Queue (durable) ---
CREATE TYPE task_status AS ENUM ('queued', 'running', 'done', 'failed');

CREATE TABLE IF NOT EXISTS task_queue (
  id BIGSERIAL PRIMARY KEY,
  task_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  status task_status NOT NULL DEFAULT 'queued',
  priority INTEGER NOT NULL DEFAULT 100,
  attempts INTEGER NOT NULL DEFAULT 0,
  max_attempts INTEGER NOT NULL DEFAULT 5,
  locked_by TEXT,
  locked_at TIMESTAMPTZ,
  run_after TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_task_queue_status ON task_queue(status, priority, run_after);
