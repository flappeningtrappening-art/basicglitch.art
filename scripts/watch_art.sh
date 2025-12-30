#!/bin/bash

# Folder to watch (Shared folder from Windows)
WATCH_DIR="/media/sf_minty_windows"
SCRIPT_PATH="$HOME/monetization/basic-glitch-art/scripts/process_art.py"

echo "--- Basic Glitch: Monitoring $WATCH_DIR ---"
echo "Waiting for Krita exports..."

# Monitor for new files or modified files being closed
inotifywait -m -e close_write --format "%f" "$WATCH_DIR" |
while read FILENAME
do
    # Only process image files
    if [[ $FILENAME =~ \.(png|jpg|jpeg)$ ]]; then
        echo "New art detected: $FILENAME"
        # Run the processor
        python3 "$SCRIPT_PATH" "$WATCH_DIR/$FILENAME"
    fi
done
