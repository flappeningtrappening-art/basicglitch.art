from krita import *
import os

# This version is for WINDOWS KRITA
# It saves directly to the shared folder so Linux can process it
# You might need to adjust the DRIVE letter (C:, D:, etc) to match your Windows setup
WINDOWS_SHARED_FOLDER = "C:/sf_minty_windows" 

def run():
    if not os.path.exists(WINDOWS_SHARED_FOLDER):
        print(f"❌ Shared folder not found: {WINDOWS_SHARED_FOLDER}")
        print(f"   Please create this folder or update the path")
        return
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No active document!")
        return
    
    # Generate filename
    filename = doc.name().split('.')[0] + ".png"
    full_path = os.path.join(WINDOWS_SHARED_FOLDER, filename)
    
    # Export flat PNG
    conf = InfoObject()
    doc.exportImage(full_path, conf)
    print(f"DONE: Art sent to Shared Folder for Linux processing!")

