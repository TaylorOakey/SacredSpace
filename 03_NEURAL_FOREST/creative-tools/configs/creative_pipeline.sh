#!/bin/bash
# 🎭 Sacred Creation Loop (SCRL) — Creative Pipeline Startup
# Source this to activate the full creative toolchain
# SacredSpace OS — 2026-07-02

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREATIVE_ENV="/mnt/c/03_NEURAL_FOREST/creative-env"
TOOLS_DIR="/mnt/d/SacredSpace_OS/03_NEURAL_FOREST/creative-tools"
OUTPUT_DIR="/mnt/d/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/creative-output"

echo "╔══════════════════════════════════════════╗"
echo "║  🎭 SACRED CREATION LOOP — INIT          ║"
echo "╚══════════════════════════════════════════╝"

# Phase 1: Activate Python creative environment
echo ""
echo "[1/4] 🔮 Activating creative environment..."
if [ -f "$CREATIVE_ENV/bin/activate" ]; then
    source "$CREATIVE_ENV/bin/activate"
    echo "  ✅ Env activated: $CREATIVE_ENV"
else
    echo "  ⚠️  Not found at $CREATIVE_ENV — creating..."
    python3 -m venv "$CREATIVE_ENV"
    source "$CREATIVE_ENV/bin/activate"
    echo "  ✅ Created and activated"
fi

# Verify installed MCP servers
echo ""
echo "[2/4] 📦 Checking MCP tools..."
for pkg in storytelling-mcp osp-marketing-tools mcp; do
    if pip show "$pkg" &>/dev/null 2>&1; then
        echo "  ✅ $pkg"
    else
        echo "  ⚠️  $pkg not found"
    fi
done

# Verify D: drive tool repos
echo ""
echo "[3/4] 📂 Checking D: drive tool repos..."
for repo in kimi-writer-mcp inkos; do
    if [ -d "$TOOLS_DIR/mcp-servers/$repo" ]; then
        echo "  ✅ $repo"
    else
        echo "  ⚠️  $repo not found"
    fi
done

# Check output dirs
echo ""
echo "[4/4] 🖼️  Checking creative output directories..."
for dir in stories art music worlds; do
    if [ -d "$OUTPUT_DIR/$dir" ]; then
        echo "  ✅ $dir"
    else
        mkdir -p "$OUTPUT_DIR/$dir"
        echo "  ➕ Created $dir"
    fi
done

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  🎭 SCRL READY — Let the creation begin  ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Available commands:"
echo "  storytelling-mcp — 16 narrative tools (in creative-env)"
echo "  osp-writer      — Marketing/writing MCP (in creative-env)"
echo "  kimi-writer     — EPUB/PDF generation (D: drive)"
echo ""
echo "SCRL Workflow:"
echo "  1. Orientation  → muse mote from KAIROS patterns"
echo "  2. Conception   → GR∆M∆ cipher + worldbuilding"
echo "  3. Generation   → storytelling-mcp → draft"
echo "  4. Review       → ASHER + Arcanum feedback"
echo "  5. Publication  → IRIS → platform distribution"
echo ""
echo "In lakesh alakin."
