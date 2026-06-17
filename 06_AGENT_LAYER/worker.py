"""
Worker — claims and executes tasks from the durable task queue.
Also starts the APScheduler cron loop for autonomous scheduled jobs.
"""
from __future__ import annotations

import asyncio
import logging
import os
import socket

from pythonjsonlogger import jsonlogger
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .db import SessionLocal
from .queue import TaskQueue
from .services.scout import run_full_scout
from .services.ingestor import Ingestor
from .services.linker import Linker
from .services.gardener import Gardener, compute_spi
from .services.pulse import send_pulse
from .services.scheduler import start_scheduler, stop_scheduler


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    ))
    logger.handlers = [handler]


async def handle_task(db: AsyncSession, task: dict):
    ttype = task["task_type"]
    payload = task.get("payload") or {}

    if ttype == "scout.run":
        items = await run_full_scout()
        for item in items:
            await TaskQueue.enqueue(
                db, "ingest.item",
                {
                    "source": item.source,
                    "source_url": item.source_url,
                    "title": item.title,
                    "body": item.body or "",
                    "meta": item.meta or {},
                },
                priority=50,
            )
        logging.info({"event": "scout_complete", "queued": len(items)})

    elif ttype == "ingest.item":
        from .services.scout import DiscoveredItem
        item = DiscoveredItem(
            source=payload["source"],
            source_url=payload["source_url"],
            title=payload.get("title") or payload["source_url"],
            body=payload.get("body") or "",
            meta=payload.get("meta") or {},
        )
        ing = Ingestor()
        node_id = await ing.ingest_item(db, item)
        if node_id:
            await TaskQueue.enqueue(db, "link.node", {"node_id": node_id}, priority=80)

    elif ttype == "link.node":
        linker = Linker()
        count = await linker.link_recent(db, payload["node_id"])
        logging.info({"event": "linked", "node": payload["node_id"], "edges": count})

    elif ttype == "gardener.decay":
        g = Gardener()
        n = await g.apply_decay(db)
        logging.info({"event": "decay_done", "nodes": n})

    elif ttype == "gardener.prune":
        g = Gardener()
        n = await g.prune(db)
        logging.info({"event": "prune_done", "archived": n})

    elif ttype == "gardener.resurrect":
        g = Gardener()
        n = await g.resurrect_candidates(db)
        logging.info({"event": "resurrect_done", "candidates": n})

    elif ttype == "gardener.deadlinks":
        g = Gardener()
        result = await g.check_dead_links(db)
        logging.info({"event": "deadlink_done", **result})

    elif ttype == "pulse.send":
        spi_data = await compute_spi(db)
        from sqlalchemy import text
        res = await db.execute(text("""
            SELECT COUNT(*) FROM forest_nodes n
            WHERE NOT EXISTS (
                SELECT 1 FROM forest_edges e WHERE e.src_id=n.id OR e.dst_id=n.id
            )
        """))
        orphans = int(res.scalar_one())
        msg = await send_pulse(spi_data, orphan_count=orphans)
        logging.info({"event": "pulse_sent", "result": msg})

    else:
        raise RuntimeError(f"Unknown task_type: {ttype!r}")


async def worker_loop():
    setup_logging()
    worker_id = f"{socket.gethostname()}:{os.getpid()}"
    logging.info({"event": "worker_start", "worker_id": worker_id})

    # Start the scheduled cron jobs
    start_scheduler()

    try:
        while True:
            async with SessionLocal() as db:
                task = await TaskQueue.claim_next(db, worker_id)
                if not task:
                    await asyncio.sleep(1.0)
                    continue

                try:
                    await handle_task(db, task)
                    await TaskQueue.mark_done(db, int(task["id"]))
                    logging.info({
                        "event": "task_done",
                        "id": int(task["id"]),
                        "type": task["task_type"],
                    })
                except Exception as e:
                    await TaskQueue.mark_failed(db, int(task["id"]), str(e))
                    logging.exception({
                        "event": "task_failed",
                        "id": int(task["id"]),
                        "type": task["task_type"],
                        "err": str(e),
                    })
    finally:
        stop_scheduler()


if __name__ == "__main__":
    asyncio.run(worker_loop())
