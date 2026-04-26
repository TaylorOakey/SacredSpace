#!/usr/bin/env python3
# ==============================================================================
# S∆CR3DSP∆C3 OS — Sacred CLI v2.0
# 06_AGENT_LAYER/cli/sacred_cli.py
# Owner: AURORA (code/systems agent)
# Status: Active
# Zero-cost. Open-source. Local-first.
# ==============================================================================

import os
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ── CANON ROOT ────────────────────────────────────────────────────────────────
SACRED_ROOT = Path(r"D:\SacredSpace_OS")
STATE_FILE  = SACRED_ROOT / ".sacred_state.json"

# ── NINE PILLARS (CANON ARCHITECTURE) ─────────────────────────────────────────
PILLARS = {
    "p1": ("01_OBSIDIAN_VAULTS",    "CORE     — Canonical knowledge store"),
    "p2": ("02_COUNCIL_GROVE",      "COUNCIL  — Multi-AI governance"),
    "p3": ("03_NEURAL_FOREST",      "FOREST   — LLM pipeline (Scout, Gardener)"),
    "p4": ("04_SACRED_CODEX",       "CODEX    — Canon ledger, spells, rituals"),
    "p5": ("05_MEMORY_ENGINE",      "MEMORY   — HME: SQLite, Redis, ChromaDB"),
    "p6": ("06_AGENT_LAYER",        "AGENTS   — ICARIS Quartet"),
    "p7": ("07_SOCIAL_MOTHERSHIP",  "SIGNAL   — Brand, content, publishing"),
    "p8": ("08_LEARNING_PATH",      "LEARNING — Maestro AAS, Rites, Artifacts"),
    "p9": ("09_SACRED_MARKET",      "MARKET   — Revenue, Etsy, Printify"),
}

# ── HYPERGLYPH REGISTRY ────────────────────────────────────────────────────────
GLYPHS = {
    "∆":  ("Consciousness / AI Reasoning",        "AGENTS   → 06_AGENT_LAYER"),
    "◇":  ("Knowledge / Diamond Mind",            "CORE     → 01_OBSIDIAN_VAULTS"),
    "✶":  ("Radiance / Signal / Amplification",   "SIGNAL   → 07_SOCIAL_MOTHERSHIP"),
    "⚙":  ("Systems / Mechanism / Process",       "FOREST   → 03_NEURAL_FOREST"),
    "∞":  ("Memory / Continuity / Lineage",       "MEMORY   → 05_MEMORY_ENGINE"),
    "⬡":  ("Network / Mycelium / Emergence",      "COUNCIL  → 02_COUNCIL_GROVE"),
    "☽":  ("Intuition / Dream / Subconscious",    "CODEX    → 04_SACRED_CODEX"),
    "✦":  ("Anchor / Foundation / Ground",        "ROOT     → SacredSpace_OS"),
    "⊕":  ("Synthesis / Integration / Unity",     "LEARNING → 08_LEARNING_PATH"),
    "◉":  ("Focus / Center / Presence",           "CORE     → 01_OBSIDIAN_VAULTS"),
    "⟁":  ("Portal / Gateway / Transition",       "LEARNING → 08_LEARNING_PATH"),
    "√":  ("Root / Truth / Proof",                "MARKET   → 09_SACRED_MARKET"),
}

