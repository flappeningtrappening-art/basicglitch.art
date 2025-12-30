#!/usr/bin/env python3
import os
import sys
from datetime import datetime

# Set your notes directory
NOTES_DIR = os.path.expanduser("~/monetization/basic-glitch-art/notes")

CATEGORIES = {
    'ai': 'ai-prompts',
    'code': 'python',
    'mon': 'monetization',
    'art': 'art-tips'
}

def capture_note():
    if len(sys.argv) < 3:
        print("Usage: note <category> <title>")
        print("Categories: ai, code, mon, art")
        return

    cat_alias = sys.argv[1]
    title = sys.argv[2].replace(" ", "_")
    cat_folder = CATEGORIES.get(cat_alias, 'general')
    
    # Ensure folder exists
    target_dir = os.path.join(NOTES_DIR, cat_folder)
    os.makedirs(target_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{timestamp}_{title}.md"
    filepath = os.path.join(target_dir, filename)

    print(f"--- Capturing Note: {title} ---")
    print("Paste your content below (Ctrl+D to save):")
    content = sys.stdin.read()

    with open(filepath, 'w') as f:
        f.write(f"# {title.replace('_', ' ')}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Category: {cat_folder}\n")
        f.write("-" * 20 + "\n\n")
        f.write(content)

    print(f"\n[SUCCESS] Note saved to {cat_folder}/{filename}")

if __name__ == "__main__":
    capture_note()
