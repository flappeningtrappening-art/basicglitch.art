import os
import json
import shutil
import re
import datetime
import csv
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# ========================================================
# FOUNDRY INGESTION ENGINE (V3.2 - MOTION SUPPORT)
# ========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_TRANSFER = "/media/sf_minty_windows"
LOCAL_RAW = os.path.join(BASE_DIR, "assets/images/raw")
LOCAL_VIDEOS = os.path.join(BASE_DIR, "assets/videos")
GALLERY_JSON = os.path.join(BASE_DIR, "assets/data/gallery.json")
MARKET_CSV = os.path.join(BASE_DIR, "assets/data/pod_market_master.csv")
THUMB_DIR = os.path.join(BASE_DIR, "assets/images/gallery-thumbs")

# Create missing directories
for d in [LOCAL_RAW, LOCAL_VIDEOS, THUMB_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

def generate_market_metadata(title, is_video=False):
    print(f"Generating POD Market Data for: {title}...")
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    medium = "Motion Art / Animation" if is_video else "Digital Surrealism"
    
    prompt = f"""
    You are a POD (Print on Demand) Marketing Expert for 'BasicGlitch'.
    Create metadata for a new {medium} titled '{title}'.
    
    Aesthetic: Cyber-Eclectic, Tech-Noir, Neon, PCB design.
    
    Return ONLY a JSON object with these keys:
    - short_desc: A punchy 2-sentence marketing description.
    - tags: 15-20 highly relevant SEO tags (comma separated).
    - search_title: An SEO-optimized title for Redbubble/Society6.
    """
    
    try:
        response = model.generate_content(prompt)
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        return {
            "short_desc": f"Exclusive {medium} from the BasicGlitch foundry. {title} signal captured.",
            "tags": "cyberpunk, tech-noir, neon, digital art, surrealism, pcb, circuitry, robot, basicglitch, motion art",
            "search_title": f"{title} | Cyberpunk Neon Glitch Art"
        }

def update_market_csv(title, metadata, image_path):
    file_exists = os.path.isfile(MARKET_CSV)
    with open(MARKET_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Original Title', 'Market Title', 'Description', 'Tags', 'Local File'])
        writer.writerow([title, metadata['search_title'], metadata['short_desc'], metadata['tags'], image_path])

def generate_forensic_analysis(title, is_video=False):
    print(f"Generating forensic analysis for: {title}...")
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    medium_context = "This temporal sequence" if is_video else "This visual artifact"
    
    prompt = f"""
    You are a forensic art critic for 'BasicGlitch'. 
    Write a 300-word forensic analysis of a new piece titled '{title}'.
    
    Requirements:
    1. EXACTLY 300 words or more.
    2. Tone: Aggressive, technical, professional, and surreal.
    3. Use terms like: 'digital entropy', 'forensic marker', 'quantum superposition', 'temporal decay', 'cyber-eclectic', 'tech-noir', 'visual autopsy'.
    4. {medium_context} represents a deep-signal capture from the Foundry.
    5. IMPORTANT: Occasionally hide a 'Forensic Fragment' in the text (e.g., [FRAGMENT: SIGNAL_77]).
    6. Output the analysis in HTML <p> tags.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI Analysis Failed: {e}")
        return f"<p>Forensic analysis for {title} is pending deeper scrutiny. This piece represents a significant anomaly in the digital signal.</p>"

def process_new_files():
    if not os.path.exists(SHARED_TRANSFER):
        print(f"Error: Shared folder not found at {SHARED_TRANSFER}")
        return

    scan_paths = [
        SHARED_TRANSFER,
        os.path.join(SHARED_TRANSFER, "savannah-grid"),
        os.path.join(SHARED_TRANSFER, "transfer2website")
    ]
    
    new_art_found = False
    
    for scan_path in scan_paths:
        if not os.path.exists(scan_path):
            continue
            
        print(f"Scanning: {scan_path}")
        for filename in os.listdir(scan_path):
            file_full_path = os.path.join(scan_path, filename)
            
            if not os.path.isfile(file_full_path):
                continue
                
            is_image = filename.lower().endswith((".png", ".jpg", ".jpeg"))
            is_video = filename.lower().endswith((".mp4", ".mov", ".webm"))
            
            if is_image or is_video:
                print(f"Detected new signal: {filename}")
                
                # 1. Setup paths
                dest_dir = LOCAL_VIDEOS if is_video else LOCAL_RAW
                local_path = os.path.join(dest_dir, filename)
                
                if os.path.exists(local_path):
                    print(f"Skipping duplicate: {filename}")
                    continue

                # 2. Move to local project
                shutil.move(file_full_path, local_path)
                
                # 3. Extract Metadata
                title = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title()
                art_id = f"art-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # 4. Generate Thumbnail & Web Version
                if is_image:
                    webp_filename = filename.rsplit('.', 1)[0] + ".webp"
                    webp_path = os.path.join(LOCAL_RAW, webp_filename)
                    print(f"Optimizing vision for web: {webp_filename}")
                    os.system(f"convert '{local_path}' -quality 85 '{webp_path}'")
                    
                    thumb_path = os.path.join(THUMB_DIR, f"{art_id}.jpg")
                    print(f"Generating gallery thumbnail: {art_id}.jpg")
                    os.system(f"convert '{local_path}' -resize 600x600^ -gravity center -extent 600x600 '{thumb_path}'")
                    final_file_path = f"assets/images/raw/{webp_filename}"
                
                else: # IS VIDEO
                    thumb_path = os.path.join(THUMB_DIR, f"{art_id}.jpg")
                    print(f"Extracting temporal frame for thumbnail: {art_id}.jpg")
                    # Extract frame at 1s mark
                    cmd = f"ffmpeg -i '{local_path}' -ss 00:00:01.000 -vframes 1 -q:v 2 -vf \"scale=600:600:force_original_aspect_ratio=increase,crop=600:600\" '{thumb_path}' -y"
                    subprocess.run(cmd, shell=True)
                    final_file_path = f"assets/videos/{filename}"

                # 5. AI Analysis
                analysis = generate_forensic_analysis(title, is_video)
                
                # 6. POD Market Data
                market_data = generate_market_metadata(title, is_video)
                update_market_csv(title, market_data, final_file_path)
                
                # 7. Update Gallery JSON
                update_gallery(art_id, title, final_file_path, analysis, is_video)
                new_art_found = True

    if new_art_found:
        print("Regenerating site and syncing mainframe...")
        os.system(f"python3 {os.path.join(BASE_DIR, 'scripts/foundry_site_gen.py')}")
        deploy_to_github()

def update_gallery(id, title, file_path, analysis, is_video):
    with open(GALLERY_JSON, 'r') as f:
        gallery = json.load(f)
    
    styles = ["Motion Art"] if is_video else ["Cyber-Eclectic"]
    
    new_item = {
        "id": id,
        "title": title,
        "file": file_path,
        "categories": ["New Arrivals"],
        "styles": styles,
        "type": "video" if is_video else "image",
        "date": datetime.date.today().isoformat(),
        "forensic_analysis": analysis,
        "description": f"New forensic entry: {title}. Deep signal analysis complete.",
        "alt_text": f"{title} - digital surrealism by BasicGlitch",
        "seo_keywords": ["new digital art", "basicglitch", "forensic art", "motion art" if is_video else ""]
    }
    
    gallery.insert(0, new_item)
    
    with open(GALLERY_JSON, 'w') as f:
        json.dump(gallery, f, indent=2)
    print(f"Registry Updated: {title}")

def deploy_to_github():
    os.chdir(BASE_DIR)
    os.system("git add .")
    os.system(f"git commit -m 'feat: automated forensic ingestion (motion + stills) of {datetime.datetime.now().isoformat()}'")
    os.system("git push origin main")
    print("Deployment Synchronized.")

if __name__ == "__main__":
    process_new_files()
