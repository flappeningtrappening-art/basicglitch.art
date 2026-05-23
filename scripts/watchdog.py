import os
import time
import subprocess
import datetime

# ========================================================
# BASICGLITCH WATCHDOG (V1.0)
# ========================================================
# Monitors the shared transfer folder and triggers ingestion.
# ========================================================

SHARED_DIR = "/media/sf_minty_windows"
INGEST_SCRIPT = "/home/blitz/monetization/basic-glitch-art/scripts/ingest_art.py"
LOG_FILE = "/home/blitz/monetization/basic-glitch-art/notes/watchdog.log"

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "
")

def check_for_new_signals():
    if not os.path.exists(SHARED_DIR):
        return False
    
    # Check root and subfolders
    for root, dirs, files in os.walk(SHARED_DIR):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".mp4", ".mov", ".webm")):
                # Check if it's in a transfer subfolder or the root
                if "transfer2website" in root or root == SHARED_DIR:
                    return True
    return False

def run_ingestion():
    log("🚀 NEW SIGNAL DETECTED. Triggering Foundry Ingestion Engine...")
    try:
        # Run the ingestion script and capture output
        result = subprocess.run(["python3", INGEST_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            log("✅ INGESTION SUCCESSFUL.")
            if "Deployment Synchronized" in result.stdout:
                log("🌍 SITE SYNCED TO MAIN FRAME.")
        else:
            log(f"❌ INGESTION FAILED: {result.stderr}")
    except Exception as e:
        log(f"⚠️ WATCHDOG ERROR: {e}")

if __name__ == "__main__":
    log("📡 WATCHDOG ONLINE. Monitoring shared frequency...")
    
    while True:
        if check_for_new_signals():
            run_ingestion()
            # Wait a bit after processing to avoid tight loops if files persist
            time.sleep(30)
        else:
            # Low-frequency poll
            time.sleep(10)
