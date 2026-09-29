# DRIVE_TEMPLATE_INDEX — 02_COUNCIL_GROVE
> SacredSpace OS | Council Grove Template Registry

---

## Template Registry

| Template Key | Description | Pillar |
|---|---|---|
| COUNCIL_GROVE_SESSION | v2.0 — dual-mode Claude seat (Sidebar/Code) | 02 |

---

## Drive IDs

| Key | Drive ID | Status |
|---|---|---|
| COUNCIL_GROVE_SESSION | `1qg5JYOXSX8RjHTg2g3eVTbDnUCwy3mgFXbfCSYHhPMs` | Active (v2.0) |
| COUNCIL_GROVE_SESSION_V1_ARCHIVE | `1wa_kY_IunGb9TjhmIZEXI-8NqO5OqqbgLwX6my6CMmc` | Superseded |

---

## Usage

### Claude Seat — CODE MODE

```bash
cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE
python council_grove_runner.py CG-2026-05-19-001 "Your session topic here" "keywords"
```

### Claude Seat — SIDEBAR MODE

1. Open Council Grove session doc in Google Docs.
2. Open Gemini sidebar (Extensions → Gemini in Docs or ✦ icon).
3. Copy the SIDEBAR PROMPT from the Claude seat block.
4. Paste session intent into the `[PASTE SESSION INTENT HERE]` field.
5. Hit Generate → Insert at cursor inside the `Input:` field.

---

## Mode Decision Tree

```
Starting a Council Grove session?
│
├─ Do you need Claude to READ FILES, QUERY APIs, or WRITE TO DISK?
│   └─ YES → CODE MODE
│              Run: python council_grove_runner.py <SESSION_ID> <TOPIC>
│
└─ Is this a reasoning/narrative/research session in Docs?
    └─ YES → SIDEBAR MODE
               Use Gemini sidebar prompts from the v2.0 template
```

---

*In lakesh alakin. ∆.*
