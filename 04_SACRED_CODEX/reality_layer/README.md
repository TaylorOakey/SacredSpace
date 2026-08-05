# REALITY_LAYER — Phase 1 MVP

**Status**: ✅ OPERATIONAL  
**Date**: 2026-08-04  
**Build**: QR shrine creation + Obsidian sync

---

## QUICK START

### 1. Create a Character
```bash
cd /mnt/d/SacredSpace_OS/04_SACRED_CODEX/reality_layer
python3 reality_layer.py create-character "Your Name"
```
Returns your `character_id` (save this).

### 2. Create a Shrine
```bash
python3 reality_layer.py create-shrine {character_id} "Shrine Name" "Archetype" \
  --lat 40.7128 --lon 74.0060 \
  --story "Why this place is sacred to you"
```

**Archetypes**: Hermit, Lovers, Magician, Strength, Fool, Emperor, Priestess, Chariot, Wheel, Justice, Hanged Man, Death, Temperance, Devil, Tower, Star, Moon, Sun, Judgement, World, Magician

Returns your `shrine_id`.

### 3. Log a Visit
```bash
python3 reality_layer.py log-visit {shrine_id} {character_id} \
  --ritual journal \
  --intention "Your intention for this visit" \
  --journal "What you experienced and learned"
```

**Ritual types**: `journal`, `photo`, `affirmation`, `sketch`

### 4. Check Status
```bash
python3 reality_layer.py status {character_id}
python3 reality_layer.py list-shrines {character_id}
```

---

## WHAT HAPPENS WHEN YOU:

### Create a Shrine
1. ✅ Shrine data saved to SQLite (`sacred_journey.db`)
2. ✅ QR payload generated (print/scan this later)
3. ✅ Obsidian entry created in `SHRINES/` folder
4. ✅ Founding story recorded in vault

### Log a Visit
1. ✅ Visit data saved to SQLite
2. ✅ Shrine visit count incremented
3. ✅ Event published to Sacred Pulse (if running)
4. ✅ Visit logged to Obsidian shrine entry
5. ✅ Journal entry added to vault

---

## DATABASE

**Location**: `/mnt/d/SacredSpace_OS/04_SACRED_CODEX/reality_layer/sacred_journey.db`

**Tables**:
- `characters` — Your character data
- `shrines` — Shrine registry
- `visits` — Visit log
- `qr_codes` — QR payload storage
- `sync_log` — Sync history

**Query examples**:
```bash
sqlite3 sacred_journey.db "SELECT name, archetype, visit_count FROM shrines;"
sqlite3 sacred_journey.db "SELECT shrine_id, ritual_type, intention FROM visits ORDER BY visited_at DESC LIMIT 5;"
```

---

## OBSIDIAN VAULT INTEGRATION

**Vault location**: `/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/REALITY_LAYER/`

**Structure**:
```
REALITY_LAYER/
├── SHRINES/
│   ├── The_River.md (shrine entry + visit log)
│   ├── The_Summit.md
│   └── Council_Grove.md
├── JOURNEYS/
│   └── (Character journey logs — Phase 2)
└── FAMILY_MYTHOLOGY/
    └── (Family mythology — Phase 2)
```

Every shrine visit automatically:
1. Appends to the shrine's Obsidian entry
2. Records intention + journal text
3. Timestamps the entry
4. Creates wikilink targets (for Phase 2: Archetype linking)

---

## WHAT'S NEXT (Phase 2+)

- [ ] Family layer (Iris/Asher character creation)
- [ ] Inherited shrines (family members visit your shrines)
- [ ] Family Arcana (family-scale archetype tracking)
- [ ] Monthly codex entries (NotebookLM pattern reflection)
- [ ] Character progression (5 Seals system)
- [ ] Sacred Pulse event listener fixes (422 error resolved)

---

## TESTING THE MVP

**End-to-end flow** (what you just did):

```bash
# Create character
python3 reality_layer.py create-character "Taylor"
# → Returns: dd81e58d-f0ec-4a0b-9505-564df6401721

# Create shrine (The River, Lovers archetype)
python3 reality_layer.py create-shrine dd81e58d-f0ec-4a0b-9505-564df6401721 \
  "The River" "Lovers" --lat 40.7128 --lon 74.0060 \
  --story "Where I find clarity and witness others fully."
# → Returns: 57ba778a-7a3f-4e8d-a902-bebfbcfd8e7e

# Log a visit
python3 reality_layer.py log-visit 57ba778a-7a3f-4e8d-a902-bebfbcfd8e7e \
  dd81e58d-f0ec-4a0b-9505-564df6401721 --ritual journal \
  --intention "To witness the flow and let go of control" \
  --journal "Sat by the water for an hour..."

# Check status
python3 reality_layer.py status dd81e58d-f0ec-4a0b-9505-564df6401721
python3 reality_layer.py list-shrines dd81e58d-f0ec-4a0b-9505-564df6401721
```

**Verify in Obsidian**:
1. Open vault: `/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/`
2. Navigate to: `00_CANON/REALITY_LAYER/SHRINES/The_River.md`
3. See your visit logged with timestamp + intention + journal entry

---

## KNOWN ISSUES (Phase 1)

- **Pulse 422 error**: Event schema mismatch. Will fix in Phase 1B.
- **SQLite deprecation warning**: Python 3.12 datetime adapter. Low priority.
- **QR as text**: Phase 1 encodes payload as `.txt`. Use https://qr-server.com to generate actual QR code image.

---

## NEXT PHASE (Phase 2)

Wire up:
- Iris character + inherited shrines
- Family-scoped shrines
- Family Arcana alignment
- Monthly codex generation via NotebookLM

**Status**: Ready to build when you give the word.

---

*In lakesh alakin. REALITY_LAYER Phase 1 is sealed.* ∆
