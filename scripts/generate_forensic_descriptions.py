import os
import json
import time
import litellm
import google.generativeai as genai
from dotenv import load_dotenv

# ========================================================
# FORENSIC DESCRIPTION GENERATOR (V2.0 - GLM-FLASH)
# ========================================================
# Uses GLM-4.6v-flash to generate 300-word analyses (Free Tier).
# ========================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# litellm configuration for GLM-4.6v-flash
litellm.api_key = ZHIPUAI_API_KEY
GLM_MODEL = "openai/glm-4.6v-flash"
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')

def generate_analysis(item):
    print(f"Analyzing: {item['title']} via GLM-Flash...")
    
    prompt = f"""
    You are a professional art critic and digital curator for 'BasicGlitch'. 
    Write a 300-word deep-dive analysis of the following artwork piece.
    
    Title: {item['title']}
    Styles: {', '.join(item.get('styles', []))}
    Literal Description (Alt Text): {item.get('alt_text', 'N/A')}
    Artist's Original Intent: {item.get('description', '')}
    
    Requirements:
    1. EXACTLY 300 words or more.
    2. Tone: Professional, academic, and deeply descriptive. Avoid repetitive marketing buzzwords.
    3. Focus: Analyze the visual composition, the interplay of colors, and the specific emotional or thematic weight of the subjects described in the Alt Text.
    4. VARIETY: Each analysis must feel unique to the specific piece. If it's a 'Pup Fiction' piece, focus on the parody and cinematic tension. If it's a 'Broboticus' piece, focus on the mechanical soul and character design. If it's a landscape, focus on the environmental mood.
    5. GROUNDING: Only mention 'neon', 'glitch', or 'tech-noir' if they are explicitly mentioned in the Alt Text or Styles. Do not use them as 'filler' words.
    6. Mention why the specific mood of THIS piece makes it suitable for high-end spaces (offices, sanctuaries, etc.).
    7. IMPORTANT: Occasionally hide a 'Forensic Fragment' in the text (e.g., [FRAGMENT: SIGNAL_77] or [FRAGMENT: DECAY_0] or [FRAGMENT: VOID_SCAN_X]). These are for the ARG.
    8. Output the analysis in HTML <p> tags.
    """
    
    try:
        response = litellm.completion(
            model=GLM_MODEL,
            api_base=GLM_BASE_URL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing {item['title']}: {e}")
        return None

def process_all():
    with open(GALLERY_JSON, 'r') as f:
        gallery = json.load(f)

    updated = False
    for item in gallery:
        # Overwrite everything to replace the old 'Taco Bell' style analyses
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
