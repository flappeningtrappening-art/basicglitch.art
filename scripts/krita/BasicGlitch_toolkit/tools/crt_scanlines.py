from krita import *
from PyQt5.QtGui import QColor

def run():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No document open")
        return
    
    # Create a paint layer
    layer = doc.createPaintLayer("FX: CRT Scanlines", "RGBA", "U8", "multiply", 30)
    doc.rootNode().addChildNode(layer, None)
    
    # Get paint device to draw on
    paint_device = layer.paintDevice()
    
    # Draw scanlines (every 4 pixels)
    color = QColor(0, 0, 0, 128)  # Semi-transparent black
    
    for y in range(0, doc.height(), 4):
        # Draw 2-pixel thick line
        for line_y in range(y, min(y + 2, doc.height())):
            for x in range(doc.width()):
                paint_device.setPixel(x, line_y, color.rgba())
    
    layer.updateProjection()
    print("✅ CRT Scanlines drawn (every 4px, 2px thick)")
    print("   Adjust layer opacity in Layers docker")
