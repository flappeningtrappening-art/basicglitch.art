from krita import *
from PyQt5.QtGui import QColor

def run():
    """Simple night mode - blue tint overlay"""
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No document open")
        return
    
    # Create blue tint overlay
    from krita import InfoObject
    config = InfoObject()
    
    # Dark blue color for night
    night_blue = QColor(30, 50, 100)  # RGB: 30,50,100
    
    config.setProperty("color", night_blue)
    
    # Create fill layer - WITH SELECTION PARAMETER (None for full layer)
    try:
        night_layer = doc.createFillLayer("NIGHT MODE: Blue Tint", "color", config, None)
        night_layer.setBlendingMode("multiply")
        night_layer.setOpacity(40)  # Adjustable
        
        doc.rootNode().addChildNode(night_layer, None)
        
        print("✅ Night mode applied")
        print("   • Dark blue tint (multiply blend)")
        print("   • 40% opacity - adjust in Layers docker")
        print("   • Toggle layer visibility for day/night")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nALTERNATIVE: Create paint layer with blue fill")
        
        # Fallback method
        paint_layer = doc.createNode("NIGHT MODE", "paintlayer")
        paint_layer.setBlendingMode("multiply")
        paint_layer.setOpacity(40)
        
        # Would need to fill with color here, but that's more complex
        doc.rootNode().addChildNode(paint_layer, None)
        
        print("✅ Created night mode layer")
        print("   Manually fill with dark blue (RGB: 30,50,100)")
