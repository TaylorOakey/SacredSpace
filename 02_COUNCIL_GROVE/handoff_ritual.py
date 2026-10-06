#!/usr/bin/env python3
"""handoff_ritual.py — CLAUDE.md `generate-handoff-capsule` entry point.

Thin wrapper over bridge/bridge.py so the legacy flags keep working:
  handoff_ritual.py --agent opencode --task ".." --done ".." --next ".."
Writes 02_COUNCIL_GROVE/LATEST_HANDOFF.md (git state + open bridge messages).
"""
import argparse, subprocess, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--agent", default="opencode")
for k in ("task", "done", "next"):
    ap.add_argument(f"--{k}", default="")
a = ap.parse_args()
bridge = Path(__file__).resolve().parent / "bridge" / "bridge.py"
sys.exit(subprocess.call([sys.executable, str(bridge), "handoff", "--to", a.agent,
                          "--task", a.task, "--done", a.done, "--next", a.next]))
