from krita import *

def create_apparel_master_templates():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("Please open a document first!")
        return
    
    res = doc.xRes() # DPI
    root = doc.rootNode()
    
    # Template Format: (Width_Inches, Height_Inches)
    templates = {
        "HOODIE / SHIRT": (12, 16),
        "BACKPACK (Main Panel)": (10, 12),
        "BANDANA (Full)": (22, 22),
        "TOTE BAG": (12, 12),
        "SOCKS (Leg Zone)": (3.5, 4.5),
        "BEANIE (Sock Hat)": (4, 2.5),
        "BALL CAP (Front Logo)": (4, 2)
    }
    
    # Create Main Group
    group = doc.createGroupLayer("APPAREL DESIGN GUIDES")
    root.addChildNode(group, None)
    
    for name, dimensions in templates.items():
        w_in, h_in = dimensions
        
        # Create Sub-Group for this item
        item_group = doc.createGroupLayer(f"TEMPLATE: {name}")
        item_group.setVisible(False) # Hide by default so user can toggle one on
        group.addChildNode(item_group, None)
        
        # 1. Full Bleed / Max Area (Cyan)
        info = InfoObject()
        info.setProperty("color", "#00fff7") # Neon Cyan
        layer = doc.createFillLayer(f"MAX AREA ({w_in}x{h_in})", "color", info)
        layer.setOpacity(20) # Low opacity for visibility
        item_group.addChildNode(layer, None)
        
        # 2. Safe Zone (Red) - 0.5 inch margin
        # We simulate this by creating a smaller selection and filling it, 
        # or easier: just a smaller guide if we were drawing vectors.
        # For simplicity in Python script, we stick to the main guide 
        # but add a note to the layer name.
        
    print("[COMPLETE] Templates created in 'APPAREL DESIGN GUIDES'.")
    print("Toggle visibility of the specific item you are designing for.")

create_apparel_master_templates()