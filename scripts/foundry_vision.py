import os
import json
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ZAI_API_KEY")

if not API_KEY:
    print("Error: ZAI_API_KEY not found in .env file.")
    exit(1)

# Config
GALLERY_PATH = "assets/data/gallery.json"
OUTPUT_PATH = "assets/data/gallery_enriched.json"
IMAGES_BASE_DIR = "." # Script runs from root

# Z.AI Config
URL = "https://api.z.ai/api/paas/v4/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, current_title):
    print(f"Analyzing {current_title}...")
    
    # Check if file exists
    full_path = os.path.join(IMAGES_BASE_DIR, image_path.lstrip('/'))
    if not os.path.exists(full_path):
        print(f"Skipping (File not found): {full_path}")
        return None

    try:
        base64_image = encode_image(full_path)
        
        prompt = (
            f"You are an art curator for a Cyber-Eclectic Surrealism portfolio. "
            f"Analyze this artwork titled '{current_title}'. "
            f"1. Write a compelling, 2-sentence description for the gallery. Focus on the neon aesthetics, mood, and glitch elements. "
            f"2. Provide a concrete, literal description for accessibility (Alt Text). "
            f"3. List 5-8 SEO keywords."
            f"\n\nReturn ONLY a valid JSON object with keys: 'description', 'alt_text', 'keywords'."
        )

        payload = {
            "model": "glm-4.6v-flash",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"} 
        }

        response = requests.post(URL, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            # Clean up potential markdown code blocks
            content = content.replace('```json', '').replace('```', '')
            return json.loads(content)
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    if not os.path.exists(GALLERY_PATH):
        print("Gallery JSON not found.")
        return

    with open(GALLERY_PATH, 'r') as f:
        gallery = json.load(f)

    updated_gallery = []
    
    for item in gallery:
        # Check if already enriched (optional optimization)
        # if 'alt_text' in item: 
        #    updated_gallery.append(item)
        #    continue

        file_path = item.get('file')
        title = item.get('title', 'Untitled')
        
        ai_data = analyze_image(file_path, title)
        
        if ai_data:
            # Update item
            item['description'] = ai_data.get('description', item.get('description'))
            item['alt_text'] = ai_data.get('alt_text', f"Artwork titled {title}")
            
            # Merge keywords
            new_keywords = ai_data.get('keywords', [])
            if isinstance(new_keywords, str): new_keywords = new_keywords.split(',')
            
            current_cats = item.get('categories', [])
            # We don't overwrite categories, maybe add them as tags if we had a tags field
            # For now, let's just create a new field 'seo_keywords'
            item['seo_keywords'] = new_keywords
            
            print(f"--> Updated: {title}")
        
        updated_gallery.append(item)

    # Save
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(updated_gallery, f, indent=2)
    
    print(f"\nSuccess! Enriched data saved to {OUTPUT_PATH}")
    print("Review it, then rename it to gallery.json to go live.")

if __name__ == "__main__":
    main()
