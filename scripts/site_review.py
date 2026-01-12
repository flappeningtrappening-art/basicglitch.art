import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ZAI_API_KEY")

if not API_KEY:
    print("Error: ZAI_API_KEY not found in .env file.")
    exit(1)

# Configuration
URL = "https://api.z.ai/api/paas/v4/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Files to analyze
FILES_TO_READ = [
    "index.html",
    "about.html",
    "gallery.html",
    "commissions.html",
    "contact.html",
    "assets/css/style.css",
    "assets/js/app.js",
    "assets/js/robot.js"
]

def read_files():
    content_buffer = ""
    for file_path in FILES_TO_READ:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                content_buffer += f"\n\n--- START OF FILE: {file_path} ---\n"
                content_buffer += content
                content_buffer += f"\n--- END OF FILE: {file_path} ---\n"
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
    return content_buffer

def get_design_review(site_content):
    print("Transmitting site architecture to the mainframe...")
    
    system_prompt = (
        "You are a Senior Creative Director and Full-Stack Developer specializing in 'Cyber-Eclectic', 'Tech-Noir', and 'Glitch Art' aesthetics. "
        "Your goal is to review the provided website code for a digital artist named 'BasicGlitch'. "
        "The site aims to be immersive, high-contrast, and interactive without sacrificing usability.\n\n"
        "Please provide a comprehensive review covering:\n"
        "1. **Visual Aesthetic & Theme:** Does the code support the intended vibe? (Neon, Glitch, Cyberpunk). Are there missed opportunities for CSS effects?\n"
        "2. **UX/UI & Accessibility:** Identify friction points. Are the 3D transforms and animations accessible? Is navigation clear?\n"
        "3. **Code Quality & Performance:** Look for redundant CSS, potential JS bottlenecks, or structural HTML issues.\n"
        "4. **Creative Recommendations:** Suggest 3 specific, actionable features or changes to make the site 'cooler' or more engaging (e.g., more interactive easter eggs, specific animations).\n\n"
        "Be critical but constructive. Speak in a professional yet slightly 'tech-noir' persona."
    )

    payload = {
        "model": "glm-4.6v-flash",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Here is the complete source code for the BasicGlitch website:\n\n{site_content}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: API returned status {response.status_code}\n{response.text}"

    except Exception as e:
        return f"Connection Error: {e}"

def main():
    site_content = read_files()
    if not site_content:
        print("No content read. Aborting.")
        return

    review = get_design_review(site_content)
    
    print("\n" + "="*40)
    print("DESIGN REVIEW INCOMING")
    print("="*40 + "\n")
    print(review)
    print("\n" + "="*40)

    # Optional: Save report
    with open("notes/design_review_glm4.md", "w") as f:
        f.write(review)
    print("Review saved to notes/design_review_glm4.md")

if __name__ == "__main__":
    main()
