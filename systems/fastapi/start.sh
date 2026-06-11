#!/bin/bash
# SacredSpace OS — FastAPI Spine start script
# Usage: ./start.sh [--bg]

SPINE_DIR="/mnt/d/SacredSpace_OS/systems/fastapi"
cd "$SPINE_DIR" || { echo "ERROR: Cannot cd to $SPINE_DIR"; exit 1; }

export SACRED_ROOT="/mnt/d/SacredSpace_OS"
# Ollama runs on Windows host — detect WSL2 gateway IP
OLLAMA_GW=$(grep nameserver /etc/resolv.conf | awk '{print $2}' | head -1)
export OLLAMA_BASE="http://${OLLAMA_GW}:11434"
export PYTHONPATH="$SPINE_DIR:$PYTHONPATH"

if [ "$1" = "--bg" ]; then
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8888 > /tmp/sacredspace_api.log 2>&1 &
    echo "SacredSpace FastAPI started in background (PID: $!)"
    echo "Log: /tmp/sacredspace_api.log"
else
    uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
fi
