"""
sacredspace — SacredSpace OS Cipher Core (GR∆M∆)

The functional core both GR∆M∆ canon tracks depend on. Compares every
known SacredSpace cipher system for a given term and reports agreement.

Systems compared:
  1. English ordinal gematria   — A:1..Z:26  (grama_persona.gematria)
  2. GR∆M∆ cipher substitution  — A:∆ E:3 O:Ø I:1 S:$  (grama_persona.cipher)
  3. Sacred Sigil encoding      — GLYPH_MAP + WORD_OVERRIDES  (sigil_layer)
  4. Sacred Alphabet Map (Hebrew / Kabbalistic — Sefer Yetzirah + Golden Dawn)
     — position / hecrechi / gadol / katan per letter
  5. Abazith phoneme resonance  — SKRY Lens 6 sonic texture (abazith_map)

Reduction: every numeric system is reduced to a single digit (digital root)
so systems can be compared for alignment.

Author: VALEN — Council Seat 4: Decision Authority
Pillar: 04_SACRED_CODEX (functional core — 06_AGENT_LAYER delivery)
Canon: 2026-08-01 — reconciled from GR∆M∆_CANON.md tracks 1+2
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

__version__ = "1.0.0-GRAMA"

# ---------------------------------------------------------------------------
# 1. ENGLISH ORDINAL GEMATRIA  (matches grama_persona.SACRED_ALPHABET_MAP)
# ---------------------------------------------------------------------------

SACRED_ALPHABET_MAP: Dict[str, int] = {
    chr(c): c - 64 for c in range(ord("A"), ord("Z") + 1)
}


def gematria(word: str) -> int:
    """English ordinal gematria — sum of letter values (A:1..Z:26)."""
    return sum(SACRED_ALPHABET_MAP.get(c.upper(), 0) for c in word if c.isalpha())


# ---------------------------------------------------------------------------
# 2. GR∆M∆ CIPHER SUBSTITUTION  (matches grama_persona.CIPHER_SUBSTITUTIONS)
# ---------------------------------------------------------------------------

CIPHER_SUBSTITUTIONS: Dict[str, str] = {
    "A": "∆", "E": "3", "O": "Ø", "I": "1", "S": "$",
}


def cipher(text: str) -> str:
    """Apply GR∆M∆ cipher substitution to a string."""
    return "".join(CIPHER_SUBSTITUTIONS.get(c.upper(), c) for c in text)


# ---------------------------------------------------------------------------
# 3. SACRED SIGIL ENCODING  (matches sigil_layer GLYPH_MAP + WORD_OVERRIDES)
# ---------------------------------------------------------------------------

GLYPH_MAP: Dict[str, str] = {
    "A": "∆", "E": "3", "I": "!", "O": "0", "S": "S", "T": "7", "Y": "Y", "H": "H",
}

WORD_OVERRIDES: Dict[str, str] = {
    "SACRED": "S∆CR3D", "SIGNAL": "S!GN∆L", "KEYBOARD": "K3YBOR∆D",
    "SYSTEM": "SYST3M", "SOURCE": "S0URC3", "SPIRIT": "SP!R!T",
    "FOREST": "F0R3ST", "CODEX": "C0D3X", "ARCANA": "∆RC∆N∆",
    "COUNCIL": "C0UNC!L", "VAULT": "V∆ULT", "RITE": "R!T3",
    "GATE": "G∆T3", "LORE": "L0R3", "SPINE": "SP!N3", "MEMORY": "M3M0RY",
    "MOTE": "M0T3", "FUNCTION": "FUNCT!0N", "MODULE": "M0DUL3",
    "SCRIPT": "SCR!P7", "BOOTSTRAP": "B00TSTR∆P", "SCHEMA": "SCH3M∆",
    "COMMIT": "C0MM!T", "BRANCH": "BR∆NCH", "SACREDSPACE": "S∆CR3DSP@C3",
}


def sigil_encode_word(word: str) -> str:
    """Sacred Sigil encode a single word (override first, then glyph map)."""
    upper = word.upper()
    if upper in WORD_OVERRIDES:
        return WORD_OVERRIDES[upper]
    return "".join(GLYPH_MAP.get(c, c) for c in upper)


def sigil_encode(text: str) -> str:
    """Sacred Sigil encode a phrase (word-wise)."""
    return " ".join(sigil_encode_word(w) for w in text.split())


def sigil_decode_partial(encoded: str) -> str:
    """Best-effort reverse decode. Lossy by design (matches sigil_layer)."""
    result = encoded
    for plain, sig in sorted(WORD_OVERRIDES.items(), key=lambda kv: -len(kv[1])):
        result = result.replace(sig, plain)
    rev_glyphs = {v: k for k, v in GLYPH_MAP.items() if k != v}
    return "".join(rev_glyphs.get(c, c) for c in result)


# ---------------------------------------------------------------------------
# 4. SACRED ALPHABET MAP (HEBREW / KABBALISTIC)
# ---------------------------------------------------------------------------

_ALPHABET_CACHE: Optional[Dict[str, Dict[str, Any]]] = None
_ALPHABET_PATH_CANDIDATES = [
    "/mnt/d/SacredSpace_OS/04_SACRED_CODEX/sacred_alphabet_map.json",
    "/mnt/c/04_SACRED_CODEX/sacred_alphabet_map.json",
]


def _load_alphabet_map() -> Dict[str, Dict[str, Any]]:
    """Load sacred_alphabet_map.json once; key by romanized letter (lower)."""
    global _ALPHABET_CACHE
    if _ALPHABET_CACHE is not None:
        return _ALPHABET_CACHE
    data: Dict[str, Any] = {}
    for path in _ALPHABET_PATH_CANDIDATES:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            break
    _ALPHABET_CACHE = {}
    for entry in data.get("alphabet", []):
        roman = entry.get("romanized", "").lower()
        if roman:
            _ALPHABET_CACHE[roman] = entry
    return _ALPHABET_CACHE


def hebrew_value(term: str, mode: str = "position") -> Dict[str, Any]:
    """Sacred Alphabet Map values for a term.

    mode: 'position' | 'hecrechi' | 'gadol' | 'katan'
    Returns {per_letter: [...], total, romanized_letters: [...]}

    English letters are transliterated to Hebrew letter names via the
    best-effort TRANSLITERATION map (symbolic resonance, not deterministic
    truth — per the map's own meta).
    """
    alphabet = _load_alphabet_map()
    per_letter: List[Dict[str, Any]] = []
    total = 0
    roman_hits: List[str] = []
    for ch in term:
        if not ch.isalpha():
            continue
        name = TRANSLITERATION.get(ch.upper())
        entry = alphabet.get(name.lower()) if name else None
        if entry is None:
            continue
        val = entry.get(mode) or 0
        per_letter.append({"letter": ch, "hebrew": name, mode: val})
        total += int(val)
        roman_hits.append(name)
    return {"per_letter": per_letter, "total": total, "romanized": roman_hits}


# Best-effort English → Hebrew letter name transliteration.
# Ambiguous mappings resolve to the most common Kabbalistic usage:
#   C→Kaf (also Samech), H→Heh (also Chet), S→Samech (also Shin),
#   T→Tav (also Tet), X→Kaf (rare), J→Yod (also Gimel in some systems)
TRANSLITERATION: Dict[str, str] = {
    "A": "Aleph", "B": "Bet", "C": "Kaf", "D": "Dalet", "E": "Heh",
    "F": "Peh", "G": "Gimel", "H": "Heh", "I": "Yod", "J": "Yod",
    "K": "Kaf", "L": "Lamed", "M": "Mem", "N": "Nun", "O": "Ayin",
    "P": "Peh", "Q": "Qoph", "R": "Resh", "S": "Samech", "T": "Tav",
    "U": "Vav", "V": "Vav", "W": "Vav", "X": "Kaf", "Y": "Yod",
    "Z": "Zayin",
}


def hebrew_letter_for_value(value: int, mode: str = "hecrechi") -> Optional[Dict[str, Any]]:
    """Resolve a numeric value to the Hebrew letter whose value matches.

    Canon link: GRAMA = 40 (English ordinal) → Mem (hecrechi 40) = Water.
    """
    alphabet = _load_alphabet_map()
    for entry in alphabet.values():
        if int(entry.get(mode) or 0) == int(value):
            return {
                "hebrew": entry.get("romanized"),
                "letter": entry.get("letter"),
                "position": entry.get("position"),
                "hecrechi": entry.get("hecrechi"),
                "katan": entry.get("katan"),
                "element": entry.get("element"),
                "tarot_key": entry.get("tarot_key"),
                "tarot_name": entry.get("tarot_name"),
                "archetype": entry.get("archetype"),
            }
    return None


# ---------------------------------------------------------------------------
# 5. ABAZITH PHONEME RESONANCE  (SKRY Lens 6 — sonic texture)
# ---------------------------------------------------------------------------

# Vowels carry open resonance values; consonants their ordinal value.
ABAZITH_VOWELS = {"A": 1, "E": 5, "I": 9, "O": 15, "U": 21, "Y": 25}


def abazith_resonance(term: str) -> Dict[str, Any]:
    """Abazith phoneme resonance sum for a term (SKRY Lens 6).

    Vowel letters use the Abazith vowel table; consonants use ordinal
    position (B:2..Z:26). Returns per-letter resonance + total.
    """
    per_letter: List[Dict[str, Any]] = []
    total = 0
    for ch in term:
        if not ch.isalpha():
            continue
        upper = ch.upper()
        if upper in ABAZITH_VOWELS:
            val = ABAZITH_VOWELS[upper]
            kind = "vowel"
        else:
            val = SACRED_ALPHABET_MAP[upper]
            kind = "consonant"
        per_letter.append({"letter": ch, "kind": kind, "resonance": val})
        total += val
    return {"per_letter": per_letter, "total": total}


# ---------------------------------------------------------------------------
# REDUCTION + COMPARISON
# ---------------------------------------------------------------------------


def reduce_to_digit(value: int) -> int:
    """Digital root / single-digit reduction."""
    v = abs(value)
    while v > 9:
        v = sum(int(d) for d in str(v))
    return v


@dataclass
class CipherComparison:
    term: str
    english_gematria: int
    english_gematria_digit: int
    grrama_cipher: str
    sigil_encoded: str
    sigil_decoded: str
    hebrew: Dict[str, Any]
    abazith: Dict[str, Any]
    agreement: Dict[str, bool] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    @property
    def digits(self) -> Dict[str, int]:
        """All single-digit reductions across numeric systems."""
        return {
            "english_gematria": self.english_gematria_digit,
            "hebrew": reduce_to_digit(self.hebrew.get("total", 0)),
            "abazith": reduce_to_digit(self.abazith.get("total", 0)),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term": self.term,
            "english_gematria": self.english_gematria,
            "english_gematria_digit": self.english_gematria_digit,
            "grrama_cipher": self.grrama_cipher,
            "sigil_encoded": self.sigil_encoded,
            "sigil_decoded": self.sigil_decoded,
            "hebrew": self.hebrew,
            "abazith": self.abazith,
            "digits": self.digits,
            "agreement": self.agreement,
            "notes": self.notes,
        }


def compare_ciphers(term: str, hebrew_mode: str = "position") -> CipherComparison:
    """Compare every SacredSpace cipher system for a term.

    Returns a CipherComparison with per-system values, single-digit
    reductions, and an agreement map across numeric systems.
    """
    eng = gematria(term)
    heb = hebrew_value(term, mode=hebrew_mode)
    abz = abazith_resonance(term)

    heb_letter = hebrew_letter_for_value(eng, mode="hecrechi")

    digits = {
        "english_gematria": reduce_to_digit(eng),
        "hebrew": reduce_to_digit(heb["total"]),
        "abazith": reduce_to_digit(abz["total"]),
    }

    # Agreement: all non-zero systems resolving to the same single digit.
    nonzero = {k: v for k, v in digits.items() if v != 0}
    agreement: Dict[str, bool] = {k: False for k in digits}
    if nonzero:
        consensus = max(set(nonzero.values()), key=list(nonzero.values()).count)
        if len(set(nonzero.values())) == 1:
            agreement = {k: True for k in digits}
        else:
            agreement = {k: (v == consensus) for k, v in digits.items()}

    notes: List[str] = []
    if heb_letter:
        notes.append(
            f"English gematria {eng} resolves to Hebrew letter "
            f"{heb_letter['hebrew']} (hecrechi {heb_letter['hecrechi']}, "
            f"element {heb_letter['element'] or '—'}, tarot "
            f"{heb_letter['tarot_name'] or '—'})"
        )
    if len(set(nonzero.values())) == 1 and nonzero:
        notes.append(f"ALL numeric systems align on digit {consensus} — strong resonance.")
    elif nonzero:
        note = "Partial alignment: " + ", ".join(
            f"{k}->{v}" for k, v in sorted(nonzero.items())
        )
        notes.append(note)
    else:
        notes.append("No resolvable numeric values (term may contain no alphabet letters).")

    return CipherComparison(
        term=term,
        english_gematria=eng,
        english_gematria_digit=digits["english_gematria"],
        grrama_cipher=cipher(term),
        sigil_encoded=sigil_encode(term),
        sigil_decoded=sigil_decode_partial(sigil_encode(term)),
        hebrew=heb,
        abazith=abz,
        agreement=agreement,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_comparison(c: CipherComparison) -> None:
    print(f"✦ COMPARE CIPHERS — '{c.term}'")
    print("─" * 50)
    print(f"English ordinal gematria : {c.english_gematria}  →  {c.english_gematria_digit}")
    print(f"GR∆M∆ cipher             : {c.grrama_cipher}")
    print(f"Sacred Sigil encoded     : {c.sigil_encoded}")
    if c.sigil_decoded:
        print(f"Sacred Sigil decoded     : {c.sigil_decoded}")
    print(f"Hebrew ({len(c.hebrew['per_letter'])} letters)      : {c.hebrew['total']}  →  {reduce_to_digit(c.hebrew['total'])}")
    if c.hebrew["per_letter"]:
        romanized = " ".join(c.hebrew["romanized"])
        print(f"Hebrew transliteration   : {romanized}")
    abz_tot = c.abazith["total"]
    print(f"Abazith resonance        : {abz_tot}  →  {reduce_to_digit(abz_tot)}")
    print(f"Agreement                : {c.agreement}")
    for note in c.notes:
        print(f"NOTE: {note}")
    print("─" * 50)
    print("∆ Sacredspace cipher core active. In lakesh alakin.")


if __name__ == "__main__":
    import sys

    terms = sys.argv[1:] or ["GRAMA", "HERMES", "SACREDSPACE", "VALEN"]
    for t in terms:
        _print_comparison(compare_ciphers(t))
        print()
