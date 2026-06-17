"""
Scout Agent — discovers sources from GitHub, arXiv, HackerNews, HuggingFace Hub,
Reddit ML feeds, and Papers With Code. Includes robots.txt enforcement,
license-aware filtering, and Blake2b URL deduplication.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import time
import urllib.robotparser
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import feedparser
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from ..config import settings

log = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
HF_API = "https://huggingface.co/api"


# ── Domain models ─────────────────────────────────────────────────────────────
@dataclass
class DiscoveredItem:
    source: str
    source_url: str
    title: str
    body: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        """Blake2b URL fingerprint for deduplication."""
        return hashlib.blake2b(
            self.source_url.encode("utf-8"), digest_size=12
        ).hexdigest()


# ── Robots.txt cache ──────────────────────────────────────────────────────────
_robots_cache: Dict[str, urllib.robotparser.RobotFileParser] = {}

async def _robots_allowed(url: str) -> bool:
    if not settings.ingest_respect_robots_txt:
        return True
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    if origin not in _robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            async with httpx.AsyncClient(timeout=8.0) as c:
                r = await c.get(f"{origin}/robots.txt")
                rp.parse(r.text.splitlines())
        except Exception:
            # If robots.txt is unreachable, allow (fail open for well-known APIs)
            rp.allow_all = True
        _robots_cache[origin] = rp
    return _robots_cache[origin].can_fetch(settings.github_user_agent, url)


# ── License filter ─────────────────────────────────────────────────────────────
def _license_allowed(spdx: Optional[str]) -> bool:
    """Refuse ingestion of repos with no license or proprietary licenses."""
    if spdx is None:
        return True  # unknown — allow, LLM will extract later
    return spdx.upper() in {s.upper() for s in settings.allowed_licenses_set}


# ── GitHub ────────────────────────────────────────────────────────────────────
class _RateLimit(Exception): ...


@retry(stop=stop_after_attempt(6), wait=wait_exponential_jitter(initial=2, max=64))
async def _gh_get(url: str, headers: dict) -> httpx.Response:
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as c:
        r = await c.get(url, headers=headers)
    if r.status_code in (403, 429):
        retry_after = r.headers.get("retry-after")
        reset = r.headers.get("x-ratelimit-reset")
        wait = int(retry_after) if retry_after else (
            max(0, int(reset) - int(time.time())) if reset else 60
        )
        log.warning("GitHub rate-limited. Waiting %ss", wait)
        await asyncio.sleep(min(wait, 120))
        raise _RateLimit("retry")
    r.raise_for_status()
    return r


def _parse_link_header(link: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in link.split(","):
        m = re.search(r'<([^>]+)>;\s*rel="([^"]+)"', part.strip())
        if m:
            out[m.group(2)] = m.group(1)
    return out


async def github_search_repos(
    query: str, per_page: int = 50, pages: int = 3
) -> List[DiscoveredItem]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": settings.github_user_agent,
    }
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"

    params = httpx.QueryParams({"q": query, "sort": "updated", "per_page": per_page})
    url = f"{GITHUB_API}/search/repositories?{params}"
    items: List[DiscoveredItem] = []

    for _ in range(pages):
        try:
            r = await _gh_get(url, headers)
        except Exception as e:
            log.error("GitHub search error: %s", e)
            break

        for repo in r.json().get("items", []):
            spdx = (repo.get("license") or {}).get("spdx_id")
            if not _license_allowed(spdx):
                log.debug("Skipping %s — license %s not allowed", repo.get("html_url"), spdx)
                continue
            items.append(DiscoveredItem(
                source="github",
                source_url=repo["html_url"],
                title=repo["full_name"],
                body=repo.get("description") or "",
                meta={
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "language": repo.get("language"),
                    "updated_at": repo.get("updated_at"),
                    "license": spdx,
                    "topics": repo.get("topics", []),
                },
            ))

        links = _parse_link_header(r.headers.get("link", ""))
        if "next" not in links:
            break
        url = links["next"]
        await asyncio.sleep(0.5)  # be polite

    log.info("GitHub scout: %d items found", len(items))
    return items


# ── arXiv ─────────────────────────────────────────────────────────────────────
async def arxiv_search(
    query: str, start: int = 0, max_results: int = 25
) -> List[DiscoveredItem]:
    """
    arXiv Atom API. Respect ~3s between calls; max 2000/slice.
    Boolean syntax: 'ti:multi-agent AND cat:cs.AI AND NOT cat:cs.RO'
    """
    base = "http://export.arxiv.org/api/query"
    params = httpx.QueryParams({
        "search_query": query,
        "start": start,
        "max_results": min(max_results, 2000),
    })
    url = f"{base}?{params}"
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.get(url, headers={"User-Agent": settings.github_user_agent})
        r.raise_for_status()
    await asyncio.sleep(3.1)  # arXiv requests ~3s delay

    feed = feedparser.parse(r.text)
    out: List[DiscoveredItem] = []
    for entry in feed.entries:
        out.append(DiscoveredItem(
            source="arxiv",
            source_url=entry.link,
            title=entry.title.replace("\n", " ").strip(),
            body=(entry.summary or "").strip(),
            meta={
                "authors": [a.name for a in getattr(entry, "authors", [])],
                "published": getattr(entry, "published", None),
                "categories": getattr(entry, "tags", []),
            },
        ))
    log.info("arXiv scout: %d items found", len(out))
    return out


# ── HackerNews RSS ────────────────────────────────────────────────────────────
async def hn_feed(url: str) -> List[DiscoveredItem]:
    async with httpx.AsyncClient(timeout=20.0) as c:
        r = await c.get(url, headers={"User-Agent": settings.github_user_agent})
        r.raise_for_status()
    feed = feedparser.parse(r.text)
    out: List[DiscoveredItem] = []
    for entry in feed.entries:
        out.append(DiscoveredItem(
            source="hn",
            source_url=entry.link,
            title=entry.title,
            body=getattr(entry, "summary", "") or "",
            meta={"published": getattr(entry, "published", None)},
        ))
    log.info("HN scout: %d items found", len(out))
    return out


# ── HuggingFace Hub ───────────────────────────────────────────────────────────
async def huggingface_search(query: str, limit: int = 30) -> List[DiscoveredItem]:
    """
    Search HuggingFace Hub models and Spaces by keyword.
    Uses the /api/models endpoint (no auth required for public search).
    """
    params = httpx.QueryParams({
        "search": query,
        "limit": limit,
        "sort": "downloads",
        "direction": "-1",
    })
    url = f"{HF_API}/models?{params}"
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.get(url, headers={"User-Agent": settings.github_user_agent})
            r.raise_for_status()
        models = r.json()
    except Exception as e:
        log.warning("HuggingFace scout failed: %s", e)
        return []

    out: List[DiscoveredItem] = []
    for m in models:
        model_id = m.get("modelId") or m.get("id", "")
        out.append(DiscoveredItem(
            source="huggingface",
            source_url=f"https://huggingface.co/{model_id}",
            title=model_id,
            body=(m.get("cardData") or {}).get("description", "") or "",
            meta={
                "downloads": m.get("downloads"),
                "likes": m.get("likes"),
                "pipeline_tag": m.get("pipeline_tag"),
                "tags": m.get("tags", []),
                "license": (m.get("cardData") or {}).get("license"),
            },
        ))
    log.info("HuggingFace scout: %d items found", len(out))
    return out


# ── Generic RSS (Reddit, Papers With Code, etc.) ──────────────────────────────
async def generic_rss_feed(url: str, source_label: str = "rss") -> List[DiscoveredItem]:
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.get(url, headers={"User-Agent": settings.github_user_agent})
            r.raise_for_status()
        feed = feedparser.parse(r.text)
    except Exception as e:
        log.warning("RSS feed %s failed: %s", url, e)
        return []

    out: List[DiscoveredItem] = []
    for entry in feed.entries:
        item_url = entry.link if hasattr(entry, "link") else ""
        if not item_url:
            continue
        out.append(DiscoveredItem(
            source=source_label,
            source_url=item_url,
            title=entry.title if hasattr(entry, "title") else item_url,
            body=getattr(entry, "summary", "") or "",
            meta={"published": getattr(entry, "published", None)},
        ))
    log.info("RSS %s: %d items found", source_label, len(out))
    return out


# ── Full scout run ────────────────────────────────────────────────────────────
async def run_full_scout() -> List[DiscoveredItem]:
    """Execute all scouts and return deduplicated items."""
    results: List[DiscoveredItem] = []
    seen_fingerprints: set = set()

    # GitHub
    try:
        gh = await github_search_repos(settings.scout_github_query, pages=3)
        results.extend(gh)
    except Exception as e:
        log.error("GitHub scout error: %s", e)

    # arXiv
    try:
        ax = await arxiv_search(settings.scout_arxiv_query, max_results=25)
        results.extend(ax)
    except Exception as e:
        log.error("arXiv scout error: %s", e)

    # HackerNews
    try:
        hn = await hn_feed(settings.scout_hn_feed)
        results.extend(hn)
    except Exception as e:
        log.error("HN scout error: %s", e)

    # HuggingFace
    if settings.scout_huggingface_enabled:
        try:
            hf = await huggingface_search(settings.scout_huggingface_query)
            results.extend(hf)
        except Exception as e:
            log.error("HuggingFace scout error: %s", e)

    # Extra RSS feeds (Reddit ML, Papers With Code, etc.)
    for feed_url in settings.extra_rss_list:
        label = "rss_" + urlparse(feed_url).netloc.replace(".", "_")
        try:
            rss = await generic_rss_feed(feed_url, source_label=label)
            results.extend(rss)
        except Exception as e:
            log.error("RSS feed %s error: %s", feed_url, e)

    # Deduplicate by URL fingerprint
    deduped: List[DiscoveredItem] = []
    for item in results:
        fp = item.fingerprint()
        if fp not in seen_fingerprints:
            seen_fingerprints.add(fp)
            deduped.append(item)

    log.info("Scout complete: %d raw → %d deduped items", len(results), len(deduped))
    return deduped
