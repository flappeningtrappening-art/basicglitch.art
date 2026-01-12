import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("ZAI_API_KEY")
if not api_key:
    print("Error: ZAI_API_KEY not found in .env file.")
    exit(1)

# Endpoint for Z.AI
url = "https://api.z.ai/api/paas/v4/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Payload to test the connection (using glm-4.6v-flash)
payload = {
    "model": "glm-4.6v-flash",
    "messages": [
        {
            "role": "user",
            "content": "Hello! I am testing the Foundry Suite connection. Please respond with a short, glitch-art themed greeting."
        }
    ],
    "temperature": 0.7,
    "stream": False
}

try:
    print(f"Connecting to Z.AI ({url})...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("\n--- CONNECTION SUCCESSFUL ---")
        print("Response from Z.AI:")
        print(result['choices'][0]['message']['content'])
        print("-----------------------------\n")
    else:
        print(f"\n--- CONNECTION FAILED ---")
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
