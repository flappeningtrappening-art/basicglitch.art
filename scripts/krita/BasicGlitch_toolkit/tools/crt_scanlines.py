from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    doc = Krita.instance().activeDocument()
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("📺 APPLYING CRT SCANLINES...")
    
    try:
        config = InfoObject()
        # We use the 'grid' generator to simulate scanlines
        config.setProperty("grid_size", 4)
        config.setProperty("line_width", 2.0)
        config.setProperty("color", QColor(0, 0, 0))
        config.setProperty("vertical", False) # Horizontal lines only
        
        # Fixed for Krita 5.2: requires (name, generator, info, selection)
        empty_selection = Selection()
        layer = doc.createFillLayer("FX: CRT Scanlines", "grid", config, empty_selection)
        layer.setBlendingMode("multiply")
        layer.setOpacity(30)
        
        doc.rootNode().addChildNode(layer, None)
        print("✅ CRT Scanlines applied via Procedural Grid.")
        doc.refreshProjection()
        
    except Exception as e:
        error_msg = f"❌ Scanline Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()
