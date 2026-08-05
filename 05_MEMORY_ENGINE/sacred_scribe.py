#!/usr/bin/env python3
"""
SACREDSPACESCRIBE Phase 1 — Audit + Routing Engine
Locates, analyzes, and routes fragmented work across SacredSpace
"""

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse

class SCRIBE:
    def __init__(self, vault_path="/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault"):
        self.vault_path = Path(vault_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "files_by_pillar": defaultdict(list),
            "files_by_status": defaultdict(list),
            "orphaned_files": [],
            "isolated_files": [],
            "suggestions": [],
            "contradictions": []
        }

    def audit_vault(self):
        """Scan entire vault and build audit index"""
        print(f"[SCRIBE] Scanning vault: {self.vault_path}")

        files_scanned = 0
        for md_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(md_file):
                continue

            files_scanned += 1
            rel_path = md_file.relative_to(self.vault_path)

            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Extract frontmatter
                    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                    pillar = None
                    status = None
                    agent = None
                    tags = []

                    if fm_match:
                        fm = fm_match.group(1)
                        pillar_match = re.search(r'pillar:\s*(.+?)$', fm, re.MULTILINE)
                        if pillar_match:
                            pillar = pillar_match.group(1).strip()

                        status_match = re.search(r'status:\s*(.+?)$', fm, re.MULTILINE)
                        if status_match:
                            status = status_match.group(1).strip()

                        agent_match = re.search(r'agent:\s*(.+?)$', fm, re.MULTILINE)
                        if agent_match:
                            agent = agent_match.group(1).strip()

                        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', fm)
                        if tags_match:
                            tags = [t.strip() for t in tags_match.group(1).split(',')]

                    # Count wikilinks
                    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)

                    # Store record
                    record = {
                        "file": str(rel_path),
                        "pillar": pillar,
                        "status": status,
                        "agent": agent,
                        "tags": tags,
                        "wikilinks": wikilinks,
                        "wikilink_count": len(wikilinks)
                    }

                    # Categorize
                    if pillar:
                        self.results["files_by_pillar"][pillar].append(record)
                    else:
                        self.results["orphaned_files"].append(record)

                    if status:
                        self.results["files_by_status"][status].append(record)

                    if len(wikilinks) == 0 and "00_INBOX" not in str(md_file):
                        self.results["isolated_files"].append(record)

            except Exception as e:
                print(f"  ⚠️  Error reading {rel_path}: {e}")

        self.results["total_files"] = files_scanned
        print(f"✓ Scanned {files_scanned} files")
        return self.results

    def analyze_04_sacred_codex(self):
        """Deep dive into 04_SACRED_CODEX pillar"""
        print("\n[SCRIBE] Analyzing 04_SACRED_CODEX (game system lore)...")

        codex_files = [f for f in self.results["files_by_pillar"].get("04_SACRED_CODEX", [])]

        # Organize by type
        archetypes = [f for f in codex_files if "ARCHETYPE" in f["file"]]
        episodes = [f for f in codex_files if "EPISODE" in f["file"]]
        npcs = [f for f in codex_files if "NPC" in f["file"]]
        nodes = [f for f in codex_files if "NODE" in f["file"]]
        schools = [f for f in codex_files if "SCHOOL" in f["file"]]

        print(f"  Archetypes: {len(archetypes)} files")
        print(f"  Episodes: {len(episodes)} files")
        print(f"  NPCs: {len(npcs)} files")
        print(f"  Nodes: {len(nodes)} files")
        print(f"  Schools: {len(schools)} files")

        # Check wikilink density
        avg_links = sum(f["wikilink_count"] for f in codex_files) / len(codex_files) if codex_files else 0
        print(f"  Average wikilinks per file: {avg_links:.2f}")

        # Suggest MOC structure
        self.results["suggestions"].append({
            "pillar": "04_SACRED_CODEX",
            "action": "AUTO_MOC",
            "suggestion": "Generate hierarchical MOC: Archetypes → Episodes → Nodes → NPCs → Schools",
            "files_affected": len(codex_files)
        })

    def detect_contradictions(self):
        """Surface contradictions and inconsistencies"""
        print("\n[SCRIBE] Detecting contradictions...")

        # Check for status inconsistencies
        status_lower = [f for f in self.results["files_by_status"].get("active", [])
                       if f["status"] == "active"]
        status_upper = [f for f in self.results["files_by_status"].get("ACTIVE", [])
                       if f["status"] == "ACTIVE"]

        if status_lower and status_upper:
            self.results["contradictions"].append({
                "type": "STATUS_CASE_INCONSISTENCY",
                "severity": "LOW",
                "count": len(status_lower) + len(status_upper),
                "message": "Pillar status values use mixed case (canon vs CANON, active vs ACTIVE)",
                "files": [f["file"] for f in status_lower[:3]]
            })

        # Check for pillar naming inconsistency
        pillar_codes = [p for p in self.results["files_by_pillar"].keys() if p.startswith(("0", "1", "2"))]
        pillar_names = [p for p in self.results["files_by_pillar"].keys() if not p.startswith(("0", "1", "2"))]

        if pillar_codes and pillar_names:
            self.results["contradictions"].append({
                "type": "PILLAR_NAMING_INCONSISTENCY",
                "severity": "MEDIUM",
                "pillar_codes": len(pillar_codes),
                "old_names": len(pillar_names),
                "message": f"Mixed pillar naming: {len(pillar_codes)} use codes (04_SACRED_CODEX), {len(pillar_names)} use old names (SYSTEMS, LEARNING, etc.)",
                "old_name_examples": list(pillar_names)[:5]
            })

    def generate_routing_suggestions(self):
        """Suggest routes for orphaned files"""
        print("\n[SCRIBE] Generating routing suggestions...")

        # Orphaned files routing
        for orphan in self.results["orphaned_files"][:10]:
            filename = orphan["file"].lower()
            suggested_pillar = "04_SACRED_CODEX"  # Default to codex

            if any(x in filename for x in ["npc", "character", "archetype", "episode", "node"]):
                suggested_pillar = "04_SACRED_CODEX"
            elif any(x in filename for x in ["agent", "icaris", "council", "iris"]):
                suggested_pillar = "06_AGENT_LAYER"
            elif any(x in filename for x in ["social", "brand", "content"]):
                suggested_pillar = "07_SOCIAL_MOTHERSHIP"
            elif any(x in filename for x in ["economy", "market", "product"]):
                suggested_pillar = "09_SACRED_MARKET"

            self.results["suggestions"].append({
                "file": orphan["file"],
                "current_state": "NO_PILLAR",
                "suggested_pillar": suggested_pillar,
                "confidence": "HIGH" if any(x in filename for x in ["npc", "archetype"]) else "MEDIUM",
                "action": "ASSIGN_PILLAR"
            })

    def report(self, output_format="markdown"):
        """Generate audit report"""
        print("\n[SCRIBE] Generating report...")

        report = f"""# SACREDSPACESCRIBE Phase 1 Audit Report
**Generated**: {self.results['timestamp']}
**Status**: INITIAL AUDIT COMPLETE

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Total files scanned | {self.results['total_files']} |
| Files with pillar assignment | {sum(len(v) for v in self.results['files_by_pillar'].values())} |
| **Orphaned files (NO pillar)** | **{len(self.results['orphaned_files'])}** |
| **Isolated files (NO wikilinks)** | **{len(self.results['isolated_files'])}** |
| Contradictions detected | {len(self.results['contradictions'])} |
| Routing suggestions | {len(self.results['suggestions'])} |

## PILLAR COVERAGE

"""
        for pillar, files in sorted(self.results["files_by_pillar"].items()):
            report += f"- **{pillar}**: {len(files)} files\n"

        report += f"\n## STATUS BREAKDOWN\n\n"
        for status, files in sorted(self.results["files_by_status"].items()):
            report += f"- {status}: {len(files)} files\n"

        report += f"\n## CRITICAL FINDINGS\n\n"
        report += f"### Orphaned Files ({len(self.results['orphaned_files'])})\n"
        report += f"Files without pillar assignment:\n"
        for orphan in self.results['orphaned_files'][:5]:
            report += f"- {orphan['file']}\n"
        if len(self.results['orphaned_files']) > 5:
            report += f"- ... and {len(self.results['orphaned_files']) - 5} more\n"

        report += f"\n### Isolated Files ({len(self.results['isolated_files'])})\n"
        report += f"Files with zero wikilinks (not connected to graph):\n"
        for isolated in self.results['isolated_files'][:5]:
            report += f"- {isolated['file']} (status: {isolated.get('status', 'unknown')})\n"
        if len(self.results['isolated_files']) > 5:
            report += f"- ... and {len(self.results['isolated_files']) - 5} more\n"

        if self.results['contradictions']:
            report += f"\n### Contradictions Detected\n"
            for contra in self.results['contradictions']:
                report += f"- **{contra['type']}** (Severity: {contra.get('severity', 'MEDIUM')})\n"
                report += f"  {contra['message']}\n"

        report += f"\n## ROUTING SUGGESTIONS (Phase 1)\n\n"
        for sugg in self.results['suggestions'][:10]:
            if sugg.get('action') == 'ASSIGN_PILLAR':
                report += f"- `{sugg['file']}` → **{sugg['suggested_pillar']}** ({sugg['confidence']})\n"

        report += f"\n## NEXT STEPS\n\n"
        report += f"1. Review routing suggestions above\n"
        report += f"2. Normalize pillar naming (use codes: 01-09, not old folder names)\n"
        report += f"3. Normalize status values (CANON, STUB, GENERATED, EXPERIMENTAL, SEEDING, ACTIVE)\n"
        report += f"4. Assign pillar to {len(self.results['orphaned_files'])} orphaned files\n"
        report += f"5. Inject wikilinks to connect isolated files\n"
        report += f"6. Auto-generate MOCs per pillar\n"
        report += f"\n*In lakesh alakin. The SCRIBE stands ready to route.* ∆\n"

        return report

    def save_index(self, path="/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/scribe_audit_index.json"):
        """Save persistent audit index"""
        # Convert defaultdicts to regular dicts for JSON serialization
        results_serializable = {
            "timestamp": self.results["timestamp"],
            "total_files": self.results["total_files"],
            "files_by_pillar": dict(self.results["files_by_pillar"]),
            "files_by_status": dict(self.results["files_by_status"]),
            "orphaned_files": self.results["orphaned_files"],
            "isolated_files": self.results["isolated_files"],
            "suggestions": self.results["suggestions"],
            "contradictions": self.results["contradictions"]
        }

        with open(path, 'w') as f:
            json.dump(results_serializable, f, indent=2)

        print(f"✓ Audit index saved: {path}")

def main():
    parser = argparse.ArgumentParser(description="SACREDSPACESCRIBE Phase 1 Audit")
    parser.add_argument("command", choices=["audit", "report"], default="audit", nargs="?")
    parser.add_argument("--vault", default="/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
    parser.add_argument("--output", default="/tmp/claude-1000/-home-useroak3ytree/c5b0b39d-1501-4529-be67-7fd1c6b3875c/scratchpad/SCRIBE_PHASE1_AUDIT_REPORT.md")

    args = parser.parse_args()

    scribe = SCRIBE(vault_path=args.vault)

    if args.command == "audit" or args.command is None:
        scribe.audit_vault()
        scribe.analyze_04_sacred_codex()
        scribe.detect_contradictions()
        scribe.generate_routing_suggestions()
        scribe.save_index()

        report = scribe.report()
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\n✓ Report generated: {args.output}")
        print(report)

if __name__ == "__main__":
    main()
