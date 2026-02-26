import json
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
THUMB_DIR = os.path.join(BASE_DIR, 'assets/images/gallery-thumbs')
RAW_DIR = os.path.join(BASE_DIR, 'assets/images/raw')

if not os.path.exists(THUMB_DIR):
    os.makedirs(THUMB_DIR)

with open(GALLERY_JSON, 'r') as f:
    gallery = json.load(f)

print(f"Checking thumbnails for {len(gallery)} items...")

for item in gallery:
    thumb_path = os.path.join(THUMB_DIR, f"{item['id']}.jpg")
    
    if not os.path.exists(thumb_path):
        # Find the raw source (prefer .png if it exists, otherwise use .webp or .jpg)
        # Note: 'file' in JSON is usually the webp path
        webp_path = os.path.join(BASE_DIR, item['file'])
        png_path = webp_path.rsplit('.', 1)[0] + ".png"
        jpg_path = webp_path.rsplit('.', 1)[0] + ".jpg"
        
        source = None
        if os.path.exists(png_path):
            source = png_path
        elif os.path.exists(jpg_path):
            source = jpg_path
        elif os.path.exists(webp_path):
            source = webp_path
            
        if source:
            print(f"Generating thumbnail for {item['title']} -> {item['id']}.jpg")
            # Generate 600x600 centered crop thumbnail
            cmd = f"convert '{source}' -resize 600x600^ -gravity center -extent 600x600 '{thumb_path}'"
            subprocess.run(cmd, shell=True)
        else:
            print(f"Warning: Source not found for {item['title']} ({item['file']})")

print("Thumbnail sync complete.")
