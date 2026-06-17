"""sigil_layer.py — SacredSigil Encoding Engine

Pillar: 07_SOCIAL/gematria_engine
Owner: AURORA
Status: ACTIVE

Purpose: Transforms standard English text into SacredSigil encoded form.
         Implements the Sigil Layer from the S∆CR3DS!G∆L K3YBOR∆D SYST3M.
"""

GLYPH_MAP = {
    'A': '∆',
    'E': '3',
    'I': '!',
    'O': '0',
    'S': 'S',  # keep readable; variant: '$'
    'T': '7',
    'Y': 'Y',  # variant: '¥'
    'H': 'H',  # variant: '#'
}

WORD_OVERRIDES = {
    # These override letter-by-letter encoding for sacred terms
    "SACRED":      "S∆CR3D",
    "SIGNAL":      "S!GN∆L",
    "KEYBOARD":    "K3YBOR∆D",
    "SYSTEM":      "SYST3M",
    "SOURCE":      "S0URC3",
    "SPIRIT":      "SP!R!T",
    "FOREST":      "F0R3ST",
    "CODEX":       "C0D3X",
    "ARCANA":      "∆RC∆N∆",
    "COUNCIL":     "C0UNC!L",
    "VAULT":       "V∆ULT",
    "RITE":        "R!T3",
    "GATE":        "G∆T3",
    "LORE":        "L0R3",
    "SPINE":       "SP!N3",
    "MEMORY":      "M3M0RY",
    "MOTE":        "M0T3",
    "FUNCTION":    "FUNCT!0N",
    "MODULE":      "M0DUL3",
    "SCRIPT":      "SCR!P7",
    "BOOTSTRAP":   "B00TSTR∆P",
    "SCHEMA":      "SCH3M∆",
    "COMMIT":      "C0MM!T",
    "BRANCH":      "BR∆NCH",
    "SACREDSPACE": "S∆CR3DSP@C3",
}


def encode_word(word: str) -> str:
    """Encode a single word using override table first, then letter substitution."""
    upper = word.upper()
    if upper in WORD_OVERRIDES:
        return WORD_OVERRIDES[upper]
    # Letter-by-letter encoding
    return ''.join(GLYPH_MAP.get(char, char) for char in upper)


def encode_phrase(text: str) -> str:
    """Encode a full phrase, word by word."""
    words = text.split()
    return ' '.join(encode_word(w) for w in words)


def decode_partial(encoded: str) -> str:
    """
    Best-effort reverse lookup. Not perfect — sigils are lossy by design.
    Returns human-readable approximation.
    """
    reverse_overrides = {v: k for k, v in WORD_OVERRIDES.items()}
    reverse_glyphs = {v: k for k, v in GLYPH_MAP.items()}

    words = encoded.split()
    result = []
    for word in words:
        if word in reverse_overrides:
            result.append(reverse_overrides[word])
        else:
            decoded = ''.join(reverse_glyphs.get(char, char) for char in word)
            result.append(decoded)
    return ' '.join(result)


if __name__ == "__main__":
    # Quick test
    tests = [
        "sacred forest",
        "sacredspace system codex",
        "in lakesh alakin",
        "council of arcana",
    ]
    print("=== SACREDSIGIL ENCODER TEST ===\n")
    for phrase in tests:
        encoded = encode_phrase(phrase)
        print(f"  {phrase:<30} → {encoded}")

    # Roundtrip test
    print("\n=== ROUNDTRIP TEST ===\n")
    for phrase in tests:
        encoded = encode_phrase(phrase)
        decoded = decode_partial(encoded)
        print(f"  {phrase:<30} → {encoded:<35} → {decoded}")

    print("\n∆ Sigil Layer active. In lakesh alakin.")
