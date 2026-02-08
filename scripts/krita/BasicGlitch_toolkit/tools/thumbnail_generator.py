from krita import *
import os

def generate_thumbnail():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No active document.")
        return

    # Clone to avoid modifying original
    thumb_doc = doc.clone()
    
    # Resize to width 600px (common thumb size)
    new_width = 600
    ratio = new_width / thumb_doc.width()
    new_height = int(thumb_doc.height() * ratio)
    
    # Use high-quality scaling
    thumb_doc.scale(new_width, new_height, 72) 
    
    # Path
    # Adapts to your project structure
    path = os.path.expanduser("~/monetization/basic-glitch-art/assets/images/gallery-thumbs/")
    if not os.path.exists(path): os.makedirs(path)
    
    # Clean filename
    clean_name = doc.name().replace(' ', '_').lower()
    if clean_name.endswith('.kra'):
        clean_name = clean_name[:-4]
        
    filename = clean_name + ".jpg"
    full_path = os.path.join(path, filename)
    
    # Export params for JPG
    export_params = InfoObject()
    export_params.setProperty("quality", 85)
    export_params.setProperty("optimize", True)
    export_params.setProperty("baseline", True)
    
    thumb_doc.setBatchmode(True)
    if thumb_doc.exportImage(full_path, export_params):
        print(f"[SUCCESS] Thumbnail generated: {full_path}")
    else:
        print(f"[ERROR] Failed to save thumbnail to {full_path}")
        
    thumb_doc.close()

generate_thumbnail()
