
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

async def generate_description(title, analysis):
    prompt = f"""
    You are the Forensic Critic for BasicGlitch art.
    Based on the following Forensic Analysis for the piece "{title}", write a concise, compelling one-paragraph description (2-3 sentences) for the art gallery.
    
    The tone should be 'Cyber-Eclectic' and 'Tech-Noir'. Use high-impact, professional, and slightly aggressive artistic terminology.
    
    Forensic Analysis:
    {analysis}
    
    Output ONLY the one-paragraph description.
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
        desc = item.get('description', '')
        # Check if it has a placeholder description
        if "New forensic entry" in desc or "Neon Surrealism Piece" in desc:
            analysis = item.get('forensic_analysis')
            context = analysis if analysis else f"A high-impact digital surrealist piece titled {item['title']} in the style of {', '.join(item.get('styles', []))}."
            
            print(f"Generating real description for: {item['title']}...")
            new_desc = await generate_description(item['title'], context)
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
