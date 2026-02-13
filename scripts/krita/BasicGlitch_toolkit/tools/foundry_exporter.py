from krita import *
import os

# ========================================================
# FOUNDRY EXPORTER (Windows -> Linux Pipeline)
# ========================================================
# 1. Saves MASTER (Full Res)
# 2. Saves WEB (Max 2500px)
# 3. Saves THUMB (600px)
# 4. Transfers all to Shared Drive for Linux Ingestion
# ========================================================

SHARED_DRIVE_ROOT = "C:/Users/basic.glitch/Desktop/minty_windows/foundry_transfer"

def ensure_dirs():
    """Creates the folder structure on the shared drive if missing."""
    for sub in ["raw", "web", "thumbs"]:
        path = os.path.join(SHARED_DRIVE_ROOT, sub)
        if not os.path.exists(path):
            os.makedirs(path)

def save_version(doc, folder_name, suffix, max_size=None, quality=100, is_jpg=False):
    """Saves a specific version of the artwork. Note: Scaling the live doc is risky, so we scale, export, and scale back."""
    
    original_w = doc.width()
    original_h = doc.height()
    
    # Resize Logic
    if max_size and (original_w > max_size or original_h > max_size):
        if original_w > original_h:
            new_w = max_size
            new_h = int(original_h * (max_size / original_w))
        else:
            new_h = max_size
            new_w = int(original_w * (max_size / original_h))
        
        doc.scale(new_w, new_h, 72) 
    
    # Filename Logic
    clean_name = doc.name().replace(" ", "_").lower()
    if clean_name.endswith(".kra"): clean_name = clean_name[:-4]
        
    ext = ".jpg" if is_jpg else ".png"
    filename = f"{clean_name}{suffix}{ext}"
    full_path = os.path.join(SHARED_DRIVE_ROOT, folder_name, filename)
    
    # Export Configuration
    info = InfoObject()
    if is_jpg:
        info.setProperty("quality", quality)
    else:
        info.setProperty("compression", 9)
        
    # Save
    if doc.exportImage(full_path, info):
        print(f"[SUCCESS] Saved: {filename}")
    else:
        print(f"[ERROR] Failed: {filename}")
        
    # Restore scale if we changed it
    if max_size and (original_w > max_size or original_h > max_size):
        doc.scale(original_w, original_h, 72)

def run():
    """Entry point for Krita loader"""
    run_pipeline()

def run_pipeline():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("Error: No active document to export.")
        return

    print("--- STARTING FOUNDRY EXPORT PIPELINE ---")
    ensure_dirs()
    
    # In Krita 5, we can't always clone reliably in Python.
    # We will export the current document state instead.
    
    # 1. Export RAW (Full Resolution, PNG)
    save_version(doc, "raw", "", max_size=None, is_jpg=False)
    
    # 2. Export WEB (Max 2500px, PNG)
    save_version(doc, "web", "", max_size=2500, is_jpg=False)
    
    # 3. Export THUMB (Max 600px, JPG 85%)
    save_version(doc, "thumbs", "", max_size=600, quality=85, is_jpg=True)
    
    print("--- PIPELINE COMPLETE: Ready for Linux Ingestion ---")
    # Fixed MessageBox call
    from PyQt5.QtWidgets import QMessageBox
    QMessageBox.information(None, "Foundry Exporter", "Export Complete! Check your shared drive.")

if __name__ == "__main__":
    run()
