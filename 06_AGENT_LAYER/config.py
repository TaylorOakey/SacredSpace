from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = Field(alias="DATABASE_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # ── GitHub ────────────────────────────────────────────────────────────────
    github_token: Optional[str] = Field(default=None, alias="GITHUB_TOKEN")
    github_user_agent: str = Field(
        default="sacredspace-forest-kernel/1.0", alias="GITHUB_USER_AGENT"
    )

    # ── LLM Providers (cascading: openai → anthropic → ollama → mock) ─────────
    llm_provider: str = Field(default="auto", alias="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-haiku-4-5-20251001", alias="ANTHROPIC_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:3b", alias="OLLAMA_MODEL")
    ollama_embed_model: str = Field(default="nomic-embed-text", alias="OLLAMA_EMBED_MODEL")

    # ── Embeddings ────────────────────────────────────────────────────────────
    embeddings_provider: str = Field(
        default="local_sentence_transformers", alias="EMBEDDINGS_PROVIDER"
    )
    sentence_transformers_model: str = Field(
        default="all-MiniLM-L6-v2", alias="SENTENCE_TRANSFORMERS_MODEL"
    )

    # ── Scout Sources ─────────────────────────────────────────────────────────
    scout_github_query: str = Field(
        default="agentic language:Python stars:>200", alias="SCOUT_GITHUB_QUERY"
    )
    scout_arxiv_query: str = Field(default="cat:cs.AI", alias="SCOUT_ARXIV_QUERY")
    scout_hn_feed: str = Field(
        default="https://hnrss.org/frontpage.atom", alias="SCOUT_HN_FEED"
    )
    scout_huggingface_enabled: bool = Field(default=True, alias="SCOUT_HUGGINGFACE_ENABLED")
    scout_huggingface_query: str = Field(
        default="multi-agent llm tools", alias="SCOUT_HUGGINGFACE_QUERY"
    )
    scout_extra_rss_feeds: str = Field(
        default=(
            "https://www.reddit.com/r/MachineLearning/.rss,"
            "https://www.reddit.com/r/LocalLLaMA/.rss,"
            "https://paperswithcode.com/rss.xml"
        ),
        alias="SCOUT_EXTRA_RSS_FEEDS",
    )
    scout_min_relevance_score: float = Field(
        default=0.45, alias="SCOUT_MIN_RELEVANCE_SCORE"
    )
    scout_allowed_licenses: str = Field(
        default="MIT,Apache-2.0,GPL-2.0,GPL-3.0,LGPL-2.1,LGPL-3.0,BSD-2-Clause,BSD-3-Clause,MPL-2.0,CC-BY-4.0,CC0-1.0,NOASSERTION",
        alias="SCOUT_ALLOWED_LICENSES",
    )

    # ── Ingestion ─────────────────────────────────────────────────────────────
    ingest_max_content_chars: int = Field(default=40_000, alias="INGEST_MAX_CONTENT_CHARS")
    ingest_chunk_size: int = Field(default=6_000, alias="INGEST_CHUNK_SIZE")
    ingest_chunk_overlap: int = Field(default=400, alias="INGEST_CHUNK_OVERLAP")
    ingest_respect_robots_txt: bool = Field(default=True, alias="INGEST_RESPECT_ROBOTS_TXT")

    # ── Linking ───────────────────────────────────────────────────────────────
    link_similarity_threshold: float = Field(
        default=0.78, alias="LINK_SIMILARITY_THRESHOLD"
    )
    link_max_edges_per_node: int = Field(default=12, alias="LINK_MAX_EDGES_PER_NODE")

    # ── Gardener / Decay ──────────────────────────────────────────────────────
    decay_half_life_days: int = Field(default=90, alias="DECAY_HALF_LIFE_DAYS")
    prune_threshold: float = Field(default=0.15, alias="PRUNE_THRESHOLD")
    resurrect_threshold: float = Field(default=0.65, alias="RESURRECT_THRESHOLD")
    deadlink_check_enabled: bool = Field(default=True, alias="DEADLINK_CHECK_ENABLED")
    deadlink_batch_size: int = Field(default=100, alias="DEADLINK_BATCH_SIZE")
    deadlink_timeout_secs: float = Field(default=8.0, alias="DEADLINK_TIMEOUT_SECS")

    # ── Pulse / Discord ───────────────────────────────────────────────────────
    discord_webhook: Optional[str] = Field(default=None, alias="DISCORD_WEBHOOK")
    pulse_enabled: bool = Field(default=True, alias="PULSE_ENABLED")

    # ── Scheduler ─────────────────────────────────────────────────────────────
    scheduler_timezone: str = Field(default="UTC", alias="SCHEDULER_TIMEZONE")

    # ── Canon / Governance ────────────────────────────────────────────────────
    canon_version: str = Field(default="v1.0", alias="CANON_VERSION")

    # ── Project Goals (used in relevance scoring) ─────────────────────────────
    project_goals: str = Field(
        default=(
            "Self-regulating AI OS; neural knowledge graph; autonomous agent ingestion; "
            "semantic memory; multi-agent orchestration; open-source tooling"
        ),
        alias="PROJECT_GOALS",
    )

    @property
    def allowed_licenses_set(self) -> set:
        return {s.strip() for s in self.scout_allowed_licenses.split(",") if s.strip()}

    @property
    def extra_rss_list(self) -> list:
        return [u.strip() for u in self.scout_extra_rss_feeds.split(",") if u.strip()]


settings = Settings()
