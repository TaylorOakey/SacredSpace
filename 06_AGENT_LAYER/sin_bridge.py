"""
SIN Bridge — SacredSpace Intelligence Network integration.

Implements the 3-tier discovery pipeline discovered in ChatGPT's
S@CR3D !NSTRUCT!ONS project, connecting it to the local agent ecosystem.

SIN Pipeline Architecture (from ChatGPT):
  Tier 1: Seed Sources  → Google Sheets (seed data, Twitter, arXiv, Podcasts, YouTube, Wikipedia)
  Tier 2: Drive Vault   → Sorted folders (Spirituality, Coding, Sacred, Business, Creative)
  Tier 3: OmniLedger    → Curated Canon (cross-referenced against existing knowledge)

Local Integration:
  Tier 1 → scout.py (existing source discovery) + Google Sheets API
  Tier 2 → ingestor.py (existing: fetch → normalize → chunk → embed → upsert)
  Tier 3 → supervisor.py (existing: canon gate, audit logging)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)

# ── SIN Tiers ──────────────────────────────────────────────────────────────────

class SINTier(Enum):
    SEED = "tier1_seed"       # Raw source discovery
    VAULT = "tier2_vault"     # Sorted/organized content
    OMNILEDGER = "tier3_omni" # Curated canonical knowledge

SIN_PILLAR_MAP = {
    "spirituality": "01_CORE",
    "coding": "06_AGENTS",
    "sacred": "04_CODEX",
    "business": "09_MARKET",
    "creative": "07_SOCIAL",
}


@dataclass
class SINRecord:
    """A single item flowing through the SIN pipeline."""
    source: str                    # Original source identifier
    source_url: str                # Original URL
    title: str                     # Human-readable title
    tier: SINTier                  # Current pipeline tier
    pillar_target: Optional[str]   # Target pillar folder (e.g. "04_CODEX")
    body: Optional[str] = None     # Extracted text content
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def fingerprint(self) -> str:
        """Deterministic dedup key."""
        import hashlib
        return hashlib.blake2b(
            self.source_url.encode("utf-8"), digest_size=12
        ).hexdigest()


# ── Tier 1: Seed Source Discovery ──────────────────────────────────────────────

SEED_SOURCES = {
    "arxiv": {
        "url": "https://export.arxiv.org/api/query?search_query=all:SacredSpace&max_results=10",
        "type": "api",
        "parser": "_parse_arxiv",
    },
    "youtube": {
        "url": "https://www.youtube.com/@SacredSpaceOS",
        "type": "channel",
        "parser": None,
    },
    "twitter": {
        "url": "https://x.com/SacredSpaceOS",
        "type": "profile",
        "parser": None,
    },
    "podcasts": {
        "url": None,  # Manual entry via Google Sheets
        "type": "sheet",
        "parser": None,
    },
    "wikipedia": {
        "url": "https://en.wikipedia.org/w/index.php?search=SacredSpace",
        "type": "search",
        "parser": None,
    },
}


async def tier1_discover(
    custom_sheet_id: Optional[str] = None,
    max_results: int = 20,
) -> List[SINRecord]:
    """
    Tier 1: Discover seed sources from configured feeds and/or Google Sheets.

    Uses the existing scout.py infrastructure where available, with Google
    Sheets integration for manual seed entries.
    """
    records: List[SINRecord] = []

    # Attempt Google Sheets read if sheet ID provided
    if custom_sheet_id:
        sheet_records = await _read_google_sheet(custom_sheet_id)
        records.extend(sheet_records)
        log.info(f"SIN Tier1: {len(sheet_records)} records from Google Sheet")

    # arXiv query
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(SEED_SOURCES["arxiv"]["url"])
            if resp.status_code == 200:
                parsed = _parse_atom_feed(resp.text)
                for entry in parsed:
                    records.append(SINRecord(
                        source="arxiv",
                        source_url=entry.get("id", ""),
                        title=entry.get("title", "Untitled"),
                        tier=SINTier.SEED,
                        pillar_target=_classify_pillar(entry.get("title", "") + " " + entry.get("summary", "")),
                        body=entry.get("summary"),
                        tags=["arxiv", "research"],
                    ))
                log.info(f"SIN Tier1: {len(parsed)} records from arXiv")
            else:
                log.warning(f"SIN Tier1: arXiv returned {resp.status_code}")
    except Exception as e:
        log.warning(f"SIN Tier1: arXiv query failed: {e}")

    # Wikipedia search
    try:
        wiki_url = (
            "https://en.wikipedia.org/w/api.php"
            "?action=query&list=search&srsearch=SacredSpace&format=json&srlimit=10"
        )
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(wiki_url)
            if resp.status_code == 200:
                data = resp.json()
                for result in data.get("query", {}).get("search", []):
                    page_title = result.get("title", "")
                    page_id = result.get("pageid", "")
                    records.append(SINRecord(
                        source="wikipedia",
                        source_url=f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                        title=page_title,
                        tier=SINTier.SEED,
                        pillar_target=_classify_pillar(page_title),
                        body=result.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
                        tags=["wikipedia", "reference"],
                        meta={"pageid": page_id},
                    ))
                log.info(f"SIN Tier1: {len(data.get('query', {}).get('search', []))} records from Wikipedia")
    except Exception as e:
        log.warning(f"SIN Tier1: Wikipedia query failed: {e}")

    return records[:max_results]


# ── Tier 2: Vault Organization ─────────────────────────────────────────────────

async def tier2_organize(records: List[SINRecord]) -> List[SINRecord]:
    """
    Tier 2: Classify, tag, and route records to their target pillar folders.

    Assigns pillar_target based on content classification. Records already
    assigned keep their target; unassigned ones get auto-classified.
    """
    for record in records:
        if not record.pillar_target:
            content = f"{record.title} {record.body or ''}"
            record.pillar_target = _classify_pillar(content)
        if "spirituality" not in [t.lower() for t in record.tags]:
            _auto_tag(record)
    return records


def _classify_pillar(text: str) -> str:
    """Classify text to a SacredSpace pillar."""
    text_lower = text.lower()
    classifications = [
        (r"\b(vault|obsidian|yaml|archive)\b", "01_CORE"),
        (r"\b(council|vote|consensus|governance|session)\b", "02_COUNCIL_GROVE"),
        (r"\b(neural|knowledge|rag|embed|vector|chroma|notebooklm)\b", "03_NEURAL"),
        (r"\b(codex|canon|spell|skry|grimoire|sacred law)\b", "04_CODEX"),
        (r"\b(memory|mote|ash|chroma|sqlite|redis|decay)\b", "05_MEMORY_ENGINE"),
        (r"\b(agent|mcp|icaris|hermes|elias|aurora|scout)\b", "06_AGENTS"),
        (r"\b(social|signal|content|kickstarter|creation)\b", "07_SOCIAL"),
        (r"\b(learning|path|skill|rite|education)\b", "08_LEARNING"),
        (r"\b(market|revenue|pod|etsy|store|commerce|merchant)\b", "09_MARKET"),
    ]
    for pattern, pillar in classifications:
        if re.search(pattern, text_lower):
            return pillar
    # Default to CODEX for uncategorized canon-worthy content
    return "04_CODEX"


def _auto_tag(record: SINRecord) -> None:
    """Auto-tag a record based on content."""
    text = f"{record.title} {record.body or ''}".lower()
    tag_map = {
        "tutorial": ["guide", "how to", "tutorial", "walkthrough"],
        "reference": ["documentation", "wiki", "reference", "spec"],
        "creative": ["art", "design", "music", "sound", "visual"],
        "technical": ["code", "api", "sdk", "library", "function"],
        "business": ["revenue", "market", "price", "customer", "product"],
        "spiritual": ["sacred", "spirit", "meditation", "consciousness", "canon"],
    }
    for tag, keywords in tag_map.items():
        if any(kw in text for kw in keywords):
            if tag not in record.tags:
                record.tags.append(tag)
    if not record.tags:
        record.tags.append("uncategorized")


# ── Tier 3: OmniLedger Curation ───────────────────────────────────────────────

@dataclass
class OmniLedgerEntry:
    """A curated entry in the OmniLedger (canonical knowledge store)."""
    fingerprint: str
    title: str
    source_url: str
    pillar: str
    summary: str
    status: str = "draft"  # draft → review → canon
    cross_references: List[str] = field(default_factory=list)
    curated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


async def tier3_curate(
    records: List[SINRecord],
    existing_fingerprints: Optional[set] = None,
) -> List[OmniLedgerEntry]:
    """
    Tier 3: Curate Tier-2 records into the OmniLedger.

    Deduplicates against existing fingerprints, generates summaries,
    and assigns cross-references.
    """
    existing = existing_fingerprints or set()
    entries: List[OmniLedgerEntry] = []

    for record in records:
        fp = record.fingerprint()
        if fp in existing:
            log.info(f"SIN Tier3: Skipping duplicate {record.title}")
            continue
        existing.add(fp)

        summary = _generate_summary(record)
        cross_refs = _find_cross_references(record)

        entries.append(OmniLedgerEntry(
            fingerprint=fp,
            title=record.title,
            source_url=record.source_url,
            pillar=record.pillar_target or "04_CODEX",
            summary=summary,
            status="draft",
            cross_references=cross_refs,
        ))

    log.info(f"SIN Tier3: {len(entries)} new OmniLedger entries created")
    return entries


def _generate_summary(record: SINRecord) -> str:
    """Generate a summary for a record."""
    body = record.body or ""
    if len(body) > 500:
        return body[:500] + "..."
    return body


def _find_cross_references(record: SINRecord) -> List[str]:
    """Find cross-references to other pillars/knowledge areas."""
    refs = []
    text = f"{record.title} {record.body or ''}".lower()
    # Map topics to potential cross-pillar references
    topic_map = {
        "01_CORE": ["vault", "obsidian", "archive", "yaml"],
        "02_COUNCIL_GROVE": ["governance", "council", "consensus", "vote"],
        "03_NEURAL": ["knowledge graph", "embedding", "vector", "rag"],
        "04_CODEX": ["canon", "spell", "skry", "sacred law"],
        "05_MEMORY_ENGINE": ["memory", "mote", "decay", "resurrection"],
        "06_AGENTS": ["agent", "mcp", "tool", "automation"],
        "07_SOCIAL": ["content", "social", "creation", "publish"],
        "08_LEARNING": ["learning", "skill", "path", "education"],
        "09_MARKET": ["revenue", "market", "product", "store"],
    }
    for pillar, keywords in topic_map.items():
        if any(kw in text for kw in keywords):
            if pillar != record.pillar_target:
                refs.append(pillar)
    return refs


# ── Google Sheets Integration ──────────────────────────────────────────────────

async def _read_google_sheet(sheet_id: str) -> List[SINRecord]:
    """
    Read a Google Sheet for seed source entries.

    Sheet format expected:
      title | url | category | notes
    """
    records: List[SINRecord] = []
    try:
        import httpx
        # Google Sheets export as CSV (public sheets only)
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(csv_url)
            if resp.status_code == 200:
                import csv
                import io
                reader = csv.DictReader(io.StringIO(resp.text))
                for row in reader:
                    title = row.get("title", row.get("Title", "Untitled"))
                    url = row.get("url", row.get("URL", row.get("Url", "")))
                    category = row.get("category", row.get("Category", ""))
                    notes = row.get("notes", row.get("Notes", ""))
                    if url:
                        records.append(SINRecord(
                            source=f"google_sheet:{sheet_id}",
                            source_url=url,
                            title=title,
                            tier=SINTier.SEED,
                            pillar_target=SIN_PILLAR_MAP.get(category.lower()),
                            body=notes,
                            tags=["seed", category.lower()] if category else ["seed"],
                            meta={"sheet_id": sheet_id},
                        ))
    except ImportError:
        log.warning("SIN: httpx not available, skipping Google Sheets")
    except Exception as e:
        log.warning(f"SIN: Google Sheets read failed: {e}")
    return records


# ── Atom Feed Parser ───────────────────────────────────────────────────────────

def _parse_atom_feed(xml_text: str) -> List[Dict[str, Any]]:
    """Minimal Atom feed parser (arXiv uses Atom)."""
    entries = []
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            entries.append({
                "id": entry.findtext("atom:id", "", ns),
                "title": entry.findtext("atom:title", "", ns),
                "summary": entry.findtext("atom:summary", "", ns),
                "updated": entry.findtext("atom:updated", "", ns),
            })
    except Exception as e:
        log.warning(f"SIN: Atom parse failed: {e}")
    return entries


# ── Full Pipeline Runner ───────────────────────────────────────────────────────

async def run_sin_pipeline(
    sheet_id: Optional[str] = None,
    max_sources: int = 20,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the full SIN 3-tier pipeline.

    Args:
        sheet_id: Optional Google Sheet ID for seed sources
        max_sources: Maximum records to process
        output_dir: Optional directory for pipeline output

    Returns:
        Pipeline summary with counts per tier
    """
    log.info("=== SIN Pipeline started ===")

    # Tier 1: Discover
    tier1_records = await tier1_discover(sheet_id, max_sources)
    log.info(f"Tier 1 complete: {len(tier1_records)} records discovered")

    if not tier1_records:
        return {"tier1": 0, "tier2": 0, "tier3": 0, "status": "no_sources"}

    # Tier 2: Organize
    tier2_records = await tier2_organize(tier1_records)
    pillar_counts = {}
    for r in tier2_records:
        p = r.pillar_target or "unknown"
        pillar_counts[p] = pillar_counts.get(p, 0) + 1
    log.info(f"Tier 2 complete: {len(tier2_records)} organized")
    log.info(f"Pillar distribution: {json.dumps(pillar_counts, indent=2)}")

    # Tier 3: Curate
    omni_entries = await tier3_curate(tier2_records)
    log.info(f"Tier 3 complete: {len(omni_entries)} curated entries")

    # Write output if directory specified
    if output_dir and omni_entries:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = out_path / f"sin_pipeline_{timestamp}.json"
        output_data = []
        for entry in omni_entries:
            output_data.append({
                "fingerprint": entry.fingerprint,
                "title": entry.title,
                "source_url": entry.source_url,
                "pillar": entry.pillar,
                "summary": entry.summary[:200] if entry.summary else "",
                "status": entry.status,
                "cross_references": entry.cross_references,
            })
        output_file.write_text(json.dumps(output_data, indent=2, default=str))
        log.info(f"Pipeline output written to {output_file}")

    log.info("=== SIN Pipeline complete ===")
    return {
        "tier1": len(tier1_records),
        "tier2": len(tier2_records),
        "tier3": len(omni_entries),
        "pillar_distribution": pillar_counts,
        "status": "complete",
    }


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SIN Pipeline — SacredSpace Intelligence Network")
    parser.add_argument("--sheet-id", help="Google Sheet ID for seed sources")
    parser.add_argument("--max-sources", type=int, default=20, help="Max records")
    parser.add_argument("--output-dir", default="/mnt/d/SacredSpace_OS/03_NEURAL/sin_output", help="Output directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )

    async def main():
        result = await run_sin_pipeline(
            sheet_id=args.sheet_id,
            max_sources=args.max_sources,
            output_dir=args.output_dir,
        )
        print(json.dumps(result, indent=2))

    asyncio.run(main())
