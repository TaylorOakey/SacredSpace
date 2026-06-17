#!/usr/bin/env python3
"""
S∆CR3D Neural Forest — CLI
Run the full harvest pipeline, check forest status, or trigger a pulse.

Usage:
  python -m app.cli harvest
  python -m app.cli status
  python -m app.cli audit
  python -m app.cli pulse
  python -m app.cli seed --title "My Idea" --url "https://example.com"
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


console = Console() if HAS_RICH else None


def _print(msg: str, style: str = ""):
    if HAS_RICH and console:
        console.print(msg, style=style)
    else:
        print(msg)


def _header():
    if HAS_RICH:
        console.print(Panel.fit(
            "[bold green]S∆CR3D Neural Forest[/bold green] [dim]— CLI v1.0[/dim]",
            border_style="green"
        ))
    else:
        print("=" * 60)
        print("  S∆CR3D Neural Forest — CLI v1.0")
        print("=" * 60)


# ── Async helpers ─────────────────────────────────────────────────────────────
async def _cmd_harvest():
    from .db import SessionLocal
    from .queue import TaskQueue
    from .services.scout import run_full_scout
    from .services.ingestor import Ingestor
    from .services.linker import Linker
    from .services.gardener import Gardener, compute_spi
    from .services.pulse import send_pulse

    _print("\n[bold cyan]Phase 1 — Scout[/bold cyan]" if HAS_RICH else "\n--- Scout ---")
    items = await run_full_scout()
    _print(f"  Found [bold]{len(items)}[/bold] items" if HAS_RICH else f"  Found {len(items)} items")

    async with SessionLocal() as db:
        _print("\n[bold cyan]Phase 2 — Ingest[/bold cyan]" if HAS_RICH else "\n--- Ingest ---")
        ing = Ingestor()
        node_ids = []
        for i, item in enumerate(items, 1):
            try:
                nid = await ing.ingest_item(db, item)
                node_ids.append(nid)
                _print(f"  [{i}/{len(items)}] ✓ {item.title[:60]}" if not HAS_RICH else
                       f"  [{i}/{len(items)}] [green]✓[/green] {item.title[:60]}")
            except Exception as e:
                _print(f"  [{i}/{len(items)}] ✗ {item.source_url[:60]}: {e}" if not HAS_RICH else
                       f"  [{i}/{len(items)}] [red]✗[/red] {item.source_url[:60]}: {e}")

        _print("\n[bold cyan]Phase 3 — Link[/bold cyan]" if HAS_RICH else "\n--- Link ---")
        linker = Linker()
        total_edges = 0
        for nid in node_ids:
            try:
                edges = await linker.link_recent(db, nid)
                total_edges += edges
            except Exception as e:
                _print(f"  Link failed for {nid}: {e}", style="red")
        _print(f"  Created [bold]{total_edges}[/bold] semantic edges" if HAS_RICH else
               f"  Created {total_edges} semantic edges")

        _print("\n[bold cyan]Phase 4 — Gardener[/bold cyan]" if HAS_RICH else "\n--- Gardener ---")
        g = Gardener()
        await g.apply_decay(db)
        pruned = await g.prune(db)
        resurrected = await g.resurrect_candidates(db)
        _print(f"  Archived: [yellow]{pruned}[/yellow] | Resurrected: [green]{resurrected}[/green]" if HAS_RICH else
               f"  Archived: {pruned} | Resurrected: {resurrected}")

        _print("\n[bold cyan]Phase 5 — SPI Report[/bold cyan]" if HAS_RICH else "\n--- SPI ---")
        spi = await compute_spi(db)
        _print_spi(spi)

        _print("\n[bold cyan]Phase 6 — Pulse[/bold cyan]" if HAS_RICH else "\n--- Pulse ---")
        result = await send_pulse(spi)
        _print(f"  {result}")


def _print_spi(spi_data: dict):
    spi = spi_data.get("spi", 0)
    stats = spi_data.get("stats", {})
    bar = "█" * int(spi / 5) + "░" * (20 - int(spi / 5))

    if HAS_RICH:
        console.print(f"\n  SPI: [bold green]{spi}/100[/bold green]  [{bar}]")
        t = Table(show_header=True, header_style="bold dim")
        t.add_column("Metric", style="cyan")
        t.add_column("Value", justify="right")
        for k, v in stats.items():
            t.add_row(k.replace("_", " ").title(), str(v))
        console.print(t)
    else:
        print(f"\n  SPI: {spi}/100  [{bar}]")
        for k, v in stats.items():
            print(f"    {k}: {v}")


async def _cmd_status():
    from .db import SessionLocal
    from .services.gardener import compute_spi
    async with SessionLocal() as db:
        spi = await compute_spi(db)
    _print_spi(spi)


async def _cmd_audit():
    from .db import SessionLocal
    from sqlalchemy import text
    async with SessionLocal() as db:
        # Orphan check
        res = await db.execute(text("""
            SELECT id, title FROM forest_nodes n
            WHERE NOT EXISTS (
                SELECT 1 FROM forest_edges e WHERE e.src_id=n.id OR e.dst_id=n.id
            )
            LIMIT 50
        """))
        orphans = res.fetchall()

        # Dead links
        res2 = await db.execute(text(
            "SELECT id, source_url FROM forest_nodes WHERE tags ? 'dead_link' LIMIT 20"
        ))
        dead = res2.fetchall()

        # Archived
        res3 = await db.execute(text(
            "SELECT COUNT(*) FROM forest_nodes WHERE tags ? 'archived'"
        ))
        archived = int(res3.scalar_one())

    _print(f"\n[bold]Audit Report[/bold]" if HAS_RICH else "\nAudit Report")
    _print(f"  Orphan nodes: [yellow]{len(orphans)}[/yellow]" if HAS_RICH else f"  Orphan nodes: {len(orphans)}")
    for nid, title in orphans[:10]:
        _print(f"    - {title[:60]} ({nid})", style="dim")

    _print(f"  Dead links: [red]{len(dead)}[/red]" if HAS_RICH else f"  Dead links: {len(dead)}")
    _print(f"  Archived nodes: [dim]{archived}[/dim]" if HAS_RICH else f"  Archived nodes: {archived}")


async def _cmd_pulse():
    from .db import SessionLocal
    from .services.gardener import compute_spi
    from .services.pulse import send_pulse
    async with SessionLocal() as db:
        spi = await compute_spi(db)
    result = await send_pulse(spi)
    _print(result)


async def _cmd_seed(title: str, url: str):
    import hashlib, json
    from .db import SessionLocal
    from sqlalchemy import text
    node_id = hashlib.blake2b(url.encode(), digest_size=12).hexdigest()
    async with SessionLocal() as db:
        await db.execute(text("""
            INSERT INTO forest_nodes (id, title, node_type, source_url, tags, updated_at)
            VALUES (:id, :title, 'manual', :url, '["manual","seed"]'::jsonb, NOW())
            ON CONFLICT (id) DO NOTHING
        """), {"id": node_id, "title": title, "url": url})
        await db.commit()
    _print(f"🌱 Seeded node [bold]{node_id}[/bold]: {title}" if HAS_RICH else
           f"Seeded node {node_id}: {title}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="S∆CR3D Neural Forest CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("harvest", help="Run full Scout → Ingest → Link → Gardener → Pulse pipeline")
    sub.add_parser("status", help="Show current SPI and forest statistics")
    sub.add_parser("audit", help="Run Librarian audit (orphans, dead links, archived)")
    sub.add_parser("pulse", help="Send a Discord pulse heartbeat immediately")
    seed_p = sub.add_parser("seed", help="Manually seed a node")
    seed_p.add_argument("--title", required=True)
    seed_p.add_argument("--url", required=True)

    args = parser.parse_args()
    _header()

    if args.command == "harvest":
        asyncio.run(_cmd_harvest())
    elif args.command == "status":
        asyncio.run(_cmd_status())
    elif args.command == "audit":
        asyncio.run(_cmd_audit())
    elif args.command == "pulse":
        asyncio.run(_cmd_pulse())
    elif args.command == "seed":
        asyncio.run(_cmd_seed(args.title, args.url))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
