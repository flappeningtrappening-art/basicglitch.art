from krita import *
import os

def export_refined():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    path = os.path.expanduser("~/monetization/basic-glitch-art/assets/images/raw/")
    if not os.path.exists(path): os.makedirs(path)
    
    filename = doc.name().split('.')[0] + "_web.png"
    full_path = os.path.join(path, filename)
    
    conf = InfoObject()
    doc.exportImage(full_path, conf)
    print(f"[SUCCESS] Web-ready version saved: {filename}")

export_refined()
