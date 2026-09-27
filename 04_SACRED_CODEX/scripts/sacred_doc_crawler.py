"""
sacred_doc_crawler.py
=====================
SacredSpace OS — Web Scout (Documentation Crawler)
Pillar: 03_NEURAL_FOREST
Owner Agent: AURORA

Crawls documentation sites and ingests every page as a MemoryMote
into the RAW tier (SQLite + ChromaDB) via sacred_ingest_core.ingest().

Uses crawl4ai for headless Chromium crawling with clean Markdown output.
Runs fully headless in WSL2 — no DISPLAY required.

Usage:
    python3 sacred_doc_crawler.py
    python3 sacred_doc_crawler.py --url https://docs.example.com --max 50
"""

import asyncio
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

# ─── PATH SETUP ───────────────────────────────────────────────────────────────
NEURAL_FOREST = Path.home() / "SacredSpace_OS" / "03_NEURAL_FOREST"
sys.path.insert(0, str(NEURAL_FOREST))

try:
    from sacred_ingest_core import ingest, MemoryMote, BaseConnector
except ImportError as e:
    raise RuntimeError(
        f"Cannot import sacred_ingest_core from {NEURAL_FOREST}\n"
        f"Ensure sacred_ingest_core.py is at that path.\nError: {e}"
    )

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

DEFAULT_MAX_PAGES = 20
DEFAULT_PILLAR    = "03_NEURAL_FOREST"
DEFAULT_AGENT     = "AURORA"

