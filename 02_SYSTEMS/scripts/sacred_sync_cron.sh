#!/bin/bash
# SacredSpace OS — Standing sync cron job (D6)
# Runs rclone --once sync for all pillars
# Log: /mnt/d/SacredSpace_OS/sacred_watcher.log

WATCHER="/tmp/watcher_venv/bin/python3"
SCRIPT="/mnt/d/SacredSpace_OS/02_SYSTEMS/scripts/sacred_watcher.py"

cd /mnt/d/SacredSpace_OS && "$WATCHER" "$SCRIPT" --once 2>&1
