import os
import json
import shutil
import re
import datetime
import csv
import google.generativeai as genai
from dotenv import load_dotenv

# ========================================================
# FOUNDRY INGESTION ENGINE (V3.1 - SELECTIVE SCAN)
# ========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_TRANSFER = "/media/sf_minty_windows"
LOCAL_RAW = os.path.join(BASE_DIR, "assets/images/raw")
GALLERY_JSON = os.path.join(BASE_DIR, "assets/data/gallery.json")
MARKET_CSV = os.path.join(BASE_DIR, "assets/data/pod_market_master.csv")
THUMB_DIR = os.path.join(BASE_DIR, "assets/images/gallery-thumbs")

def generate_market_metadata(title):
    print(f"Generating POD Market Data for: {title}...")
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    You are a POD (Print on Demand) Marketing Expert for 'BasicGlitch'.
    Create metadata for a new art piece titled '{title}'.
    
    Aesthetic: Cyber-Eclectic, Tech-Noir, Neon, PCB design.
    
    Return ONLY a JSON object with these keys:
    - short_desc: A punchy 2-sentence marketing description.
    - tags: 15-20 highly relevant SEO tags (comma separated).
    - search_title: An SEO-optimized title for Redbubble/Society6.
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        return {
            "short_desc": f"Exclusive digital surrealism from the BasicGlitch foundry. {title} signal captured.",
            "tags": "cyberpunk, tech-noir, neon, digital art, surrealism, pcb, circuitry, robot, basicglitch",
            "search_title": f"{title} | Cyberpunk Neon Glitch Art"
        }

def update_market_csv(title, metadata, image_path):
    file_exists = os.path.isfile(MARKET_CSV)
    with open(MARKET_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Original Title', 'Market Title', 'Description', 'Tags', 'Local File'])
        writer.writerow([title, metadata['search_title'], metadata['short_desc'], metadata['tags'], image_path])

def generate_forensic_analysis(title):
    print(f"Generating forensic analysis for: {title}...")
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    You are a forensic art critic for 'BasicGlitch'. 
    Write a 300-word forensic analysis of a new piece titled '{title}'.
    
    Requirements:
    1. EXACTLY 300 words or more.
    2. Tone: Aggressive, technical, professional, and surreal.
    3. Use terms like: 'digital entropy', 'forensic marker', 'quantum superposition', 'cyber-eclectic', 'tech-noir', 'visual autopsy'.
    4. Focus on the 'Foundry' philosophy: processing raw chaos into high-fidelity artistic intelligence.
    5. IMPORTANT: Occasionally hide a 'Forensic Fragment' in the text (e.g., [FRAGMENT: SIGNAL_77] or [FRAGMENT: DECAY_0]). These are for the ARG.
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

    # ONLY scan specific folders to avoid root clutter
    scan_paths = [
        os.path.join(SHARED_TRANSFER, "savannah-grid"),
        os.path.join(SHARED_TRANSFER, "transfer2website")
    ]
    
    new_art_found = False
    
    for scan_path in scan_paths:
        if not os.path.exists(scan_path):
            print(f"Skipping missing path: {scan_path}")
            continue
            
        print(f"Scanning: {scan_path}")
        for filename in os.listdir(scan_path):
            file_full_path = os.path.join(scan_path, filename)
            
            # Skip directories
            if not os.path.isfile(file_full_path):
                continue
                
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                print(f"Detected new signal: {filename}")
                
                # Check if it already exists locally to avoid duplicates
                local_path = os.path.join(LOCAL_RAW, filename)
                if os.path.exists(local_path):
                    print(f"Skipping duplicate: {filename}")
                    continue

                # 1. Move to local raw
                shutil.move(file_full_path, local_path)
                
                # 1b. Create WebP version for high performance
                webp_filename = filename.rsplit('.', 1)[0] + ".webp"
                webp_path = os.path.join(LOCAL_RAW, webp_filename)
                print(f"Optimizing vision for web: {webp_filename}")
                os.system(f"convert '{local_path}' -quality 85 '{webp_path}'")
                
                # 2. Extract Title
                title = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title()
                art_id = f"art-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # 2b. Generate Thumbnail (600x600 centered)
                thumb_path = os.path.join(THUMB_DIR, f"{art_id}.jpg")
                print(f"Generating gallery thumbnail: {art_id}.jpg")
                os.system(f"convert '{local_path}' -resize 600x600^ -gravity center -extent 600x600 '{thumb_path}'")
                
                # 3. AI Analysis (300 Words)
                analysis = generate_forensic_analysis(title)
                
                # 3b. Generate POD Market Data
                market_data = generate_market_metadata(title)
                update_market_csv(title, market_data, f"assets/images/raw/{filename}")
                
                # 4. Update Gallery JSON (Use WebP for the website)
                update_gallery(art_id, title, f"assets/images/raw/{webp_filename}", analysis)
                new_art_found = True

    if new_art_found:
        print("Regenerating site and syncing mainframe...")
        os.system(f"python3 {os.path.join(BASE_DIR, 'scripts/foundry_site_gen.py')}")
        deploy_to_github()

def update_gallery(id, title, file_path, analysis):
    with open(GALLERY_JSON, 'r') as f:
        gallery = json.load(f)
    
    new_item = {
        "id": id,
        "title": title,
        "file": file_path,
        "categories": ["New Arrivals"],
        "styles": ["Cyber-Eclectic"],
        "date": datetime.date.today().isoformat(),
        "forensic_analysis": analysis,
        "description": f"New forensic entry: {title}. Deep signal analysis complete.",
        "alt_text": f"{title} - digital surrealism by BasicGlitch",
        "seo_keywords": ["new digital art", "basicglitch", "forensic art"]
    }
    
    gallery.insert(0, new_item)
    
    with open(GALLERY_JSON, 'w') as f:
        json.dump(gallery, f, indent=2)
    print(f"Registry Updated: {title}")

def deploy_to_github():
    os.chdir(BASE_DIR)
    os.system("git add .")
    os.system(f"git commit -m 'feat: automated forensic ingestion of {datetime.datetime.now().isoformat()}'")
    os.system("git push origin main")
    print("Deployment Synchronized.")

if __name__ == "__main__":
    process_new_files()
