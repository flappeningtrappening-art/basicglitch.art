import json
import os
import time
from playwright.sync_api import sync_playwright

# ========================================================
# POD SIGNUP ASSISTANT (V2 - RESILIENT)
# ========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "pod_identity.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("Error: pod_identity.json not found.")
        return None
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def run_assistant():
    config = load_config()
    if not config: return

    user = config['common']
    print(f"Loaded Identity: {user['username']}")

    with sync_playwright() as p:
        # Increased slow_mo to 150ms to look more human
        browser = p.chromium.launch(headless=False, slow_mo=150)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        # 1. REDBUBBLE
        print("\n--- INITIATING: REDBUBBLE ---")
        page_rb = context.new_page()
        # Direct Join URL
        page_rb.goto("https://www.redbubble.com/signup", wait_until="networkidle")
        
        try:
            # Redbubble uses "Artist Signup" vs "Customer Signup"
            # Try to click Artist Signup if it appears
            if page_rb.get_by_text("Artist signup").is_visible():
                page_rb.click("text=Artist signup")
                print(">> Selected Artist Signup.")
            
            page_rb.fill("input[name='email']", user['email'])
            page_rb.fill("input[name='username']", user['username'])
            page_rb.fill("input[name='password']", user['password'])
            print(">> Redbubble Fields Injected.")
        except Exception:
            print(">> Redbubble: Field detection failed. Please fill manually.")

        # 2. TEEPUBLIC
        print("\n--- INITIATING: TEEPUBLIC ---")
        page_tp = context.new_page()
        page_tp.goto("https://www.teepublic.com/register", wait_until="networkidle")
        
        try:
            # Using broader selectors
            page_tp.fill("input[placeholder*='Email']", user['email'])
            page_tp.fill("input[placeholder*='Username']", user['username'])
            page_tp.fill("input[name*='password']", user['password'])
            page_tp.fill("input[name*='confirmation']", user['password'])
            print(">> TeePublic Fields Injected.")
        except Exception:
            print(">> TeePublic: Field detection failed. Please fill manually.")

        # 3. SOCIETY6
        print("\n--- INITIATING: SOCIETY6 ---")
        page_s6 = context.new_page()
        page_s6.goto("https://society6.com/register", wait_until="networkidle")
        
        try:
            page_s6.fill("input[name='email']", user['email'])
            page_s6.fill("input[name='username']", user['username'])
            page_s6.fill("input[name='password']", user['password'])
            print(">> Society6 Fields Injected.")
        except Exception:
            print(">> Society6: Field detection failed. Please fill manually.")

        print("\n========================================================")
        print("ACTION REQUIRED: FINISH SIGNUPS MANUALLY")
        print("1. Solve CAPTCHAs on each tab.")
        print("2. Click 'Sign Up' or 'Join'.")
        print("3. Check your email for verification links.")
        print("\nBrowser remains open for 15 minutes.")
        print("========================================================")
        
        time.sleep(900) 
        browser.close()

if __name__ == "__main__":
    run_assistant()
