from krita import *
from PyQt5.QtGui import QColor

def run():
    """Generates professional apparel design templates with safe zones"""
    doc = Krita.instance().activeDocument()
    if not doc:
        print("Please open a document first!")
        return
    
    print("👕 GENERATING MASTER APPAREL TEMPLATES...")
    
    # Template Configuration
    # Format: "Name": (Width_Inches, Height_Inches, "HexColor")
    templates = {
        "HOODIE / T-SHIRT (Chest)": (12, 16, "#00fff7"),       # Cyan
        "TAPESTRY (Wall Hang)": (50, 60, "#ff1ccf"),           # Neon Magenta
        "BACKPACK (Main Panel)": (11, 15, "#00ff3e"),          # Neon Green
        "DUFFEL BAG (Side Panel)": (12, 12, "#ff5f1f"),        # Neon Orange
        "SHOPPING BAG (Tote)": (13, 13, "#d0ff00"),            # Neon Lemon
        "SOCKS (Leg Zone)": (3.5, 4.5, "#0a7aff"),             # Neon Blue
        "BEANIE (Cuff Area)": (4, 2.5, "#c724ff"),             # Neon Purple
        "BALL CAP (Front Panel)": (4.5, 2.25, "#ffff00")       # Neon Yellow
    }
    
    root = doc.rootNode()
    dpi = doc.xRes()
    
    # Create Main Group
    main_group = doc.createGroupLayer("APPAREL DESIGN GUIDES")
    root.addChildNode(main_group, None)
    
    for name, specs in templates.items():
        w_in, h_in, color_hex = specs
        
        # Convert inches to pixels based on document DPI
        w_px = int(w_in * dpi)
        h_px = int(h_in * dpi)
        
        # Create Sub-Group for this item
        item_group = doc.createGroupLayer(f"TEMPLATE: {name}")
        item_group.setVisible(False) # Hide by default
        main_group.addChildNode(item_group, None)
        
        # 1. Create Safe Zone Guide (Vector Rectangle)
        # We use a selection mask fill because it's reliable in Krita's API
        info = InfoObject()
        info.setProperty("color", color_hex)
        
        # Calculate center position
        x = (doc.width() - w_px) // 2
        y = (doc.height() - h_px) // 2
        
        # Create Selection for the box
        selection = Selection()
        selection.select(x, y, w_px, h_px, 255)
        
        # Create Fill Layer with that selection
        layer = doc.createFillLayer(f"GUIDE: {name} ({w_in}\"x{h_in}\")", "color", info)
        layer.setOpacity(40) # 40% opacity
        layer.setSelection(selection)
        
        item_group.addChildNode(layer, None)
        
        # 2. Add Label (Note: Text shapes are complex in API, sticking to layer naming)
        
    print("✅ Apparel Templates Created")
    print("   • Toggle visibility in the 'APPAREL DESIGN GUIDES' group")
    print("   • Guides are centered and scaled to document DPI")

if __name__ == "__main__":
    run()
