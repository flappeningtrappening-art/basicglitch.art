import csv
import json
import os
import time
from playwright.sync_api import sync_playwright

# ========================================================
# POD UPLOAD ASSISTANT (V1)
# ========================================================
# AUTOMATED METADATA INJECTION
# 1. Loads credentials from pod_identity.json
# 2. Reads artwork from pod_market_master.csv
# 3. Uploads image and fills SEO fields
# ========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "scripts/pod_identity.json")
MARKET_CSV = os.path.join(BASE_DIR, "assets/data/pod_market_master.csv")

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def run_upload():
    config = load_config()
    user = config['common']
    
    if not os.path.exists(MARKET_CSV):
        print("Error: No market data found. Run ingest_art.py first.")
        return

    with open(MARKET_CSV, mode='r') as f:
        reader = csv.DictReader(f)
        listings = list(reader)

    if not listings:
        print("Market Registry is empty.")
        return

    # Process the most recent listing
    item = listings[-1]
    print(f"\n🚀 READY TO LAUNCH: {item['Original Title']}")
    
    image_path = os.path.join(BASE_DIR, item['Local File'])
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        
        # ----------------------------------------------------
        # 1. REDBUBBLE UPLOAD
        # ----------------------------------------------------
        print("\n--- TARGET: REDBUBBLE ---")
        page_rb = context.new_page()
        page_rb.goto("https://www.redbubble.com/portfolio/images/new")
        
        print(">> Please LOGIN manually if prompted. Waiting 30s...")
        time.sleep(30) # Time for manual login
        
        try:
            # Re-goto upload page in case redirect happened
            page_rb.goto("https://www.redbubble.com/portfolio/images/new")
            
            # Select the File
            page_rb.set_input_files("input[type='file']", image_path)
            print(">> Image Uploading...")
            
            # Fill Metadata
            page_rb.fill("#work_title_en", item['Market Title'])
            page_rb.fill("#work_description_en", item['Description'])
            page_rb.fill("#work_tag_field", item['Tags'])
            print(">> Metadata Injected.")
        except Exception as e:
            print(f"Redbubble Error: {e}")

        # ----------------------------------------------------
        # 2. TEEPUBLIC UPLOAD
        # ----------------------------------------------------
        print("\n--- TARGET: TEEPUBLIC ---")
        page_tp = context.new_page()
        page_tp.goto("https://www.teepublic.com/designs/new")
        
        try:
            page_tp.set_input_files("input[type='file']", image_path)
            # TeePublic typically updates fields via AJAX after upload
            time.sleep(5)
            page_tp.fill("input[name='design[title]']", item['Market Title'])
            page_tp.fill("textarea[name='design[description]']", item['Description'])
            page_tp.fill("#tags", item['Tags'])
            print(">> TeePublic Injected.")
        except Exception as e:
            print(f"TeePublic Error: {e}")

        print("\n========================================================")
        print("FINALIZE PRODUCT PLACEMENT MANUALLY")
        print("Adjust designs on each product, then click PUBLISH.")
        print("Browser will close in 15 minutes.")
        print("========================================================")
        
        time.sleep(900) 
        browser.close()

if __name__ == "__main__":
    run_upload()
