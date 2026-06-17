import json
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime, timezone
from fnmatch import fnmatch

CONFIG_PATH = Path("/mnt/d/SacredSpace_OS/02_SYSTEMS/CONFIGS/sacred_watcher_config.json")
LOCAL_BASE = Path("/mnt/d/SacredSpace_OS")
RCLONE_REMOTE = "gdrive:SacredSpace_OS_CLOUD"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text()) if CONFIG_PATH.exists() else {}


def log_event(log_path: str, entry: str):
    log_file = LOCAL_BASE / log_path
    timestamp = datetime.now(timezone.utc).isoformat()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {entry}\n")


def get_mission_tags(config: dict) -> list[str]:
    state_path = config.get("mission_state_path", "")
    state_file = Path(state_path)
    if state_file.exists():
        try:
            return json.loads(state_file.read_text()).get("context_tags", [])
        except Exception as e:
            log_event(config.get("main_log", "sacred_watcher.log"), f"Error reading mission state: {e}")
            return []
    return []


def is_never_ingest(filepath: str, config: dict) -> bool:
    patterns = config.get("never_ingest", [])
    return any(fnmatch(filepath, p) for p in patterns)


def is_locked(filepath: str, config: dict) -> bool:
    lock_str = config.get("lock_protocol", {}).get("locked_status_string", "Status: LOCKED")
    scan_lines = config.get("lock_protocol", {}).get("header_scan_lines", 10)
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            head = [next(f) for _ in range(scan_lines)]
        return any(lock_str in line for line in head)
    except (StopIteration, IOError):
        return False


def _log_security(filepath: str, config: dict):
    log_event(config.get("security_log", "watcher_security.log"), f"BLOCKED: {filepath}")


def _log_locked(filepath: str, config: dict):
    queue_file = config.get("lock_protocol", {}).get("locked_queue_file", "watcher_locked_queue.json")
    queue_path = LOCAL_BASE / queue_file
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = json.dumps({"file": filepath, "locked_at": timestamp}) + "\n"
    with open(queue_path, "a") as f:
        f.write(entry)


def should_ingest(filepath: str, config: dict) -> bool:
    if is_never_ingest(filepath, config):
        _log_security(filepath, config)
        return False
    if is_locked(filepath, config):
        _log_locked(filepath, config)
        return False
    ingest_logic = config.get("ingest_logic", "intersection_nonempty")
    open_ingestion = config.get("open_ingestion_when_no_mission", True)
    mission_tags = get_mission_tags(config)
    if not mission_tags and open_ingestion:
        return True
    if ingest_logic == "intersection_nonempty":
        file_tags = []
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.startswith("X-Tags:"):
                        file_tags = [t.strip() for t in line[7:].split(",")]
                        break
        except IOError:
            pass
        if not file_tags and not open_ingestion:
            return False
        return bool(set(file_tags) & set(mission_tags)) if file_tags else open_ingestion
    return True


def resolve_conflict(local_path: Path, remote_path: str, config: dict) -> str:
    conflict_rules = config.get("conflict_mode", {})
    path_str = str(local_path)
    if any(k in path_str for k in ["04_SACRED_CODEX", "CANON"]):
        mode = conflict_rules.get("canon_files", "local_wins")
    elif "DISTILLED" in path_str:
        mode = conflict_rules.get("distilled_files", "local_wins")
    elif "GEMINI" in path_str.upper():
        mode = conflict_rules.get("gemini_authored_files", "drive_wins_pending_review")
    elif "STORYLINE" in path_str or "CREATION_LAB" in path_str:
        mode = conflict_rules.get("draft_active_files", "timestamp_wins")
    else:
        mode = conflict_rules.get("untagged_files", "flag_to_pending_review")
    return mode


def sync_pillar(pillar_id: str, config: dict):
    local_path = Path(config["pillar_paths"][pillar_id])
    cloud_path = f"gdrive:{config['cloud_pillar_paths'][pillar_id]}"
    log_path = config.get("main_log", "sacred_watcher.log")
    if not local_path.exists():
        local_path.mkdir(parents=True)
    log_event(log_path, f"SYNC START: {pillar_id}")
    result = subprocess.run(
        ["rclone", "copy", cloud_path, str(local_path), "--progress"],
        capture_output=True, text=True, timeout=600
    )
    if result.returncode == 0:
        log_event(log_path, f"SYNC OK: {pillar_id}")
    else:
        log_event(log_path, f"SYNC FAIL: {pillar_id} - {result.stderr[:200]}")
    pending = resolve_pending_reviews(pillar_id, config)
    if pending:
        log_event(log_path, f"PENDING: {pillar_id} - {pending} file(s) flagged")
    return result.returncode == 0


def resolve_pending_reviews(pillar_id: str, config: dict) -> int:
    pending_dir = LOCAL_BASE / "_PENDING_REVIEW"
    if not pending_dir.exists():
        return 0
    count = 0
    conflict_log = config.get("conflict_mode", {}).get("conflict_log", "watcher_conflicts.log")
    for item in pending_dir.rglob("*"):
        if item.is_file():
            log_event(conflict_log, f"PENDING: {item.relative_to(LOCAL_BASE)} - awaiting review")
            count += 1
    return count


def check_locked_queue(config: dict):
    queue_file = config.get("lock_protocol", {}).get("locked_queue_file", "watcher_locked_queue.json")
    queue_path = LOCAL_BASE / queue_file
    if not queue_path.exists():
        return
    retry_minutes = config.get("lock_protocol", {}).get("retry_interval_minutes", 15)
    now = datetime.now(timezone.utc)
    new_queue = []
    with open(queue_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            locked_at = datetime.fromisoformat(entry["locked_at"])
            if (now - locked_at).total_seconds() / 60 >= retry_minutes:
                if not is_locked(entry["file"], config):
                    log_event(config.get("main_log", "sacred_watcher.log"), f"LOCK RELEASED: {entry['file']}")
                    continue
            new_queue.append(line)
    with open(queue_path, "w") as f:
        f.writelines(new_queue)


def run_watch_cycle(config: dict):
    log_path = config.get("main_log", "sacred_watcher.log")
    log_event(log_path, "--- Watch cycle start ---")
    for pillar_id in sorted(config.get("pillar_paths", {}).keys()):
        sync_pillar(pillar_id, config)
    check_locked_queue(config)
    log_event(log_path, "--- Watch cycle end ---")


if __name__ == "__main__":
    config = load_config()
    if not config:
        print("ERROR: Config not found at", CONFIG_PATH)
        exit(1)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        run_watch_cycle(config)
    elif len(sys.argv) > 1 and sys.argv[1] == "--pillar":
        pillar = sys.argv[2]
        if pillar in config.get("pillar_paths", {}):
            sync_pillar(pillar, config)
        else:
            print(f"Unknown pillar: {pillar}")
            exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        filepath = sys.argv[2]
        result = should_ingest(filepath, config)
        print(f"should_ingest({filepath}): {result}")
    else:
        interval = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
        log_event(config.get("main_log", "sacred_watcher.log"), f"Watcher started (interval={interval}s)")
        while True:
            run_watch_cycle(config)
            time.sleep(interval)
