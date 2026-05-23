
import os
import json
import asyncio
import litellm
from dotenv import load_dotenv

# Path to the analytic-service .env
load_dotenv("/home/blitz/monetization/foundry-suite/solution-factory/services/analytic-service/.env")

api_key = os.getenv("ZHIPUAI_API_KEY")
api_base = "https://open.bigmodel.cn/api/paas/v4/"
model = "glm-4.6v-flash"

GALLERY_FILE = "/home/blitz/monetization/basic-glitch-art/assets/data/gallery.json"

async def generate_description(item):
    title = item['title']
    styles = ", ".join(item.get('styles', []))
    alt_text = item.get('alt_text', 'N/A')
    
    prompt = f"""
    You are a professional art curator for the 'BasicGlitch' gallery.
    Based on the following visual details (Alt Text) for the piece "{title}", write a concise, compelling one-paragraph description (2-3 sentences).
    
    Title: {title}
    Styles: {styles}
    Literal Visual Content: {alt_text}
    
    Requirements:
    1. Ground the description in the actual subjects described in the Alt Text.
    2. Tone: Professional and artistically descriptive. Do not use filler buzzwords like 'digital entropy' unless they are central to the piece.
    3. VARIETY: Each description should reflect the specific piece's unique theme (e.g., character design, landscape, or cinematic parody).
    4. Output ONLY the one-paragraph description.
    """
    
    try:
        response = await asyncio.to_thread(
            litellm.completion,
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_key=api_key,
            api_base=api_base,
            custom_llm_provider="openai",
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating description for {title}: {e}")
        return None

async def main():
    with open(GALLERY_FILE, 'r') as f:
        data = json.load(f)
    
    updated = False
    for item in data:
        # Update all items to replace the old 'Taco Bell' style descriptions
        print(f"Generating unique description for: {item['title']}...")
        new_desc = await generate_description(item)
        if new_desc:
            item['description'] = new_desc
            updated = True
            print(f"DONE: {new_desc[:50]}...")
    
    if updated:
        with open(GALLERY_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print("Gallery updated successfully.")
    else:
        print("No eligible items found for update.")

if __name__ == "__main__":
    asyncio.run(main())
