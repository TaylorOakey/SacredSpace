#!/usr/bin/env python3
"""
SCRIBE Google Drive Source Integration
Indexes Google Docs, Sheets, and Takeout exports
Routes to canonical pillars via SACREDTAG
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import zipfile

class DriveSource:
    def __init__(self):
        self.vault_path = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
        self.raw_path = Path("/mnt/d/SacredSpace_OS/_RAW")
        self.documents = []
        self.index = {
            "timestamp": datetime.now().isoformat(),
            "total_docs": 0,
            "by_pillar": defaultdict(list),
            "unrouted": [],
            "suggestions": []
        }

    def scan_takeout_archives(self):
        """Extract and scan Google Takeout .zip files"""
        print("[SCRIBE Drive] Scanning Google Takeout archives...")

        for zip_file in self.raw_path.glob("takeout*.zip"):
            if ".partial" in zip_file.name:
                print(f"  ⚠️  Skipping partial: {zip_file.name} (2.6GB, incomplete)")
                continue

            print(f"  Scanning: {zip_file.name}")
            try:
                with zipfile.ZipFile(zip_file, 'r') as zf:
                    # Look for Google Docs JSON exports
                    for item in zf.namelist():
                        if 'Google Drive' in item and (item.endswith('.json') or 'document' in item.lower()):
                            self.documents.append({
                                "source": "Google Takeout",
                                "path": item,
                                "archive": zip_file.name,
                                "type": "document"
                            })
            except Exception as e:
                print(f"    Error: {e}")

    def scan_gdrive_exports(self):
        """Scan previously extracted Google Drive exports"""
        print("\n[SCRIBE Drive] Scanning Drive exports...")

        gdrive_paths = [
            Path("/mnt/c/03_NEURAL_FOREST/gdrive_export"),
            Path("/mnt/d/SacredSpace_OS/03_NEURAL_FOREST/gdrive_export"),
        ]

        for drive_path in gdrive_paths:
            if not drive_path.exists():
                continue

            for md_file in drive_path.rglob("*.md"):
                doc_name = md_file.stem
                self.documents.append({
                    "source": "Google Drive Export",
                    "path": str(md_file.relative_to(drive_path.parent)),
                    "name": doc_name,
                    "type": "markdown"
                })

        print(f"  Found {len(self.documents)} exported documents")

    def infer_pillar(self, doc_name):
        """Infer pillar from document name"""
        doc_lower = doc_name.lower()

        # Heuristic routing based on keywords
        if any(x in doc_lower for x in ["agent", "iris", "icaris", "council", "asher"]):
            return "06_AGENT_LAYER"
        elif any(x in doc_lower for x in ["social", "brand", "content", "marketing"]):
            return "07_SOCIAL_MOTHERSHIP"
        elif any(x in doc_lower for x in ["economy", "market", "product", "price"]):
            return "09_SACRED_MARKET"
        elif any(x in doc_lower for x in ["learn", "rite", "education", "course"]):
            return "08_LEARNING_PATH"
        elif any(x in doc_lower for x in ["game", "lore", "story", "archetype", "episode"]):
            return "04_SACRED_CODEX"
        elif any(x in doc_lower for x in ["system", "architecture", "plan", "spec"]):
            return "02_COUNCIL_GROVE"
        elif any(x in doc_lower for x in ["memory", "mind", "thought", "consciousness"]):
            return "05_MEMORY_ENGINE"
        else:
            return "03_NEURAL_FOREST"  # Default to research

    def index_documents(self):
        """Build index of all Drive documents"""
        print("\n[SCRIBE Drive] Indexing Google Drive documents...")

        routed = 0
        unrouted = 0

        for doc in self.documents:
            doc_name = doc.get("name", Path(doc["path"]).stem)
            pillar = self.infer_pillar(doc_name)

            record = {
                "name": doc_name,
                "source": doc["source"],
                "path": doc["path"],
                "type": doc["type"],
                "inferred_pillar": pillar,
                "action": "ROUTE_TO_PILLAR"
            }

            if pillar:
                self.index["by_pillar"][pillar].append(record)
                routed += 1
            else:
                self.index["unrouted"].append(record)
                unrouted += 1

        self.index["total_docs"] = routed + unrouted
        print(f"  ✓ Indexed {routed} documents with pillar assignment")
        if unrouted:
            print(f"  ⚠️  {unrouted} documents need manual routing")

    def generate_sacredtag_templates(self):
        """Generate SACREDTAG frontmatter templates for Drive documents"""
        print("\n[SCRIBE Drive] Generating SACREDTAG templates...")

        templates = []
        for pillar, docs in self.index["by_pillar"].items():
            for doc in docs[:2]:  # Sample first 2 per pillar
                template = f"""---
