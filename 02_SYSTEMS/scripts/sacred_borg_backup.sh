#!/bin/bash
# SacredSpace OS — Borg dedup backup (hourly canon snapshots)
# Usage: bash sacred_borg_backup.sh
# Retention: 30 days

SACRED_ROOT="/mnt/d/SacredSpace_OS"
BORG_REPO="$SACRED_ROOT/05_MEMORY_ENGINE/borg_repo"
BORG_PASSFILE="/tmp/borg_passphrase.txt"
LOG_FILE="$SACRED_ROOT/02_SYSTEMS/logs/borg_backup.log"

export BORG_PASSPHRASE=$(cat "$BORG_PASSFILE" 2>/dev/null || echo "")
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⟡ Borg backup start" >> "$LOG_FILE"

# Create backup of canon directories (04_SACRED_CODEX, 01_OBSIDIAN_VAULTS, 05_MEMORY_ENGINE, configs)
borg create \
    --verbose \
    --stats \
    --compression lz4 \
    --exclude '**/__pycache__' \
    --exclude '**/.git' \
    --exclude '**/node_modules' \
    --exclude '**/.venv' \
    --exclude '**/chroma_db' \
    --exclude '**/borg_repo' \
    "$BORG_REPO::sacredspace-{now:%Y-%m-%d_%H%M%S}" \
    "$SACRED_ROOT/01_OBSIDIAN_VAULTS" \
    "$SACRED_ROOT/04_SACRED_CODEX" \
    "$SACRED_ROOT/05_MEMORY_ENGINE" \
    "$SACRED_ROOT/systems/fastapi" \
    "$SACRED_ROOT/02_SYSTEMS/scripts" \
    "$SACRED_ROOT/02_SYSTEMS/CONFIGS" \
    2>&1 | tail -3 >> "$LOG_FILE"

# Prune: keep 30 daily snapshots
borg prune \
    --verbose \
    --list \
    --keep-daily 30 \
    "$BORG_REPO" \
    2>&1 | tail -5 >> "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⟡ Borg backup complete" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
