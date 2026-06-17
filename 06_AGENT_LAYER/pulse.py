"""
Pulse Service — sends a Forest health heartbeat to Discord with an embedded
matplotlib chart PNG. Falls back to text-only if matplotlib is unavailable.
"""
from __future__ import annotations

import io
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import httpx

from ..config import settings

log = logging.getLogger(__name__)


def _build_chart_png(spi_data: Dict[str, Any]) -> Optional[bytes]:
    """Generate a bar chart of SPI components as PNG bytes."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend
        import matplotlib.pyplot as plt

        components = spi_data.get("components", {})
        labels = [
            "Node\nScore", "Edge\nDensity", "Health", "Resurrection", "Recency"
        ]
        values = [
            components.get("node_score", 0),
            components.get("density_score", 0),
            components.get("health_score", 0),
            components.get("resurrection_score", 0),
            components.get("recency_score", 0),
        ]
        max_vals = [15, 25, 25, 20, 15]
        colors = ["#00ff6a", "#00c4a7", "#7fff00", "#22d3ee", "#a78bfa"]

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor("#0c150e")
        ax.set_facecolor("#0c150e")

        bars = ax.bar(labels, values, color=colors, edgecolor="#1c3022", linewidth=0.8)
        ax.bar(labels, max_vals, color="#1c3022", zorder=0)

        # Value labels on bars
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{val:.1f}",
                ha="center", va="bottom",
                color="#c8dfc9", fontsize=9
            )

        spi = spi_data.get("spi", 0)
        ax.set_title(
            f"S∆CR3D Neural Forest — SPI: {spi}/100",
            color="#00ff6a", fontsize=13, pad=12
        )
        ax.set_ylim(0, 28)
        ax.tick_params(colors="#3a5440")
        ax.spines[:].set_color("#1c3022")
        ax.yaxis.label.set_color("#3a5440")
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_color("#607a63")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=120, facecolor="#0c150e")
        plt.close(fig)
        buf.seek(0)
        return buf.read()

    except ImportError:
        log.warning("matplotlib not installed — pulse will be text-only")
        return None
    except Exception as e:
        log.warning("Chart generation failed: %s", e)
        return None


def _build_embed(spi_data: Dict[str, Any], orphans: int, has_chart: bool) -> Dict:
    spi = spi_data.get("spi", 0)
    stats = spi_data.get("stats", {})
    components = spi_data.get("components", {})

    spi_bar = "█" * int(spi / 10) + "░" * (10 - int(spi / 10))
    color = 0x00FF6A if spi >= 70 else (0xF59E0B if spi >= 40 else 0xFF5F57)

    return {
        "title": "🌲 S∆CR3D Neural Forest — Heartbeat",
        "color": color,
        "description": f"`{spi_bar}` **{spi}/100**",
        "fields": [
            {
                "name": "📊 Nodes",
                "value": (
                    f"Total: **{stats.get('total_nodes', 0)}**\n"
                    f"Active: **{stats.get('active_nodes', 0)}**\n"
                    f"Recent (30d): **{stats.get('recent_nodes', 0)}**"
                ),
                "inline": True,
            },
            {
                "name": "🔗 Graph",
                "value": (
                    f"Edges: **{stats.get('total_edges', 0)}**\n"
                    f"Avg RS: **{stats.get('avg_resurrection_score', 0):.3f}**\n"
                    f"Orphans: **{orphans}**"
                ),
                "inline": True,
            },
            {
                "name": "⚡ SPI Components",
                "value": (
                    f"Nodes: `{components.get('node_score', 0):.1f}/15`  "
                    f"Density: `{components.get('density_score', 0):.1f}/25`\n"
                    f"Health: `{components.get('health_score', 0):.1f}/25`  "
                    f"RS: `{components.get('resurrection_score', 0):.1f}/20`\n"
                    f"Recency: `{components.get('recency_score', 0):.1f}/15`"
                ),
                "inline": False,
            },
        ],
        "image": {"url": "attachment://forest_spi.png"} if has_chart else None,
        "footer": {
            "text": f"S∆CR3D OS • {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        },
        "thumbnail": {"url": "https://i.imgur.com/PLACEHOLDER.png"},
    }


async def send_pulse(spi_data: Dict[str, Any], orphan_count: int = 0) -> str:
    """Send heartbeat to Discord webhook with optional chart attachment."""
    if not settings.discord_webhook:
        return "⚠️  DISCORD_WEBHOOK not set — pulse skipped"
    if not settings.pulse_enabled:
        return "⚠️  Pulse disabled"

    chart_bytes = _build_chart_png(spi_data)
    embed = _build_embed(spi_data, orphan_count, has_chart=chart_bytes is not None)

    # Remove None fields from embed
    embed = {k: v for k, v in embed.items() if v is not None}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            if chart_bytes:
                # Multipart: JSON embed + PNG file
                r = await client.post(
                    settings.discord_webhook,
                    data={"payload_json": json.dumps({"embeds": [embed]})},
                    files={"file": ("forest_spi.png", chart_bytes, "image/png")},
                )
            else:
                r = await client.post(
                    settings.discord_webhook,
                    json={"embeds": [embed]},
                )
        r.raise_for_status()
        return f"✅ Pulse sent (status {r.status_code})"
    except Exception as e:
        log.error("Pulse failed: %s", e)
        return f"❌ Pulse failed: {e}"