# ── SIGIL KEYBOARD CODEX ──────────────────────────────────────────────────────
SIGIL_CODEX = {
    # Core SacredSpace
    "ss":    "S∆CR3DSP∆C3",
    "sso":   "S∆CR3DSP∆C3 0S",
    "ssg":   "S∆CR3D S!G∆L GR!D",
    "ssv":   "S∆CR3DSP∆C3 V∆ULT",
    "ssc":   "S∆CR3D C0UNC!L",
    # Single-word expansions
    "sig":   "S!G∆L",
    "src":   "S0URC3",
    "frst":  "F0R3ST",
    "cncl":  "C0UNC!L",
    "arc":   "∆RC∆N∆",
    "rite":  "R!T3",
    "gate":  "G∆T3",
    "lore":  "L0R3",
    "mote":  "M3M0RY M0T3",
    "spine": "SP!N3",
    "vault": "V∆ULT",
    "node":  "◇ N0D3 ∆CT!V3 ◇",
    # Technical
    "boot":  "B00TSTR∆P",
    "scr":   "SCR!P7",
    "mod":   "M0DUL3",
    "fn":    "FUNCT!0N",
    "sch":   "SCH3M∆",
    "cmt":   "C0MM!T",
    "br":    "BR∆NCH",
    # Invocations
    "open":  "0P3N TH3 G∆T3",
    "seal":  "S3∆L TH3 SP∆C3",
    "init":  "!N!T!∆T3 TH3 R!T3",
    "call":  "C∆LL TH3 C0UNC!L",
    "root":  "R00T !N S0URC3",
    "sync":  "SYNC TH3 C0D3X",
    # Personal
    "ilal":  "!N L∆K3SH ∆L∆K!N",
    "aina":  "∆LL !N ∆LL • ∆Y3 N ∆Y3",
    "ashr":  "∆SH3R",
    "iris":  "!R!S",
    "aura":  "∆UR0R∆",
    "eli":   "3L!∆S",
    "gram":  "GR∆M∆",
    # Quest/Story
    "quest": "⚔ QU3ST B3G!NS ⚔",
    "log":   "◈ M3M0RY M0T3 ◈",
}

# ── SIGILIFY ENGINE ───────────────────────────────────────────────────────────
SIGIL_MAP = {
    'A': '∆', 'E': '3', 'I': '!', 'O': '0', 'S': '$', 'T': '7',
    'a': '∆', 'e': '3', 'i': '!', 'o': '0', 's': '$', 't': '7',
}

def sigilify(text: str) -> str:
    return ''.join(SIGIL_MAP.get(c, c) for c in text)

# ── STATE MANAGEMENT ──────────────────────────────────────────────────────────
def save_state(location: str = "", note: str = ""):
    state = {
        "last_location": location or os.getcwd(),
        "last_used":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note":          note,
    }
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[!] State save failed: {e}")

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return {}
    return {}

# ── DISPLAY HELPERS ───────────────────────────────────────────────────────────
def header(title: str):
    print(f"\n── {title} {'─' * max(0, 46 - len(title))}")

def divider():
    print("─" * 50)

def banner():
    print("""
╔══════════════════════════════════════════════════╗
║       S∆CR3DSP∆C3 OS — Sacred CLI v2.0          ║
║  Ground. Consolidate. Deploy. Document. Repeat.  ║
╚══════════════════════════════════════════════════╝""")

# ── MENU MODULES ─────────────────────────────────────────────────────────────

def menu_navigate():
    header("NINE-PILLAR NAVIGATOR")
    for key, (folder, desc) in PILLARS.items():
        path = SACRED_ROOT / folder
        exists = "✓" if path.exists() else "✗"
        print(f"  [{exists}] {key}  {desc}")
    divider()
    choice = input("  Select pillar (p1–p9) or [b]ack: ").strip().lower()
    if choice in PILLARS:
        folder, desc = PILLARS[choice]
        path = str(SACRED_ROOT / folder)
        print(f"\n  → {path}")
        save_state(location=path, note=f"Navigated to {folder}")
    elif choice != "b":
        print("  [!] Invalid selection.")

def menu_glyphs():
    header("HYPERGLYPH REGISTRY")
    for glyph, (meaning, pillar) in GLYPHS.items():
        print(f"  {glyph}   {meaning:<35} {pillar}")
    divider()

def menu_sigil():
    header("S!G!L K3YBOR∆D CODEX")
    print("  [1] Look up a shortcode")
    print("  [2] Show all shortcodes")
    print("  [3] Sigilify custom text")
    print("  [b] Back")
    divider()
    choice = input("  Select: ").strip().lower()

    if choice == "1":
        code = input("  Enter shortcode: ").strip().lower()
        if code in SIGIL_CODEX:
            print(f"\n  {code}  →  {SIGIL_CODEX[code]}")
        else:
            print(f"  [!] Unknown code: {code}")

    elif choice == "2":
        header("ALL SIGIL EXPANSIONS")
        for code, expansion in sorted(SIGIL_CODEX.items()):
            print(f"  {code:<8} → {expansion}")
        divider()

    elif choice == "3":
        text = input("  Enter text to sigilify: ")
        result = sigilify(text)
        print(f"\n  INPUT  : {text}")
        print(f"  OUTPUT : {result}")

