#!/usr/bin/env python3
"""
REALITY_LAYER Phase 1 MVP
QR-based shrine creation, visitation, and Obsidian sync
"""

import sqlite3
import json
import uuid
from pathlib import Path
from datetime import datetime
import requests
import argparse
from typing import Optional

class RealityLayer:
    def __init__(self, db_path="/mnt/d/SacredSpace_OS/04_SACRED_CODEX/reality_layer/sacred_journey.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.vault_path = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/REALITY_LAYER")
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.pulse_url = "http://localhost:8890"
        self.init_db()

    def init_db(self):
        """Initialize database from schema"""
        schema_path = Path("/mnt/d/SacredSpace_OS/04_SACRED_CODEX/reality_layer/sacred_journey.sql")
        if schema_path.exists():
            with open(schema_path) as f:
                conn = sqlite3.connect(self.db_path)
                conn.executescript(f.read())
                conn.commit()
                conn.close()

    def create_character(self, name: str) -> str:
        """Create a new character (player)"""
        char_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO characters (character_id, name) VALUES (?, ?)",
            (char_id, name)
        )
        conn.commit()
        conn.close()
        print(f"✅ Character created: {name} ({char_id})")
        return char_id

    def create_shrine(self, char_id: str, name: str, archetype: str,
                     lat: Optional[float] = None, lon: Optional[float] = None,
                     founding_story: str = "") -> str:
        """Create a new shrine"""
        shrine_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT INTO shrines
               (shrine_id, character_id, name, location_lat, location_lon, archetype, founding_story)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (shrine_id, char_id, name, lat, lon, archetype, founding_story)
        )
        conn.commit()
        conn.close()

        # Generate QR code
        self.generate_qr(shrine_id, name)

        # Create Obsidian entry
        self.create_shrine_obsidian_entry(shrine_id, name, archetype, lat, lon, founding_story)

        print(f"✅ Shrine created: {name}")
        print(f"   Archetype: {archetype}")
        print(f"   Location: ({lat}, {lon})" if lat and lon else "   Location: Not specified")
        print(f"   Shrine ID: {shrine_id}")
        return shrine_id

    def generate_qr(self, shrine_id: str, shrine_name: str):
        """Generate QR code payload for shrine"""
        payload = f"qr://shrine/{shrine_id}?v=1"

        # Save payload as text (can be printed/encoded into QR later)
        qr_path = self.vault_path / f"QR_{shrine_name.replace(' ', '_')}.txt"
        with open(qr_path, 'w') as f:
            f.write(payload)

        # Store in DB
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO qr_codes (qr_id, shrine_id, qr_payload, qr_image_path) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), shrine_id, payload, str(qr_path))
        )
        conn.commit()
        conn.close()

        print(f"   QR payload: {payload}")
        print(f"   (Generate QR: https://qr-server.com/qr?data={payload})")

    def create_shrine_obsidian_entry(self, shrine_id: str, name: str, archetype: str,
                                   lat: Optional[float] = None, lon: Optional[float] = None,
                                   founding_story: str = ""):
        """Create Obsidian vault entry for shrine"""
        shrines_dir = self.vault_path / "SHRINES"
        shrines_dir.mkdir(exist_ok=True)

        frontmatter = f"""---
title: {name}
pillar: 04_SACRED_CODEX
topic: REALITY_LAYER
archetype: {archetype}
shrine_id: {shrine_id}
location: {lat}°N, {lon}°E
visits: 0
family_access: solo
status: ACTIVE
created: {datetime.now().isoformat()}
---

# {name}

**Archetype**: {archetype}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Visits**: 0

## Founding Story

{founding_story if founding_story else '(Your story of why this place is sacred)'}

## Visit History

(Visits will be logged here)

---

*In lakesh alakin. This shrine is sealed.* ∆
"""

        file_path = shrines_dir / f"{name.replace(' ', '_')}.md"
        with open(file_path, 'w') as f:
            f.write(frontmatter)

        print(f"   Obsidian entry: {file_path.relative_to(self.vault_path)}")

    def log_visit(self, shrine_id: str, char_id: str, ritual_type: str = "journal",
                 intention: str = "", journal_entry: str = ""):
        """Log a shrine visit"""
        visit_id = str(uuid.uuid4())
        visited_at = datetime.now()

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT INTO visits
               (visit_id, shrine_id, character_id, ritual_type, intention, journal_entry, visited_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (visit_id, shrine_id, char_id, ritual_type, intention, journal_entry, visited_at)
        )

        # Update shrine visit count
        conn.execute("UPDATE shrines SET visit_count = visit_count + 1 WHERE shrine_id = ?", (shrine_id,))
        conn.commit()
        conn.close()

        # Publish to Sacred Pulse
        self.publish_to_pulse("reality_layer:shrine_visited", {
            "visit_id": visit_id,
            "shrine_id": shrine_id,
            "character_id": char_id,
            "ritual_type": ritual_type,
            "intention": intention,
            "timestamp": visited_at.isoformat()
        })

        # Sync to Obsidian
        self.sync_visit_to_obsidian(visit_id, shrine_id, char_id, intention, journal_entry)

        print(f"✅ Visit logged: {shrine_id}")
        print(f"   Ritual type: {ritual_type}")
        print(f"   Intention: {intention}")
        return visit_id

    def publish_to_pulse(self, topic: str, payload: dict):
        """Publish event to Sacred Pulse event bus"""
        try:
            response = requests.post(
                f"{self.pulse_url}/publish",
                json={"topic": topic, "payload": payload},
                timeout=2
            )
            if response.status_code == 200:
                print(f"   ✓ Published to Pulse: {topic}")
            else:
                print(f"   ⚠️  Pulse publish failed: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Pulse unreachable: {e}")

    def sync_visit_to_obsidian(self, visit_id: str, shrine_id: str, char_id: str,
                              intention: str, journal_entry: str):
        """Sync visit to Obsidian vault"""
        # Get shrine info
        conn = sqlite3.connect(self.db_path)
        shrine = conn.execute(
            "SELECT name, archetype FROM shrines WHERE shrine_id = ?", (shrine_id,)
        ).fetchone()
        conn.close()

        if not shrine:
            return

        shrine_name, archetype = shrine
        shrine_file = self.vault_path / "SHRINES" / f"{shrine_name.replace(' ', '_')}.md"

        if not shrine_file.exists():
            print(f"   ⚠️  Shrine file not found: {shrine_file}")
            return

        # Append visit entry
        visit_entry = f"""
## Visit — {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Intention**: {intention}

{journal_entry}

---
"""

        with open(shrine_file, 'a') as f:
            f.write(visit_entry)

        # Update database
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "UPDATE visits SET synced_to_obsidian = TRUE, synced_at = ? WHERE visit_id = ?",
            (datetime.now(), visit_id)
        )
        conn.commit()
        conn.close()

        print(f"   ✓ Synced to Obsidian: {shrine_file.name}")

    def list_shrines(self, char_id: str):
        """List all shrines for a character"""
        conn = sqlite3.connect(self.db_path)
        shrines = conn.execute(
            "SELECT shrine_id, name, archetype, visit_count FROM shrines WHERE character_id = ? ORDER BY name",
            (char_id,)
        ).fetchall()
        conn.close()

        if not shrines:
            print("No shrines yet. Create one with: reality-layer create-shrine")
            return

        print(f"\n🏛️  Your Shrines:\n")
        for shrine_id, name, archetype, visits in shrines:
            print(f"  {name}")
            print(f"    Archetype: {archetype}")
            print(f"    Visits: {visits}")
            print(f"    ID: {shrine_id}\n")

    def show_status(self, char_id: str):
        """Show character + shrine status"""
        conn = sqlite3.connect(self.db_path)
        char = conn.execute(
            "SELECT name, current_archetype, total_visits FROM characters WHERE character_id = ?",
            (char_id,)
        ).fetchone()
        shrines = conn.execute(
            "SELECT COUNT(*), SUM(visit_count) FROM shrines WHERE character_id = ?",
            (char_id,)
        ).fetchone()
        conn.close()

        if not char:
            print("Character not found")
            return

        name, current_archetype, total_visits = char
        shrine_count, total_shrine_visits = shrines

        print(f"\n✨ {name} — Sacred Journey Status\n")
        print(f"  Current Archetype: {current_archetype}")
        print(f"  Shrines Created: {shrine_count or 0}")
        print(f"  Total Visits: {total_shrine_visits or 0}")
        print(f"  Character ID: {char_id}\n")

