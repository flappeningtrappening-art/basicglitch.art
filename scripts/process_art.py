#!/usr/bin/env python3
import os
import json
import shutil
from PIL import Image
from datetime import datetime

# Paths
BASE_DIR = os.path.expanduser("~/monetization/basic-glitch-art")
RAW_DIR = os.path.join(BASE_DIR, "assets/images/raw")
THUMB_DIR = os.path.join(BASE_DIR, "assets/images/gallery-thumbs")
JSON_FILE = os.path.join(BASE_DIR, "assets/data/gallery.json")

def process_art():
    print("--- Basic Glitch Art Processor ---")
    input_path = input("Drag and drop the new image file here (or type path): ").strip().replace("'", "")
    
    if not os.path.exists(input_path):
        print(f"[ERROR] File not found: {input_path}")
        return

    # 1. Get info from user
    title = input("Enter Title: ")
    description = input("Enter Description: ")
    price = input("Enter Price (leave blank for none): ")
    styles_input = input("Enter Styles (comma separated, e.g. Neon, Surrealism): ")
    styles = [s.strip() for s in styles_input.split(",")]
    
    # 2. Generate unique ID and Filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ext = os.path.splitext(input_path)[1]
    filename = f"{title.lower().replace(' ', '_')}_{timestamp}{ext}"
    target_raw_path = os.path.join(RAW_DIR, filename)
    
    # 3. Copy to Raw directory
    shutil.copy(input_path, target_raw_path)
    print(f"[1/3] Copied to assets/images/raw/{filename}")

    # 4. Create Thumbnail
    try:
        with Image.open(input_path) as img:
            # Generate ID based on filename for thumbnail
            art_id = f"art-{timestamp}"
            thumb_filename = f"{art_id}.jpg"
            thumb_path = os.path.join(THUMB_DIR, thumb_filename)
            
            # Maintain aspect ratio, max width 600
            img.thumbnail((600, 600))
            # Convert to RGB if needed (for JPG save)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(thumb_path, "JPEG", quality=85)
            print(f"[2/3] Created thumbnail: assets/images/gallery-thumbs/{thumb_filename}")
    except Exception as e:
        print(f"[ERROR] Failed to create thumbnail: {e}")
        return

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
            new_entry["price"] = int(price)

        gallery_data.insert(0, new_entry) # Add to start of list

        with open(JSON_FILE, 'w') as f:
            json.dump(gallery_data, f, indent=2)
        print(f"[3/3] Updated gallery.json")

    except Exception as e:
        print(f"[ERROR] Failed to update JSON: {e}")
        return

    print(f"\n[SUCCESS] '{title}' is now live locally! Just have Gemini push the changes.")

if __name__ == "__main__":
    process_art()
