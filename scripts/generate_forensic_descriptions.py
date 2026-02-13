import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

# ========================================================
# FORENSIC DESCRIPTION GENERATOR
# ========================================================
# Uses Gemini 1.5 Flash to generate 300-word analyses.
# ========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')

def generate_analysis(item):
    print(f"Analyzing: {item['title']}...")
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    You are a forensic art critic and digital curator for 'BasicGlitch'. 
    Write a 300-word forensic analysis of the following artwork piece.
    
    Title: {item['title']}
    Styles: {', '.join(item.get('styles', []))}
    Description: {item.get('description', '')}
    
    Requirements:
    1. EXACTLY 300 words or more.
    2. Tone: Aggressive, technical, professional, and surreal.
    3. Use terms like: 'digital entropy', 'forensic marker', 'quantum superposition', 'cyber-eclectic', 'tech-noir', 'visual autopsy', 'signal-to-noise ratio'.
    4. Focus on the 'Foundry' philosophy: processing raw chaos into high-fidelity artistic intelligence.
    5. Mention why it's perfect for high-end home offices or gaming sanctuaries.
    6. IMPORTANT: Occasionally hide a 'Forensic Fragment' in the text (e.g., [FRAGMENT: SIGNAL_77] or [FRAGMENT: DECAY_0]). These are for the ARG.
    7. Output the analysis in HTML <p> tags.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error analyzing {item['title']}: {e}")
        return None

def process_all():
    with open(GALLERY_JSON, 'r') as f:
        gallery = json.load(f)

    updated = False
    for item in gallery:
        # Only generate if missing or too short
        existing_analysis = item.get('forensic_analysis', "")
        if len(existing_analysis.split()) < 250:
            analysis = generate_analysis(item)
            if analysis:
                item['forensic_analysis'] = analysis
                updated = True
                # Save after each successful generation to prevent data loss
                with open(GALLERY_JSON, 'w') as f:
                    json.dump(gallery, f, indent=2)
                # Avoid rate limits
                time.sleep(5) # Increased delay to 5 seconds

    if updated:
        print("\nSUCCESS: All forensic analyses generated.")
        # Trigger site regeneration
        os.system(f"python3 {os.path.join(BASE_DIR, 'scripts/foundry_site_gen.py')}")
    else:
        print("All items already have high-density forensic analysis.")

if __name__ == "__main__":
    process_all()
