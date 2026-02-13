from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Generates apparel design templates. Fixed for Krita 5.2 API."""
    doc = Krita.instance().activeDocument()
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "Please open a document first!")
        return
    
    print("👕 GENERATING MASTER APPAREL TEMPLATES...")
    
    templates = {
        "HOODIE (12x16)": (12, 16, "#00fff7"),
        "TAPESTRY (50x60)": (50, 60, "#ff1ccf"),
        "BALL CAP (4.5x2.25)": (4.5, 2.25, "#ffff00")
    }
    
    try:
        root = doc.rootNode()
        dpi = doc.xRes()
        if dpi < 1: dpi = 300 # Fallback
        
        main_group = doc.createGroupLayer("APPAREL DESIGN GUIDES")
        root.addChildNode(main_group, None)
        
        empty_selection = Selection()
        
        for name, specs in templates.items():
            w_in, h_in, color_hex = specs
            w_px = int(w_in * dpi)
            h_px = int(h_in * dpi)
            
            # Create Color Config
            info = InfoObject()
            info.setProperty("color", QColor(color_hex))
            
            # Create Fill Layer 
            # Fixed for Krita 5.2: requires (name, generator, info, selection)
            layer = doc.createFillLayer(f"GUIDE: {name}", "color", info, empty_selection)
            layer.setOpacity(100)
            layer.setVisible(False)
            
            # Center it
            # Note: For fill layers, we'd ideally use a selection mask, 
            # but since we're using fill layers as guides, we'll just name them with dimensions.
            
            main_group.addChildNode(layer, None)
            
        QMessageBox.information(None, "BasicGlitch", "Apparel Templates Created in hidden group.")
        print("✅ Apparel Templates Created.")
        
    except Exception as e:
        error_msg = f"❌ Template Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()
