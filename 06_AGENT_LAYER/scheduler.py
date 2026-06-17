"""
Scheduler Service — APScheduler cron jobs for the Forest lifecycle.
Runs inside the worker process. Schedules: scout, gardener, pulse.
"""
from __future__ import annotations

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..config import settings

log = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler | None = None


def _cron_from_string(cron_str: str) -> CronTrigger:
    """Parse '0 3 * * *' style cron string into APScheduler CronTrigger."""
    parts = cron_str.strip().split()
    if len(parts) != 5:
        raise ValueError(f"Invalid cron string: {cron_str!r}")
    minute, hour, day, month, day_of_week = parts
    return CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
        timezone=settings.scheduler_timezone,
        misfire_grace_time=3600,  # allow 1hr late start
        coalesce=True,
    )


async def _run_scout():
    from ..db import SessionLocal
    from ..queue import TaskQueue
    async with SessionLocal() as db:
        task_id = await TaskQueue.enqueue(db, "scout.run", {}, priority=10)
    log.info("Scheduler: enqueued scout.run → task #%d", task_id)


async def _run_gardener():
    from ..db import SessionLocal
    from ..queue import TaskQueue
    async with SessionLocal() as db:
        for task_type, priority in [
            ("gardener.decay", 200),
            ("gardener.prune", 210),
            ("gardener.resurrect", 220),
            ("gardener.deadlinks", 230),
        ]:
            await TaskQueue.enqueue(db, task_type, {}, priority=priority)
    log.info("Scheduler: enqueued full gardener pass")


async def _run_pulse():
    from ..db import SessionLocal
    from .gardener import Gardener, compute_spi
    from .pulse import send_pulse
    async with SessionLocal() as db:
        gardener = Gardener()
        spi_data = await compute_spi(db)
        # Count orphan nodes (no edges)
        from sqlalchemy import text
        res = await db.execute(text("""
            SELECT COUNT(*) FROM forest_nodes n
            WHERE NOT EXISTS (
                SELECT 1 FROM forest_edges e
                WHERE e.src_id = n.id OR e.dst_id = n.id
            )
        """))
        orphans = int(res.scalar_one())
    result = await send_pulse(spi_data, orphan_count=orphans)
    log.info("Scheduler pulse: %s", result)


def start_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        return

    _scheduler = AsyncIOScheduler(timezone=settings.scheduler_timezone)

    # Scout: daily at 3AM
    _scheduler.add_job(
        _run_scout,
        trigger=_cron_from_string("0 3 * * *"),
        id="scout_daily",
        replace_existing=True,
    )

    # Gardener: every Sunday at 4AM
    _scheduler.add_job(
        _run_gardener,
        trigger=_cron_from_string("0 4 * * 0"),
        id="gardener_weekly",
        replace_existing=True,
    )

    # Pulse: every Monday at 8AM
    _scheduler.add_job(
        _run_pulse,
        trigger=_cron_from_string("0 8 * * 1"),
        id="pulse_weekly",
        replace_existing=True,
    )

    _scheduler.start()
    log.info(
        "Scheduler started — scout: daily 03:00, gardener: Sun 04:00, pulse: Mon 08:00 (%s)",
        settings.scheduler_timezone,
    )


def stop_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        log.info("Scheduler stopped")
