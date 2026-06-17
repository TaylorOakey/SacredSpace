"""
Ingestor Agent — fetches, normalizes, chunks, extracts, embeds, and upserts Nodes.
Includes robots.txt enforcement, license filtering, and quality gating.
"""
from __future__ import annotations

import logging
import textwrap
from typing import List, Optional

from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .embeddings import build_embeddings_provider
from .http import fetch_text
from .llm import build_llm_provider
from .scout import DiscoveredItem, _robots_allowed, _license_allowed
from ..config import settings

log = logging.getLogger(__name__)


# ── Text normalization ────────────────────────────────────────────────────────
def normalize_html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header"]):
        tag.decompose()
    raw = soup.get_text("\n")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    return "\n".join(lines)


# ── Chunking ──────────────────────────────────────────────────────────────────
def chunk_text(text_in: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split text into sentence-aware chunks. Splits on newlines first,
    then falls back to character slicing. Avoids cutting mid-sentence.
    """
    if len(text_in) <= chunk_size:
        return [text_in]

    # Split into paragraphs
    paragraphs = [p.strip() for p in text_in.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > chunk_size:
            if current:
                chunks.append(current.strip())
            # If a single para is huge, hard-split it
            if len(para) > chunk_size:
                for i in range(0, len(para), chunk_size - overlap):
                    chunks.append(para[i:i + chunk_size])
                current = ""
            else:
                current = para
        else:
            current = (current + "\n\n" + para).strip() if current else para

    if current:
        chunks.append(current.strip())

    return chunks or [text_in[:chunk_size]]


def merge_chunk_summaries(summaries: List[str]) -> str:
    """Merge LLM chunk summaries into one coherent body under 1200 chars."""
    merged = " | ".join(s.strip() for s in summaries if s.strip())
    if len(merged) > 1200:
        merged = merged[:1197] + "..."
    return merged


# ── Node ID ───────────────────────────────────────────────────────────────────
import hashlib

def node_id_from_url(url: str) -> str:
    return hashlib.blake2b(url.encode("utf-8"), digest_size=12).hexdigest()


# ── Ingestor ──────────────────────────────────────────────────────────────────
class Ingestor:
    def __init__(self):
        self.llm = build_llm_provider()
        self.emb = build_embeddings_provider()

    async def _fetch_content(self, url: str) -> str:
        """Fetch URL content with robots.txt check."""
        if not await _robots_allowed(url):
            raise PermissionError(f"robots.txt disallows crawling: {url}")
        raw = await fetch_text(url)
        if "<html" in raw.lower():
            return normalize_html_to_text(raw)
        return raw

    async def _extract_with_chunking(self, content: str, source_url: str) -> dict:
        """
        For large documents: chunk → extract each chunk summary → merge.
        For small documents: single LLM call.
        """
        chunk_size = settings.ingest_chunk_size
        overlap = settings.ingest_chunk_overlap

        if len(content) <= chunk_size:
            result = await self.llm.extract_metadata(content, source_url)
            return result.data

        # Multi-chunk extraction
        chunks = chunk_text(content, chunk_size, overlap)
        log.debug("Chunking %s into %d chunks", source_url, len(chunks))

        first_result = await self.llm.extract_metadata(chunks[0], source_url)
        data = first_result.data.copy()

        # Extract summaries from remaining chunks
        extra_summaries: List[str] = []
        for chunk in chunks[1:]:
            try:
                r = await self.llm.extract_metadata(chunk, source_url)
                if r.data.get("summary"):
                    extra_summaries.append(r.data["summary"])
            except Exception as e:
                log.warning("Chunk extraction failed: %s", e)

        if extra_summaries:
            all_summaries = [data.get("summary", "")] + extra_summaries
            data["summary"] = merge_chunk_summaries(all_summaries)

        return data

    async def ingest_item(self, db: AsyncSession, item: DiscoveredItem) -> str:
        node_id = node_id_from_url(item.source_url)

        # ── Check for license in meta (GitHub provides it pre-flight) ────────
        known_license = item.meta.get("license") if item.meta else None
        if known_license and not _license_allowed(known_license):
            log.info("Skipping %s — proprietary license: %s", item.source_url, known_license)
            # Insert as sealed node so we don't re-ingest it
            await self._insert_sealed(db, node_id, item, known_license)
            return node_id

        # ── Fetch content ─────────────────────────────────────────────────────
        try:
            content = await self._fetch_content(item.source_url)
        except PermissionError as e:
            log.warning(str(e))
            return node_id
        except Exception as e:
            log.error("Fetch failed for %s: %s", item.source_url, e)
            content = (item.body or "")

        # Trim total content
        content = content[:settings.ingest_max_content_chars]
        if not content.strip():
            content = item.body or item.title

        # ── LLM extraction (with chunking) ────────────────────────────────────
        try:
            data = await self._extract_with_chunking(content, item.source_url)
        except Exception as e:
            log.error("LLM extraction failed for %s: %s", item.source_url, e)
            data = {
                "title": item.title,
                "summary": item.body or "",
                "tags": [item.source],
                "license": known_license,
                "quality": {"relevance": 0.5, "credibility": 0.5, "freshness": 0.5},
            }

        # ── Quality gate ─────────────────────────────────────────────────────
        quality = data.get("quality") or {}
        avg_quality = (
            float(quality.get("relevance", 0))
            + float(quality.get("credibility", 0))
            + float(quality.get("freshness", 0))
        ) / 3.0
        if avg_quality < settings.scout_min_relevance_score:
            log.info("Skipping %s — quality score %.2f below threshold", item.source_url, avg_quality)
            return node_id

        # ── Re-check extracted license ────────────────────────────────────────
        extracted_license = data.get("license") or known_license
        if extracted_license and not _license_allowed(extracted_license):
            log.info("Skipping %s — extracted license not allowed: %s", item.source_url, extracted_license)
            await self._insert_sealed(db, node_id, item, extracted_license)
            return node_id

        # ── Embed ─────────────────────────────────────────────────────────────
        embed_text = (data.get("title") or item.title) + "\n" + (data.get("summary") or "")
        emb_res = self.emb.embed_text(embed_text)

        # ── Tags from multiple sources ────────────────────────────────────────
        tags = list(set(
            (data.get("tags") or [])
            + [item.source]
            + (item.meta.get("topics", []) if item.meta else [])
        ))

        # ── Upsert Node ───────────────────────────────────────────────────────
        q = text("""
            INSERT INTO forest_nodes
              (id, title, node_type, source_url, body, tags, license,
               embedding, embedding_hash, resurrection_score, updated_at)
            VALUES
              (:id, :title, :node_type, :source_url, :body, :tags::jsonb, :license,
               :embedding, :embedding_hash, 0.75, NOW())
            ON CONFLICT (id) DO UPDATE SET
              title = EXCLUDED.title,
              body  = EXCLUDED.body,
              tags  = EXCLUDED.tags,
              license = EXCLUDED.license,
              embedding = EXCLUDED.embedding,
              embedding_hash = EXCLUDED.embedding_hash,
              updated_at = NOW()
        """)
        import json
        await db.execute(q, dict(
            id=node_id,
            title=(data.get("title") or item.title)[:240],
            node_type=item.source,
            source_url=item.source_url,
            body=data.get("summary") or (item.body or "")[:1200],
            tags=json.dumps(tags),
            license=extracted_license,
            embedding=str(emb_res.vector),
            embedding_hash=emb_res.embedding_hash,
        ))
        await db.commit()
        log.info("Ingested node %s [%s]", node_id, item.source_url[:80])
        return node_id

    async def _insert_sealed(
        self, db: AsyncSession, node_id: str, item: DiscoveredItem, reason: str
    ):
        import json
        q = text("""
            INSERT INTO forest_nodes
              (id, title, node_type, source_url, body, tags, license, updated_at)
            VALUES
              (:id, :title, :node_type, :source_url, :body, :tags::jsonb, :license, NOW())
            ON CONFLICT (id) DO NOTHING
        """)
        await db.execute(q, dict(
            id=node_id,
            title=item.title[:240],
            node_type=item.source,
            source_url=item.source_url,
            body=f"[SEALED: license={reason}]",
            tags=json.dumps(["sealed", item.source]),
            license=reason,
        ))
        await db.commit()