BROWSER_ARGS = [
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-setuid-sandbox",
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def clean_markdown(text: str) -> str:
    """Strip navigation noise and boilerplate from crawled Markdown."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").strip()
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    for pattern in [
        r"Was this page helpful\?", r"Yes\s*No", r"Copy page",
        r"Edit this page", r"Report an issue", r"Last updated.*",
    ]:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [l for l in text.splitlines()
             if not re.match(r"^\s*[|—\-_=]{3,}\s*$", l)]
    return "\n".join(lines).strip()


def extract_tags_from_url(url: str) -> list:
    """Generate semantic tags from a URL path."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "").replace(".", "_")
        parts  = [p for p in parsed.path.split("/") if p and len(p) > 2]
        return [domain] + parts[:4]
    except Exception:
        return ["web_crawl"]


# ─── CONNECTOR ────────────────────────────────────────────────────────────────

class WebScoutConnector(BaseConnector):
    """
    crawl4ai-powered documentation site crawler.

    Crawls a documentation URL up to max_pages deep, converts each page
    to clean Markdown, and returns MemoryMotes ready for RAW tier ingestion.
    """

    def __init__(self, start_url, max_pages=DEFAULT_MAX_PAGES,
                 pillar=DEFAULT_PILLAR, agent=DEFAULT_AGENT, extra_tags=None):
        self.start_url  = start_url
        self.max_pages  = max_pages
        self.pillar     = pillar
        self.agent      = agent
        self.extra_tags = extra_tags or []

    def collect(self) -> list:
        """Synchronous entry point — runs the async crawl."""
        return asyncio.run(self._crawl())

    async def _crawl(self) -> list:
        """Core async crawl loop using crawl4ai AsyncWebCrawler."""
        try:
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        except ImportError:
            raise RuntimeError(
                "crawl4ai not installed.\n"
                "Run: pip install crawl4ai --break-system-packages\n"
                "     python -m playwright install --with-deps"
            )

        motes   = []
        visited = set()
        queue   = [self.start_url]
        base_domain = urlparse(self.start_url).netloc

        browser_cfg = BrowserConfig(headless=True, extra_args=BROWSER_ARGS)
        run_cfg = CrawlerRunConfig(
            word_count_threshold=10,
            excluded_tags=["nav", "footer", "header", "aside"],
            remove_overlay_elements=True,
        )

        print(f"\n[SCOUT] Starting crawl of {self.start_url}")
        print(f"[SCOUT] Max pages: {self.max_pages} | Pillar: {self.pillar}\n")

        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            page_count = 0

            while queue and page_count < self.max_pages:
                url = queue.pop(0)
                if url in visited:
                    continue
                visited.add(url)
                page_count += 1

                print(f"[SCOUT] Crawling page {page_count}/{self.max_pages}: {url}")

                try:
                    result = await crawler.arun(url=url, config=run_cfg)

                    if not result.success:
                        print(f"  [SCOUT ✗] Failed: {result.error_message}")
                        continue

                    markdown = clean_markdown(result.markdown or "")

                    if len(markdown) < 100:
                        print(f"  [SCOUT —] Skipping (too short: {len(markdown)} chars)")
                        continue

                    tags    = extract_tags_from_url(url) + self.extra_tags + ["web_crawl"]
                    mote_id = self.fingerprint(markdown)

                    mote = MemoryMote(
                        mote_id  = mote_id,
                        content  = markdown,
                        source   = "web_crawl",
                        pillar   = self.pillar,
                        agent    = self.agent,
                        tags     = list(set(tags)),
                        metadata = {
                            "url":        url,
                            "crawled_at": datetime.now(timezone.utc).isoformat(),
                            "char_count": len(markdown),
                            "start_url":  self.start_url,
                        }
                    )
                    motes.append(mote)
                    print(f"  [SCOUT ✓] {len(markdown):,} chars → mote {mote_id[:8]}...")

                    # Discover new same-domain links
                    if result.links:
                        for link in result.links.get("internal", []):
                            href = link.get("href", "")
                            if href and href not in visited and href not in queue:
                                link_domain = urlparse(href).netloc
                                if not link_domain or link_domain == base_domain:
                                    queue.append(href)

                except Exception as exc:
                    print(f"  [SCOUT ✗] Error on {url}: {exc}")
                    continue

        print(f"\n[SCOUT] Crawl complete — {len(motes)} pages collected")
        return motes


# ─── MAIN FUNCTION ────────────────────────────────────────────────────────────

def crawl_and_ingest(start_url, max_pages=DEFAULT_MAX_PAGES,
                     pillar=DEFAULT_PILLAR, agent=DEFAULT_AGENT,
                     extra_tags=None, skip_chroma=False) -> list:
    """
    Crawl a documentation site and ingest all pages into SacredSpace OS.

    Primary entry point for the Web Scout layer.

    Args:
        start_url:   Root URL to begin crawling from.
        max_pages:   Maximum number of pages to crawl.
        pillar:      Target SacredSpace pillar for all motes.
        agent:       Owning ICARIS agent.
        extra_tags:  Additional tags to apply to all motes.
        skip_chroma: Skip ChromaDB write (SQLite only, faster for testing).

    Returns:
        list[MemoryMote]: All ingested motes.
    """
    extra_tags = extra_tags or []
    connector  = WebScoutConnector(start_url, max_pages, pillar, agent, extra_tags)
    motes      = connector.collect()

    if not motes:
        print("[SCOUT] No pages collected — check URL and network.")
        return []

    print(f"\n[SCOUT] Ingesting {len(motes)} motes into Memory Engine...")
    ingested = []

    for i, mote in enumerate(motes, 1):
        print(f"[SCOUT] Ingesting {i}/{len(motes)}: {mote.mote_id[:8]}...")
        result = ingest(
            content     = mote.content,
            source      = mote.source,
            pillar      = mote.pillar,
            agent       = mote.agent,
            tags        = mote.tags,
            metadata    = mote.metadata,
            skip_chroma = skip_chroma,
        )
        ingested.append(result)

    print(f"\n[SCOUT] ✓ Complete — {len(ingested)} motes in the Forest")
    return ingested


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SacredSpace Web Scout — crawl docs into Memory Engine"
    )
    parser.add_argument("--url",      default="https://docs.crawl4ai.com",
                        help="Documentation URL to crawl")
    parser.add_argument("--max",      type=int, default=5,
                        help="Maximum pages to crawl (default: 5)")
    parser.add_argument("--pillar",   default="03_NEURAL_FOREST",
                        help="SacredSpace pillar")
    parser.add_argument("--agent",    default="AURORA",
                        help="ICARIS agent owner")
    parser.add_argument("--no-chroma", action="store_true",
                        help="Skip ChromaDB, SQLite only")
    args = parser.parse_args()

    print("=" * 60)
    print("∆∆∆ SACRED WEB SCOUT — NEURAL FOREST CRAWLER ∆∆∆")
    print(f"URL:    {args.url}")
    print(f"Max:    {args.max} pages")
    print(f"Pillar: {args.pillar}")
    print(f"Agent:  {args.agent}")
    print("=" * 60)

    motes = crawl_and_ingest(
        start_url   = args.url,
        max_pages   = args.max,
        pillar      = args.pillar,
        agent       = args.agent,
        skip_chroma = args.no_chroma,
    )

    print("\n" + "=" * 60)
    print(f"∆ WEB SCOUT COMPLETE — {len(motes)} motes in the Forest ∆")
    print("=" * 60)
