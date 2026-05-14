#!/bin/bash
FASTAPI_DIR="/mnt/d/SacredSpace_OS/systems/fastapi"
VAULT="/mnt/d/01_VAULT/SacredSpace_Vault"
echo "[SACRED OS] Killing port 8888..."
fuser -k 8888/tcp 2>/dev/null
sleep 1
echo "[SACRED OS] Clearing cache..."
rm -rf "$FASTAPI_DIR/__pycache__"
echo "[SACRED OS] Starting..."
cd "$FASTAPI_DIR" && SACREDSPACE_VAULT="$VAULT" OLLAMA_HOST="http://192.168.240.1:11434" python3 main.py
