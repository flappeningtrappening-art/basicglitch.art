#!/bin/bash

# Configuration
SOURCE_DIR="$HOME/monetization/basic-glitch-art"
BACKUP_DEST="/media/sf_minty_windows/backups"
DATE=$(date +%Y-%m-%d_%H-%M)
FILENAME="basicglitch_backup_$DATE.tar.gz"

# Ensure backup directory exists on the host
mkdir -p "$BACKUP_DEST"

echo "--- Basic Glitch Backup System ---"
echo "Targeting: $BACKUP_DEST/$FILENAME"

# Create the compressed backup
# Excluding .git folder to keep size small (since it's already on GitHub)
tar -czf "$BACKUP_DEST/$FILENAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")" --exclude='.git'

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Backup created successfully!"
    # List backups and show size
    ls -lh "$BACKUP_DEST/$FILENAME"
else
    echo "[ERROR] Backup failed. Check if shared folder is accessible."
fi
