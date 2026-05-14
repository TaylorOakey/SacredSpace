#!/usr/bin/env python3
"""sacred_diagnostics.py — SacredSpace OS Stack Diagnostics
Checks all components and reports status.
"""
import os
import sys
import json
import subprocess
import requests
from datetime import datetime

# pydantic-settings stat()s '.env' relative to CWD; fails on unmounted WSL paths
os.chdir(os.path.expanduser("~"))

OLLAMA_URL  = "http://192.168.240.1:11434"
SPINE_URL   = "http://localhost:8888"
REQUIRED_MODELS = {"llama3.1:8b", "qwen2.5-coder:7b", "nomic-embed-text", "phi3.5"}

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    def out(label, status, detail=""):
        color = "green" if "✓" in status else ("yellow" if "⚠" in status else "red")
        console.print(f"  [{color}]{status}[/{color}]  {label}" + (f"  [dim]{detail}[/dim]" if detail else ""))
except ImportError:
    console = None
    def out(label, status, detail=""):
        print(f"  {status}  {label}" + (f"  {detail}" if detail else ""))

def section(title):
    if console:
        console.rule(f"[bold purple]{title}[/bold purple]")
    else:
        print(f"\n{'='*40}\n{title}\n{'='*40}")

results = {}

# ∆ 1 — Ollama
section("∆ OLLAMA")
try:
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    r.raise_for_status()
    installed = {m["name"] for m in r.json().get("models", [])}
    out("Ollama reachable", "✓", OLLAMA_URL)
    results["ollama"] = True

    for model in sorted(REQUIRED_MODELS):
        if model in installed:
            out(model, "✓ installed")
        else:
            out(model, "✗ MISSING", f"run: ollama pull {model}")
    results["models"] = {m: (m in installed) for m in REQUIRED_MODELS}
except requests.exceptions.ConnectionError:
    out("Ollama", "✗ NOT REACHABLE", f"{OLLAMA_URL} — start: ollama serve")
    results["ollama"] = False
    results["models"] = {}

# ∆ 2 — Sacred Spine
section("∆ SACRED SPINE v2")
try:
    r = requests.get(f"{SPINE_URL}/health", timeout=5)
    data = r.json()
    out("Spine reachable", "✓", SPINE_URL)
    out("Grove loaded", "✓" if data.get("grove") else "⚠ agent_core missing")
    results["spine"] = True
except Exception:
    out("Spine", "⚠ not running", f"start: bash sacred_boot.sh")
    results["spine"] = False

# ∆ 3 — Python packages
section("∆ PYTHON PACKAGES")
packages = ["fastapi", "uvicorn", "chromadb", "rich", "requests", "pydantic"]
for pkg in packages:
    try:
        __import__(pkg)
        out(pkg, "✓")
        results.setdefault("packages", {})[pkg] = True
    except ImportError:
        out(pkg, "✗ MISSING", f"pip install {pkg}")
        results.setdefault("packages", {})[pkg] = False

# ∆ 4 — Tailscale
section("∆ TAILSCALE")
try:
    ts = subprocess.run(["tailscale", "status", "--json"],
                        capture_output=True, text=True, timeout=5)
    data = json.loads(ts.stdout)
    state = data.get("BackendState", "unknown")
    ip = next((v.get("TailscaleIPs", [""])[0]
               for v in data.get("Peer", {}).values()
               if "sacredspace" in v.get("HostName", "").lower()), "")
    out(f"Tailscale {state}", "✓" if state == "Running" else "⚠", ip or "")
    results["tailscale"] = state == "Running"
except Exception:
    out("Tailscale", "⚠ not found or not running")
    results["tailscale"] = False

# ∆ 5 — Summary
section("∆ SUMMARY")
total = sum([
    results.get("ollama", False),
    results.get("spine", False),
    all(results.get("models", {}).values()),
    all(results.get("packages", {}).values()),
])
out(f"{total}/4 subsystems nominal", "✓" if total == 4 else "⚠",
    f"as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if console:
    console.print("\n[dim]∆ In Lakesh — Alakin.[/dim]\n")
else:
    print("\n∆ In Lakesh — Alakin.\n")

sys.exit(0 if total == 4 else 1)
