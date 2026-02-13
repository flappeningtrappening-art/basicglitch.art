import os
import json
import shutil
import re
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# ========================================================
# FOUNDRY INGESTION ENGINE (V2 - AI ENHANCED)
# ========================================================
# Monitors shared drive, processes new art with Gemini, and deploys.
# ========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_TRANSFER = "/media/sf_minty_windows/foundry_transfer"
LOCAL_RAW = os.path.join(BASE_DIR, "assets/images/raw")
GALLERY_JSON = os.path.join(BASE_DIR, "assets/data/gallery.json")

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
    5. Output the analysis in HTML <p> tags.
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

    raw_incoming = os.path.join(SHARED_TRANSFER, "raw")
    if not os.path.exists(raw_incoming):
        return

    new_art_found = False
    
    for filename in os.listdir(raw_incoming):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            print(f"Detected new signal: {filename}")
            
            # 1. Move to local raw
            local_path = os.path.join(LOCAL_RAW, filename)
            shutil.move(os.path.join(raw_incoming, filename), local_path)
            
            # 2. Extract Title
            title = filename.split('.')[0].replace('_', ' ').title()
            art_id = f"art-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 3. AI Analysis (300 Words)
            analysis = generate_forensic_analysis(title)
            
            # 4. Update Gallery JSON
            update_gallery(art_id, title, f"assets/images/raw/{filename}", analysis)
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
