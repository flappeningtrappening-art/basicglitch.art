import json
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
THUMB_DIR = os.path.join(BASE_DIR, 'assets/images/gallery-thumbs')

if not os.path.exists(THUMB_DIR):
    os.makedirs(THUMB_DIR)

with open(GALLERY_JSON, 'r') as f:
    gallery = json.load(f)

for item in gallery:
    thumb_path = os.path.join(THUMB_DIR, f"{item['id']}.jpg")
    if not os.path.exists(thumb_path):
        source = os.path.join(BASE_DIR, item['file'])
        if os.path.exists(source):
            print(f"Generating thumbnail: {item['id']}.jpg")
            # Use ffmpeg for 600x600 centered crop
            cmd = f"ffmpeg -i '{source}' -vf 'scale=600:600:force_original_aspect_ratio=increase,crop=600:600' -y -hide_banner -loglevel error '{thumb_path}'"
            subprocess.run(cmd, shell=True)
        else:
            print(f"Source missing: {source}")
