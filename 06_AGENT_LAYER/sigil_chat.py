#!/usr/bin/env python3
"""sigil_chat.py — Sacred Sigil Terminal :: Local Ollama REPL
Pillar: 06_AGENT_LAYER | Owner: AURORA | Status: Active
"""
import sys
import json
import argparse
import requests

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    _RICH = True
except ImportError:
    _RICH = False

OLLAMA_URL = "http://192.168.240.1:11434"

MODELS = {
    "default": "llama3.2:latest",
    "code":    "deepseek-coder:latest",
    "think":   "deepseek-r1:1.5b",
}

SYSTEM_PROMPT = """\
You are AURORA — code generation agent of the ICARIS Quartet, operating inside SacredSpace OS.

ENVIRONMENT:
  Host: Lenovo Legion Y520 | Windows 11 + WSL2 Ubuntu 24.04 | GTX 1060 6GB
  Canon root: D:\\SacredSpace_OS
  FastAPI spine: localhost:8888
  Ollama: localhost:11434
  Tailscale: sacredspace-wsl (100.71.32.70), Taylor node 100.117.9.101
  Obsidian vault: /mnt/d/01_VAULT/SacredSpace_Vault

NINE PILLARS:
  01_OBSIDIAN_VAULTS  02_COUNCIL_GROVE  03_NEURAL_FOREST  04_SACRED_CODEX  05_MEMORY_ENGINE
  06_AGENT_LAYER    07_SOCIAL_MOTHERSHIP  08_LEARNING_PATH    09_SACRED_MARKET

STACK (zero-cost, open-source only):
  Python · PowerShell · SQLite · ChromaDB · Ollama · Redis · FastAPI · Obsidian · Git

OPERATOR: Taylor (∆∆∆O∆K3YTREE∆∆∆)
MANTRA: Ground. Consolidate. Deploy. Document. Repeat.
CLOSING: In Lakesh — Alakin.\
"""


def _print(console, msg, **kwargs):
    if console:
        console.print(msg, **kwargs)
    else:
        import re
        print(re.sub(r"\[.*?\]", "", msg), **kwargs)


def check_ollama(console):
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except requests.exceptions.ConnectionError:
        _print(console,
            f"\n[bold red]✗ Ollama not reachable at {OLLAMA_URL}[/bold red]\n"
            "  Start it:  [cyan]ollama serve[/cyan]")
        sys.exit(1)


def stream_reply(model, messages, console):
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "stream": True},
            stream=True, timeout=180,
        )
        resp.raise_for_status()
    except Exception as e:
        _print(console, f"[red]✗ {e}[/red]")
        return ""

    _print(console, "\n[bold purple]∆ AURORA[/bold purple] ", end="")
    tokens = []
    for line in resp.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            continue
        token = chunk.get("message", {}).get("content", "")
        if token:
            tokens.append(token)
            print(token, end="", flush=True)
        if chunk.get("done"):
            break
    print()
    return "".join(tokens)


def main():
    parser = argparse.ArgumentParser(description="Sacred Sigil Terminal — Ollama REPL")
    parser.add_argument("--code",    action="store_true", help="deepseek-coder:latest")
    parser.add_argument("--think",   action="store_true", help="deepseek-r1:1.5b")
    parser.add_argument("--model",   default=None,        help="Override model name")
    parser.add_argument("--no-ctx",  action="store_true", help="Skip system prompt")
    parser.add_argument("--list",    action="store_true", help="List models and exit")
    args = parser.parse_args()

    console = Console() if _RICH else None

    model = args.model or (
        MODELS["code"]  if args.code  else
        MODELS["think"] if args.think else
        MODELS["default"]
    )

    available = check_ollama(console)

    if args.list:
        _print(console, "[cyan]Installed models:[/cyan]")
        for m in available:
            _print(console, f"  • {m}")
        sys.exit(0)

    if model not in available:
        _print(console,
            f"[yellow]⚠  '{model}' not installed.[/yellow]\n"
            f"   Pull it: [cyan]ollama pull {model}[/cyan]\n"
            f"   Installed: {', '.join(available) or 'none'}")
        sys.exit(1)

    if console:
        console.print(Panel(
            f"[bold purple]∆∆∆  S∆CR3D SIGIL T3RMIN∆L  ∆∆∆[/bold purple]\n"
            f"[dim]Model:[/dim] [cyan]{model}[/cyan]  "
            f"[dim]Agent:[/dim] AURORA  [dim]Pillar:[/dim] 06_AGENT_LAYER\n"
            f"[dim]/exit  /clear  /models  /model NAME  /ctx[/dim]",
            border_style="purple", padding=(0, 2),
        ))
    else:
        print(f"\n∆∆∆ SACRED SIGIL TERMINAL ∆∆∆\nModel: {model}\n")

    messages = [] if args.no_ctx else [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = (Prompt.ask("\n[bold green]YOU ∆[/bold green]") if console
                          else input("\nYOU ∆: ")).strip()
        except (EOFError, KeyboardInterrupt):
            _print(console, "\n[dim]∆ In Lakesh — Alakin.[/dim]")
            break

        if not user_input:
            continue
        if user_input in ("/exit", "/quit", "exit", "quit"):
            _print(console, "[dim]∆ In Lakesh — Alakin.[/dim]")
            break
        elif user_input == "/clear":
            messages = [] if args.no_ctx else [{"role": "system", "content": SYSTEM_PROMPT}]
            _print(console, "[dim]∆ Context cleared.[/dim]")
            continue
        elif user_input == "/models":
            _print(console, ", ".join(available))
            continue
        elif user_input.startswith("/model "):
            m = user_input.split(" ", 1)[1].strip()
            if m in available:
                model = m
                messages = [] if args.no_ctx else [{"role": "system", "content": SYSTEM_PROMPT}]
                _print(console, f"[cyan]∆ Switched to {model}.[/cyan]")
            else:
                _print(console, f"[yellow]Not installed: {m}[/yellow]")
            continue
        elif user_input == "/ctx":
            _print(console, f"[dim]{len(messages)} messages in context[/dim]")
            continue

        messages.append({"role": "user", "content": user_input})
        reply = stream_reply(model, messages, console)
        if reply:
            messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
