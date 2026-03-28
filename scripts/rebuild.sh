#!/bin/bash
# rebuild.sh — full pipeline: extract pages then build flipbook
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."

cd "$ROOT"

echo "=== Step 1: Extract pages ==="
python3 scripts/extract_pages.py "$@"

echo ""
echo "=== Step 2: Build flipbook ==="
python3 scripts/build_flipbook.py

echo ""
echo "=== Done ==="
echo "Open: output/extra_cheese_flipbook.html"
