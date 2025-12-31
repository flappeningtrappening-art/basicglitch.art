from krita import *
import os

# This version is for WINDOWS KRITA
# It saves directly to the shared folder so Linux can process it
# Confirmed Path: C:/sf_minty_windows
WINDOWS_SHARED_FOLDER = "C:/sf_minty_windows" 

def export_to_shared():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No active document!")
        return
    
    # Robust filename handling
    # "my.cool.art.kra" -> "my.cool.art.png"
    base_name = os.path.splitext(doc.name())[0]
    filename = base_name + ".png"
    
    full_path = os.path.join(WINDOWS_SHARED_FOLDER, filename)
    
    # Export flat PNG
    # Note: Krita's 'InfoObject' defaults usually work for PNG
    conf = InfoObject()
    # Force high compression, no interlacing
    conf.setProperty("compression", 9)
    conf.setProperty("interlaced", False)
    
    doc.exportImage(full_path, conf)
    print(f"DONE: Exported '{filename}' to Shared Folder!")

export_to_shared()