def main():
    parser = argparse.ArgumentParser(description="REALITY_LAYER Phase 1 MVP")
    subparsers = parser.add_subparsers(dest="command")

    # Create character
    create_char = subparsers.add_parser("create-character", help="Create a new character")
    create_char.add_argument("name", help="Character name")

    # Create shrine
    create_shrine = subparsers.add_parser("create-shrine", help="Create a new shrine")
    create_shrine.add_argument("char_id", help="Character ID")
    create_shrine.add_argument("name", help="Shrine name")
    create_shrine.add_argument("archetype", help="Archetype (Hermit, Lovers, etc.)")
    create_shrine.add_argument("--lat", type=float, help="Latitude")
    create_shrine.add_argument("--lon", type=float, help="Longitude")
    create_shrine.add_argument("--story", help="Founding story")

    # Log visit
    log_visit = subparsers.add_parser("log-visit", help="Log a shrine visit")
    log_visit.add_argument("shrine_id", help="Shrine ID")
    log_visit.add_argument("char_id", help="Character ID")
    log_visit.add_argument("--ritual", default="journal", help="Ritual type (photo, journal, affirmation)")
    log_visit.add_argument("--intention", help="Ritual intention")
    log_visit.add_argument("--journal", help="Journal entry")

    # List shrines
    list_shrines = subparsers.add_parser("list-shrines", help="List shrines for character")
    list_shrines.add_argument("char_id", help="Character ID")

    # Status
    status = subparsers.add_parser("status", help="Show character status")
    status.add_argument("char_id", help="Character ID")

    args = parser.parse_args()
    rl = RealityLayer()

    if args.command == "create-character":
        rl.create_character(args.name)
    elif args.command == "create-shrine":
        rl.create_shrine(args.char_id, args.name, args.archetype, args.lat, args.lon, args.story or "")
    elif args.command == "log-visit":
        rl.log_visit(args.shrine_id, args.char_id, args.ritual, args.intention or "", args.journal or "")
    elif args.command == "list-shrines":
        rl.list_shrines(args.char_id)
    elif args.command == "status":
        rl.show_status(args.char_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
