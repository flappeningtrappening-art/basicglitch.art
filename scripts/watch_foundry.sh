#!/bin/bash

# ========================================================
# FOUNDRY WATCHER
# ========================================================
# Runs in background, detects changes in shared drive.
# ========================================================

WATCH_DIR="/media/sf_minty_windows/foundry_transfer/raw"
SCRIPT_PATH="/home/blitz/monetization/basic-glitch-art/scripts/ingest_art.py"

echo "--- FOUNDRY WATCHER ACTIVE ---"
echo "Monitoring: $WATCH_DIR"

while true; do
    # Check if directory exists
    if [ -d "$WATCH_DIR" ]; then
        # Check if directory is not empty
        if [ "$(ls -A $WATCH_DIR)" ]; then
            echo "[SIGNAL DETECTED] New art detected in shared folder."
            python3 "$SCRIPT_PATH"
        fi
    fi
    sleep 30 # Check every 30 seconds
done