# Add this to top of {doc['name']}
title: {doc['name']}
pillar: {pillar}
source: Google Drive
status: DISTILLED
tags: [from-drive, {pillar.lower()}]
date_imported: {datetime.now().isoformat()}
original_source: {doc['source']}
---"""
                templates.append(template)

        return templates

    def generate_report(self):
        """Generate Drive integration report"""
        report = f"""# SCRIBE Google Drive Source — Integration Report

**Generated**: {self.index['timestamp']}
**Status**: INDEXED AND ROUTED

## Summary

| Metric | Value |
|--------|-------|
| **Total Google Drive documents found** | {self.index['total_docs']} |
| **Documents indexed** | {sum(len(v) for v in self.index['by_pillar'].values())} |
| **Documents routed to pillars** | {sum(len(v) for v in self.index['by_pillar'].values())} |
| **Unrouted documents** | {len(self.index['unrouted'])} |

## Pillar Distribution

"""
        for pillar, docs in sorted(self.index["by_pillar"].items()):
            report += f"- **{pillar}**: {len(docs)} documents\n"

        report += f"""

## Sample Documents by Pillar

"""
        for pillar, docs in sorted(self.index["by_pillar"].items()):
            report += f"\n### {pillar}\n"
            for doc in docs[:3]:
                report += f"- {doc['name']} (from {doc['source']})\n"

        report += f"""

## Integration Instructions

To import Google Drive documents into the vault:

1. **Extract Takeout archives** (if not already done)
   ```bash
   unzip takeout-20260609T031003Z-6-001.zip -d /mnt/d/SacredSpace_OS/_RAW/takeout_extracted/
   ```

2. **Convert Google Docs to Markdown**
   - Use: Google Docs → Download as → Markdown
   - Or use: `gdocs2md` script (Python package)

3. **Apply SACREDTAG frontmatter** (see templates below)

4. **Move to canonical pillar folders**
   ```bash
   mv document.md /mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/[PILLAR]/
   ```

5. **Re-run SCRIBE audit**
   ```bash
   python3 05_MEMORY_ENGINE/sacred_scribe.py audit
   ```

## SACREDTAG Templates

"""
        templates = self.generate_sacredtag_templates()
        for i, template in enumerate(templates[:5], 1):
            report += f"\n**Template {i}:**\n```yaml\n{template}\n```\n"

        report += f"""

## Next Steps

1. Extract full Takeout archive (2.6GB partial file)
2. Convert all Google Docs to Markdown
3. Apply SACREDTAG metadata
4. Re-run full audit
5. Wikilink injection to connect with Obsidian graph

**Status**: Ready for manual document migration + auto-indexing

*Drive source is now wired into SCRIBE. Execute import flow whenever ready.* ∆
"""
        return report

    def save_index(self, path="/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/scribe_drive_index.json"):
        """Save persistent Drive index"""
        index_serializable = {
            "timestamp": self.index["timestamp"],
            "total_docs": self.index["total_docs"],
            "by_pillar": {k: v for k, v in self.index["by_pillar"].items()},
            "unrouted": self.index["unrouted"],
        }

        with open(path, 'w') as f:
            json.dump(index_serializable, f, indent=2)

        print(f"✓ Drive index saved: {path}")

def main():
    scribe = DriveSource()

    print("[SCRIBE Drive Source] Wiring Google Drive integration...\n")

    scribe.scan_takeout_archives()
    scribe.scan_gdrive_exports()
    scribe.index_documents()
    scribe.save_index()

    report = scribe.generate_report()

    report_path = "/tmp/claude-1000/-home-useroak3ytree/c5b0b39d-1501-4529-be67-7fd1c6b3875c/scratchpad/SCRIBE_DRIVE_INTEGRATION.md"
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"\n✓ Drive integration report: {report_path}")
    print(report)

if __name__ == "__main__":
    main()
