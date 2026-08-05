#!/bin/bash
# ═══════════════════════════════════════════════════════════╗
# ║  GOOGLE TAKEOUT RESUME — SacredSpace OS                  ║
# ║  Resume download of Google Photos Takeout (252+ GiB)     ║
# ║  Run this on WSL2 with stable internet (expect 8+ hrs)   ║
# ╚══════════════════════════════════════════════════════════╝
# Usage: bash TAKEOUT_RESUME.sh <download_url>
#   or:  bash TAKEOUT_RESUME.sh --help

set -euo pipefail

RAW_DIR="/mnt/d/SacredSpace_OS/_RAW"
LOG_FILE="/tmp/takeout_download.log"
PARSER="/mnt/d/SacredSpace_OS/google_takeout_parser.py"
MARKET_DIR="/mnt/d/SacredSpace_OS/09_SACRED_MARKET/First_Flame"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

show_help() {
    echo -e "${CYAN}GOOGLE TAKEOUT RESUME — SacredSpace OS${NC}"
    echo ""
    echo "This script resumes downloading Google Photos Takeout ZIPs."
    echo ""
    echo "Prerequisites:"
    echo "  1. Go to https://takeout.google.com/"
    echo "  2. Deselect ALL platforms EXCEPT Google Photos"
    echo "  3. Export format: .zip"
    echo "  4. Max file size: 50 GiB"
    echo "  5. Create export & wait for it to generate"
    echo "  6. Copy the download URL(s)"
    echo ""
    echo "Usage:"
    echo "  bash TAKEOUT_RESUME.sh <download_url>      # Download a single takeout ZIP"
    echo "  bash TAKEOUT_RESUME.sh batch               # If you have multiple URLs in a file"
    echo "  bash TAKEOUT_RESUME.sh parse               # Parse downloaded ZIPs into pillars"
    echo "  bash TAKEOUT_RESUME.sh status              # Check what ZIPs are downloaded"
    echo ""
    echo "Steps after download:"
    echo "  bash TAKEOUT_RESUME.sh parse               # Run the parser on all downloaded ZIPs"
    echo "  Then check IMAGE_CATALOG.md for art bank inventory"
}

check_deps() {
    local missing=0
    for cmd in curl wget python3; do
        if ! command -v "$cmd" &>/dev/null; then
            echo -e "${RED}Missing: $cmd${NC}"
            missing=1
        fi
    done
    if [ "$missing" = "1" ]; then
        echo "Install missing dependencies and retry."
        exit 1
    fi
}

show_status() {
    echo -e "${CYAN}📦 Takeout Download Status${NC}"
    echo ""
    
    local total_parts=7
    local downloaded=0
    
    for f in "$RAW_DIR"/takeout-*-*.zip*; do
        if [ -f "$f" ]; then
            local size=$(du -h "$f" 2>/dev/null | cut -f1)
            local name=$(basename "$f")
            if [[ "$f" == *.partial ]]; then
                echo -e "  ${YELLOW}⏳${NC} $name (${size} — PARTIAL)"
            else
                echo -e "  ${GREEN}✅${NC} $name (${size})"
                downloaded=$((downloaded + 1))
            fi
        fi
    done
    
    echo ""
    echo -e "  ${downloaded}/${total_parts} complete"
}

do_download() {
    local url="$1"
    local filename="takeout-batch-$(date +%Y%m%d-%H%M%S).zip"
    
    echo -e "${CYAN}📥 Downloading: ${NC}$filename"
    echo -e "${YELLOW}   Log: ${NC}$LOG_FILE"
    echo -e "${YELLOW}   Destination: ${NC}$RAW_DIR/"
    echo ""
    echo -e "${RED}⚠️  This download is ~50 GiB and may take 2-8 hours.${NC}"
    echo -e "${RED}   Ensure stable internet connection.${NC}"
    echo ""
    
    # Download with resume support
    wget -c "$url" \
        -O "$RAW_DIR/$filename" \
        --progress=dot:giga \
        2>&1 | tee -a "$LOG_FILE"
    
    echo -e "${GREEN}✅ Download complete:${NC} $RAW_DIR/$filename"
    
    # Pulse notification
    curl -s -X POST http://localhost:8890/publish \
        -H "Content-Type: application/json" \
        -d "{
            \"source\": \"takeout_resume\",
            \"topic\": \"market.product_researched\",
            \"payload\": {
                \"action\": \"takeout_downloaded\",
                \"filename\": \"$filename\",
                \"size_gb\": \"$(du -h $RAW_DIR/$filename | cut -f1)\"
            }
        }" 2>/dev/null || true
}

do_parse() {
    echo -e "${CYAN}🔍 Parsing downloaded takeout ZIPs...${NC}"
    
    for zip in "$RAW_DIR"/takeout-*.zip; do
        if [ -f "$zip" ] && [[ "$zip" != *.partial ]]; then
            echo -e "  Parsing: $(basename "$zip")"
            python3 "$PARSER" \
                --zip "$zip" \
                --output "/mnt/d/SacredSpace_OS" \
                2>&1 | tee -a "$LOG_FILE"
        fi
    done
    
    echo -e "${GREEN}✅ Parse complete! Check output at /mnt/d/SacredSpace_OS/ for extracted images.${NC}"
    
    # Count extracted images
    local img_count=$(find /mnt/d/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/CREATION_LAB/IMAGE_ARCHIVE/ -type f \( -iname "*.png" -o -iname "*.jpg" \) 2>/dev/null | wc -l)
    echo -e "  Total images now: ${CYAN}$img_count${NC}"
}

# ── Main ──
check_deps

case "${1:-help}" in
    --help|-h|help)
        show_help
        ;;
    status)
        show_status
        ;;
    parse)
        do_parse
        ;;
    batch)
        echo "Batch mode: reading URLs from stdin (one per line)"
        echo "Paste URLs, then Ctrl+D:"
        while read -r url; do
            [ -z "$url" ] && continue
            do_download "$url"
        done
        ;;
    *)
        do_download "$1"
        ;;
esac
