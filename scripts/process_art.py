#!/usr/bin/env python3
import os
import json
import shutil
import sys
import select
from PIL import Image
from datetime import datetime

# Paths
BASE_DIR = os.path.expanduser("~/monetization/basic-glitch-art")
RAW_DIR = os.path.join(BASE_DIR, "assets/images/raw")
THUMB_DIR = os.path.join(BASE_DIR, "assets/images/gallery-thumbs")
JSON_FILE = os.path.join(BASE_DIR, "assets/data/gallery.json")

def get_input_with_timeout(prompt, default_value, timeout=5):
    """
    Tries to get input from user. 
    If not interactive (background) or times out, returns default.
    """
    # Check if we have a valid TTY (terminal)
    if not sys.stdin.isatty():
        return default_value

    print(f"{prompt} [Default: {default_value}] ", end='', flush=True)
    
    # Wait for input with timeout
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        data = sys.stdin.readline().strip()
        if data:
            return data
    else:
        print(f"\n[Timeout] Using default: {default_value}")
    
    return default_value

def process_art():
    print(f"--- BasicGlitch Art Processor [{datetime.now()}] ---")
    
    # Check if path was passed as argument
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        print(f"Triggered for: {input_path}")
    else:
        print("Usage: process_art.py <path_to_image>")
        return

    if not os.path.exists(input_path):
        print(f"[ERROR] File not found: {input_path}")
        return

    # Default Metadata
    default_title = os.path.splitext(os.path.basename(input_path))[0].replace("_", " ").title()
    
    # Get Metadata (Timeout logic prevents hanging in background)
    title = get_input_with_timeout("Enter Title:", default_title)
    description = get_input_with_timeout("Enter Description:", "Neon Surrealism Piece")
    price = get_input_with_timeout("Enter Price:", "")
    styles_input = get_input_with_timeout("Styles (comma sep):", "Neon, Glitch")
    
    styles = [s.strip() for s in styles_input.split(",")]
    
    # 2. Generate unique ID and Filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ext = os.path.splitext(input_path)[1]
    clean_title = title.lower().replace(' ', '_')
    filename = f"{clean_title}_{timestamp}{ext}"
    target_raw_path = os.path.join(RAW_DIR, filename)
    
    # 3. Copy to Raw directory
    try:
        shutil.copy(input_path, target_raw_path)
        print(f"[1/3] Copied to assets/images/raw/{filename}")
    except Exception as e:
        print(f"[ERROR] Copy failed: {e}")
        return

    # 4. Create Thumbnail
    art_id = f"art-{timestamp}"
    try:
        with Image.open(input_path) as img:
            thumb_filename = f"{art_id}.jpg"
            thumb_path = os.path.join(THUMB_DIR, thumb_filename)
            
            img.thumbnail((600, 600))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(thumb_path, "JPEG", quality=85)
            print(f"[2/3] Created thumbnail: {thumb_filename}")
    except Exception as e:
        print(f"[ERROR] Thumbnail failed: {e}")
        # Proceed anyway, not fatal

    # 5. Update gallery.json
    try:
        with open(JSON_FILE, 'r') as f:
            gallery_data = json.load(f)
        
        new_entry = {
            "id": art_id,
            "title": title,
            "file": f"assets/images/raw/{filename}",
            "categories": ["Available for Purchase"],
            "styles": styles,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description
        }
        if price:
            try:
                new_entry["price"] = int(price)
            except:
                pass # Ignore bad price input

        gallery_data.insert(0, new_entry) 

        with open(JSON_FILE, 'w') as f:
            json.dump(gallery_data, f, indent=2)
        print(f"[3/3] Updated gallery.json")

    except Exception as e:
        print(f"[ERROR] JSON Update failed: {e}")
        return

    print(f"\n[SUCCESS] '{title}' is live! ID: {art_id}")

if __name__ == "__main__":
    process_art()