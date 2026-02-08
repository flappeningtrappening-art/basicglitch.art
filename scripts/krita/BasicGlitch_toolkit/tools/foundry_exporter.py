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

SHARED_DRIVE_ROOT = "C:/sf_minty_windows/foundry_transfer"

def ensure_dirs():
    """Creates the folder structure on the shared drive if missing."""
    for sub in ["raw", "web", "thumbs"]:
        path = os.path.join(SHARED_DRIVE_ROOT, sub)
        if not os.path.exists(path):
            os.makedirs(path)

def save_version(doc, folder_name, suffix, max_size=None, quality=100, is_jpg=False):
    """Resizes and saves a specific version of the artwork."""
    
    # Clone to avoid destroying the open document
    clone = doc.clone()
    
    # Resize Logic
    if max_size:
        current_w = clone.width()
        current_h = clone.height()
        
        if current_w > max_size or current_h > max_size:
            if current_w > current_h:
                new_w = max_size
                new_h = int(current_h * (max_size / current_w))
            else:
                new_h = max_size
                new_w = int(current_w * (max_size / current_h))
            
            clone.scale(new_w, new_h, 72) # 72 DPI for web
    
    # Filename Logic (Clean Spaces)
    clean_name = doc.name().replace(" ", "_").lower()
    if clean_name.endswith(".kra"):
        clean_name = clean_name[:-4]
        
    ext = ".jpg" if is_jpg else ".png"
    filename = f"{clean_name}{suffix}{ext}"
    full_path = os.path.join(SHARED_DRIVE_ROOT, folder_name, filename)
    
    # Export Configuration
    info = InfoObject()
    if is_jpg:
        info.setProperty("quality", quality)
        info.setProperty("optimize", True)
    else:
        info.setProperty("compression", 9) # Max PNG compression
        info.setProperty("interlaced", False)
        
    # Save
    clone.setBatchmode(True)
    if clone.exportImage(full_path, info):
        print(f"[SUCCESS] Saved {folder_name.upper()}: {filename}")
    else:
        print(f"[ERROR] Failed to save {filename}")
        
    clone.close()

def run_pipeline():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("Error: No active document to export.")
        return

    print("--- STARTING FOUNDRY EXPORT PIPELINE ---")
    ensure_dirs()
    
    # 1. Export RAW (Full Resolution, PNG)
    save_version(doc, "raw", "", max_size=None, is_jpg=False)
    
    # 2. Export WEB (Max 2500px, PNG)
    save_version(doc, "web", "", max_size=2500, is_jpg=False)
    
    # 3. Export THUMB (Max 600px, JPG 85%)
    save_version(doc, "thumbs", "", max_size=600, quality=85, is_jpg=True)
    
    print("--- PIPELINE COMPLETE: Ready for Linux Ingestion ---")
    MessageBox = Krita.instance().messageBox
    MessageBox("Foundry Export Complete!
Files transferred to shared drive.", "Success")

run_pipeline()
