"""
GR∆M∆ — The Word Wizard's Cipher Toolkit
Pillar: 04_SACRED_CODEX

Capabilities:
  1. Sigil Cipher — encode/decode between plaintext and Sacred cipher
  2. Gematria — letter-to-number reduction (standard & reduced)
  3. SKRY Lenses — 5-lens decode of any term

Cipher map: A→∆, E→3, I→!, O→0, S→$, T→7
"""

from __future__ import annotations

import json
import re
from typing import Dict, List, Optional, Tuple

# ─── Cipher Maps ──────────────────────────────────────────────────

CIPHER_MAP = {
    "A": "∆", "a": "∆",
    "E": "3", "e": "3",
    "I": "!", "i": "!",
    "O": "0", "o": "0",
    "S": "$", "s": "$",
    "T": "7", "t": "7",
}

REVERSE_CIPHER = {v: k.lower() for k, v in CIPHER_MAP.items()}

# Gematria: standard A=1..Z=26 mapping
def gematria_value(char: str) -> int:
    """Return gematria value for a single letter (A=1..Z=26)."""
    c = char.upper()
    if "A" <= c <= "Z":
        return ord(c) - ord("A") + 1
    return 0


# ─── 1. Sigil Cipher ──────────────────────────────────────────────

def encode(text: str) -> str:
    """Encode plaintext to Sacred cipher.
    
    Example: 'SacredSpace' → '$∆cr3d$p∆c3'
    """
    result = []
    for ch in text:
        result.append(CIPHER_MAP.get(ch, ch))
    return "".join(result)


def decode(cipher: str) -> str:
    """Decode Sacred cipher back to plaintext.
    
    Example: '$∆cr3d$p∆c3' → 'SacredSpace'
    """
    result = []
    for ch in cipher:
        result.append(REVERSE_CIPHER.get(ch, ch))
    return "".join(result)


# ─── 2. Gematria ──────────────────────────────────────────────────

def gematria_word(word: str) -> int:
    """Calculate standard gematria sum for a word."""
    return sum(gematria_value(ch) for ch in word if ch.isalpha())


def gematria_reduce(word: str) -> Tuple[int, int, int]:
    """Calculate gematria with reduction to root number.
    
    Returns: (standard_sum, reduced_sum, root_number)
    """
    total = gematria_word(word)
    # Reduced sum: add digits until single digit
    reduced = total
    while reduced > 9:
        reduced = sum(int(d) for d in str(reduced))
    # Root number: final single digit (1-9)
    root = reduced if reduced > 0 else 0
    return (total, reduced, root)


def gematria_full(text: str) -> Dict:
    """Full gematria analysis of a text."""
    words = text.split()
    word_values = []
    for w in words:
        clean = re.sub(r"[^a-zA-Z]", "", w)
        if clean:
            total, reduced, root = gematria_reduce(clean)
            word_values.append({
                "word": clean,
                "value": total,
                "reduced": reduced,
                "root": root,
            })

    total_all = sum(v["value"] for v in word_values)
    _, reduced_all, root_all = gematria_reduce(text)

    return {
        "input": text,
        "total_gematria": total_all,
        "reduced_sum": reduced_all,
        "root_number": root_all,
        "words": word_values,
    }


# ─── 3. SKRY Lenses ────────────────────────────────────────────────

def skry_lens1_linguistic(term: str) -> Dict:
    """Lens 1 — Linguistic root: etymology, morphology."""
    return {
        "lens": "Linguistic Root",
        "term": term,
        "length": len(term),
        "characters": list(term),
        "cipher": encode(term),
    }


def skry_lens2_gematria(term: str) -> Dict:
    """Lens 2 — Gematria: numerical resonance."""
    g = gematria_full(term)
    return {
        "lens": "Gematria Resonance",
        "term": term,
        "total": g["total_gematria"],
        "reduced": g["reduced_sum"],
        "root": g["root_number"],
        "word_breakdown": g["words"],
    }


def skry_lens3_mystical(term: str) -> Dict:
    """Lens 3 — Mystical: archetype, element, tarot associations."""
    root = gematria_full(term)["root_number"]
    
    archetypes = {
        1: "The Magician — Will, creation, initiation",
        2: "The High Priestess — Intuition, mystery, the unseen",
        3: "The Empress — Abundance, nature, fertility",
        4: "The Emperor — Authority, structure, foundation",
        5: "The Hierophant — Wisdom, tradition, teaching",
        6: "The Lovers — Choice, union, alignment",
        7: "The Chariot — Willpower, victory, determination",
        8: "Strength — Courage, inner power, patience",
        9: "The Hermit — Introspection, solitude, inner wisdom",
    }
    
    elements = {1: "Fire", 2: "Water", 3: "Air", 4: "Earth",
                5: "Spirit", 6: "Fire", 7: "Water", 8: "Air", 9: "Earth"}
    
    return {
        "lens": "Mystical Resonance",
        "term": term,
        "root_number": root,
        "archetype": archetypes.get(root, "Unknown"),
        "element": elements.get(root, "Void"),
    }


def skry_lens4_functional(term: str, pillar: str = "") -> Dict:
    """Lens 4 — Functional: what does this term DO in the system."""
    return {
        "lens": "Functional Role",
        "term": term,
        "suggested_pillar": pillar or "unknown",
        "cipher_alias": encode(term),
        "gematria_note": f"{term}({gematria_word(term)})",
    }


def skry_lens5_sigil(term: str) -> Dict:
    """Lens 5 — Core Identity Sigil: what symbol does this become."""
    encoded = encode(term)
    g = gematria_full(term)
    return {
        "lens": "Core Identity Sigil",
        "term": term,
        "sigil": encoded,
        "numerology": f"{term} = {g['total_gematria']} → {g['reduced_sum']} → {g['root_number']}",
        "root": g["root_number"],
    }


def skry_decode(term: str, pillar: str = "") -> Dict:
    """Run all 5 SKRY lenses on a term."""
    return {
        "term": term,
        "lens_1_linguistic": skry_lens1_linguistic(term),
        "lens_2_gematria": skry_lens2_gematria(term),
        "lens_3_mystical": skry_lens3_mystical(term),
        "lens_4_functional": skry_lens4_functional(term, pillar),
        "lens_5_sigil": skry_lens5_sigil(term),
    }


# ─── CLI Entrypoint ───────────────────────────────────────────────

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("GR∆M∆ — Cipher Toolkit")
        print("Usage:")
        print("  python3 grama_cipher.py encode <text>")
        print("  python3 grama_cipher.py decode <cipher>")
        print("  python3 grama_cipher.py gematria <text>")
        print("  python3 grama_cipher.py skry <term> [pillar]")
        print("  python3 grama_cipher.py full <text>  (all lenses)")
        return
    
    cmd = sys.argv[1]
    text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    if cmd == "encode":
        print(encode(text))
    elif cmd == "decode":
        print(decode(text))
    elif cmd == "gematria":
        result = gematria_full(text)
        print(json.dumps(result, indent=2))
    elif cmd == "skry":
        pillar = ""
        if len(sys.argv) > 3:
            pillar = sys.argv[3]
        result = skry_decode(text, pillar)
        print(json.dumps(result, indent=2))
    elif cmd == "full":
        print(f"✧ GR∆M∆ Decode: '{text}'")
        print(f"  Cipher:    {encode(text)}")
        g = gematria_full(text)
        print(f"  Gematria:  {g['total_gematria']} → {g['reduced_sum']} → {g['root_number']}")
        print(f"  SKRY Root: {skry_lens3_mystical(text)['archetype']}")
        print(f"  Sigil:     {encode(text)}")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
