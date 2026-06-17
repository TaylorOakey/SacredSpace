"""
copyq_bridge.py
CopyQ <-> SacredSpace OS bridge
Pillar: 02_COUNCIL_GROVE
Owner: AURORA
"""

import subprocess
import datetime
import os
from pathlib import Path

COPYQ_EXE = r"D:\SacredSpace_OS\02_COUNCIL_GROVE\tools\copyq\copyq.exe"
COPYQ_WSL = "/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/tools/copyq/copyq.exe"
SACRED_ROOT = Path("/mnt/d/SacredSpace_OS")

# Resolves correct binary path depending on execution environment
_copyq_bin = COPYQ_WSL if Path(COPYQ_WSL).exists() else COPYQ_EXE

PILLAR_TAB_MAP = {
    "01": "VAULT",
    "02": "COUNCIL",
    "03": "COUNCIL",
    "04": "CODEX",
    "05": "MEMORY",
    "06": "VAULT",
    "07": "MARKET",
    "08": "LEARNING",
    "09": "MARKET",
    "raw": "INBOX",
    "forge": "FORGE",
}

TAB_NAMES = ["FORGE", "CODEX", "VAULT", "COUNCIL", "MARKET", "LEARNING", "MEMORY", "INBOX"]


def _run(args: list) -> str:
    result = subprocess.run(
        [_copyq_bin] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def clipboard_read() -> str:
    return _run(["clipboard"])


def clipboard_write(text: str) -> None:
    _run(["copy", text])


def push_to_tab(tab: str, text: str) -> None:
    _run(["tab", tab, "add", text])


def route_by_pillar(pillar_key: str, text: str) -> str:
    tab = PILLAR_TAB_MAP.get(str(pillar_key), "INBOX")
    push_to_tab(tab, text)
    return tab


def sacredtag_stamp(text: str, pillar: str = "raw", topic: str = "", keywords: str = "") -> str:
    date = datetime.date.today().isoformat()
    tag = f"[SACREDTAG|DATE:{date}|PILLAR:{pillar}|TOPIC:{topic}|KEYWORDS:{keywords}|STATUS:RAW]"
    stamped = f"{tag}\n{text}"
    push_to_tab("INBOX", stamped)
    return stamped


def flush_tab_to_file(tab: str = "FORGE") -> Path:
    output_dir = SACRED_ROOT / "07_SOCIAL_MOTHERSHIP" / "FORGE_OUTPUT"
    output_dir.mkdir(parents=True, exist_ok=True)
    date = datetime.date.today().isoformat()
    out_file = output_dir / f"copyq_{tab.lower()}_flush_{date}.txt"

    count_raw = _run(["tab", tab, "count"])
    try:
        count = int(count_raw)
    except ValueError:
        count = 0

    lines = []
    for i in range(count):
        item = _run(["tab", tab, "read", str(i)])
        lines.append(f"--- ITEM {i} ---\n{item}\n")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[copyq_bridge] Flushed {count} items from {tab} → {out_file}")
    return out_file


def list_tabs() -> list:
    raw = _run(["tab"])
    return [t.strip() for t in raw.splitlines() if t.strip()]


def search_tabs(query: str) -> list:
    results = []
    for tab in list_tabs():
        count_raw = _run(["tab", tab, "count"])
        try:
            count = int(count_raw)
        except ValueError:
            continue
        for i in range(count):
            item = _run(["tab", tab, "read", str(i)])
            if query.lower() in item.lower():
                results.append({"tab": tab, "index": i, "text": item})
    return results


if __name__ == "__main__":
    print("CopyQ version:", _run(["--version"]))
    print("Tabs:", list_tabs())
    print("Clipboard:", clipboard_read()[:80])
