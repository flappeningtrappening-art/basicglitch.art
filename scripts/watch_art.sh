#!/bin/bash

# Folder to watch (Shared folder from Windows)
# Confirmed path: /media/sf_minty_windows
WATCH_DIR="/media/sf_minty_windows"
SCRIPT_PATH="$HOME/monetization/basic-glitch-art/scripts/process_art.py"

echo "--- BasicGlitch: Monitoring $WATCH_DIR ---"
echo "Waiting for Krita exports..."

# Monitor for new files or modified files being closed
# Added -q (quiet) to reduce log noise
inotifywait -m -e close_write --format "%f" "$WATCH_DIR" |
while read FILENAME
do
    # Only process image files
    if [[ $FILENAME =~ \.(png|jpg|jpeg)$ ]]; then
        echo "Detected: $FILENAME"
        
        # 1. Robustness: Wait for file write to fully settle
        sleep 2
        
        # 2. Check if file still exists (wasn't a temp file)
        if [ -f "$WATCH_DIR/$FILENAME" ]; then
             echo "Processing $FILENAME..."
             # Run the processor
             python3 "$SCRIPT_PATH" "$WATCH_DIR/$FILENAME"
        fi
    fi
done