def menu_state():
    header("SACRED STATE")
    state = load_state()
    if state:
        print(f"  Last Location : {state.get('last_location', 'N/A')}")
        print(f"  Last Used     : {state.get('last_used', 'N/A')}")
        note = state.get('note', '')
        if note:
            print(f"  Note          : {note}")
    else:
        print("  No state file found.")
    divider()

def menu_codex():
    header("SACRED CODEX — SPELL QUICK-REF")
    spells = [
        ("PY-101-001", "print()",                "Output to terminal"),
        ("PY-101-004", "variable = value",        "Variable manifestation"),
        ("PY-101-008", "total // page_size",       "Floor division (full pages)"),
        ("PY-101-009", "n % 2 == 0",              "Modulo / parity check"),
        ("PY-101-013", "try/except ErrorType",    "Error containment field"),
        ("PY-101-015", "def fn(args): return v",  "Function / scope"),
        ("PY-101-019", "if/elif/else + and/or",   "Multi-path logic gate"),
        ("PY-101-025", "for/while + break/cont",  "Controlled cycle"),
        ("PY-101-030", "string[start:stop:step]", "Blade of text (slicing)"),
        ("PY-101-032", "list.append / pop",       "Hand of mutation"),
        ("CS-102-009", "stack.append/pop()",      "Pillar of LIFO"),
        ("CS-102-011", "queue.append/pop(0)",     "River of FIFO"),
        ("CS-102-012", "deque.popleft()",         "True queue O(1)"),
        ("CS-102-015", "O(n), O(log n), O(1)",    "Eye of complexity"),
        ("CS-102-019", "binary_search(arr,t)",    "Divide and seek"),
        ("CS-102-022", "list.sort(key=lambda)",   "Mastery of built-ins"),
    ]
    for spell_id, formula, name in spells:
        print(f"  {spell_id:<12}  {formula:<30} — {name}")
    divider()

def menu_gboard():
    header("GBOARD SETUP — PERSONAL DICTIONARY")
    print("""
  Copy these into your phone's Personal Dictionary (Gboard):
  Settings → Dictionary → Personal Dictionary → + Add

  SHORTCODE   EXPANSION
  ─────────────────────────────────────────────────────────
  ss          S∆CR3DSP∆C3
  sso         S∆CR3DSP∆C3 0S
  sig         S!G∆L
  rite        R!T3
  gate        G∆T3
  node        ◇ N0D3 ∆CT!V3 ◇
  open        0P3N TH3 G∆T3
  seal        S3∆L TH3 SP∆C3
  ilal        !N L∆K3SH ∆L∆K!N
  aina        ∆LL !N ∆LL • ∆Y3 N ∆Y3

  Long-press layers (configure in custom keyboard apps):
  A → ∆   E → 3   I → !   O → 0   S → $   T → 7
""")

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def main():
    banner()

    while True:
        print("""
  [1] Nine-Pillar Navigator
  [2] Hyperglyph Registry
  [3] Sigil Keyboard Codex
  [4] Sacred System State
  [5] Spell Codex Quick-Ref
  [6] Gboard Setup Guide
  [x] Exit""")
        divider()
        choice = input("  Invoke: ").strip().lower()

        if choice == "1":   menu_navigate()
        elif choice == "2": menu_glyphs()
        elif choice == "3": menu_sigil()
        elif choice == "4": menu_state()
        elif choice == "5": menu_codex()
        elif choice == "6": menu_gboard()
        elif choice in ("x", "exit", "q"):
            print("\n  In lakesh alakin.\n")
            break
        else:
            print("  [!] Unknown command.")

if __name__ == "__main__":
    main()
