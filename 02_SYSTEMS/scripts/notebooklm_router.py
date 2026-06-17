import json
import subprocess
import sys
from pathlib import Path

ROUTING_PATH = Path("/mnt/d/SacredSpace_OS/02_SYSTEMS/CONFIGS/notebook_routing.json")
LOCAL_BASE = Path("/mnt/d/SacredSpace_OS")
RCLONE_REMOTE = "gdrive:SacredSpace_OS_CLOUD"


def load_routing() -> list[dict]:
    data = json.loads(ROUTING_PATH.read_text())
    return data.get("notebooks", [])


def list_notebook_sources():
    notebooks = load_routing()
    print(f"{'Notebook':<25} {'Source Path':<45} {'Auto-Sync':<12} {'Manual':<10}")
    print("-" * 92)
    for nb in notebooks:
        print(f"{nb['name']:<25} {nb['source_path']:<45} {str(nb.get('drive_auto_sync', False)):<12} {str(nb.get('manual_push_only', False)):<10}")


def check_source_exists(source_path: str) -> bool:
    # source_path from config includes SacredSpace_OS_CLOUD/ prefix
    # RCLONE_REMOTE already has the gdrive:SacredSpace_OS_CLOUD part
    rel = source_path.replace("SacredSpace_OS_CLOUD/", "", 1) if source_path.startswith("SacredSpace_OS_CLOUD/") else source_path
    full_path = f"{RCLONE_REMOTE}/{rel}"
    result = subprocess.run(
        ["rclone", "lsf", full_path],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


def verify_all_sources():
    notebooks = load_routing()
    all_ok = True
    print("Verifying NotebookLM source paths in Drive...")
    print()
    for nb in notebooks:
        path = nb["source_path"]
        exists = check_source_exists(path)
        status = "OK" if exists else "MISSING"
        if not exists:
            all_ok = False
        print(f"  [{status}] {nb['name']:<20} → {path}")
    print()
    if all_ok:
        print("All 8 notebook sources verified.")
    else:
        print("Some sources missing. Check paths above.")
    return all_ok


def verify_local_mirror():
    notebooks = load_routing()
    all_ok = True
    print("Verifying local mirror for each notebook source...")
    print()
    for nb in notebooks:
        cloud_path = nb["source_path"]
        rel_path = cloud_path.replace("SacredSpace_OS_CLOUD/", "")
        local_dir = LOCAL_BASE / rel_path
        status = "OK" if local_dir.exists() else "MISSING"
        if not local_dir.exists():
            all_ok = False
        file_count = len(list(local_dir.rglob("*"))) if local_dir.exists() else 0
        print(f"  [{status}] {nb['name']:<20} → local: {rel_path} ({file_count} items)")
    print()
    if all_ok:
        print("All notebook sources mirrored locally.")
    else:
        print("Some local mirrors missing.")
    return all_ok


def audit_key_documents():
    notebooks = load_routing()
    print("Key document audit:")
    print()
    for nb in notebooks:
        docs = nb.get("key_documents", [])
        cloud_path = nb["source_path"]
        rel_path = cloud_path.replace("SacredSpace_OS_CLOUD/", "")
        local_dir = LOCAL_BASE / rel_path
        if not local_dir.exists():
            print(f"  {nb['name']}: local dir missing, skipping")
            continue
        found = 0
        for doc in docs:
            matches = list(local_dir.rglob(f"*{doc}*"))
            if matches:
                found += 1
        print(f"  {nb['name']:<20} {found}/{len(docs)} key documents found")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list":
            list_notebook_sources()
        elif command == "verify":
            verify_all_sources()
        elif command == "local":
            verify_local_mirror()
        elif command == "audit":
            audit_key_documents()
        elif command == "all":
            list_notebook_sources()
            print()
            verify_all_sources()
            print()
            verify_local_mirror()
            print()
            audit_key_documents()
        else:
            print("Commands: list, verify, local, audit, all")
    else:
        list_notebook_sources()
