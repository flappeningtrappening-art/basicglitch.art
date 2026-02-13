from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Circuit Grid: High-performance Procedural Grid Generation"""
    app = Krita.instance()
    doc = app.activeDocument()
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("⚡ GENERATING CIRCUIT GRID...")
    
    try:
        config = InfoObject()
        config.setProperty("subdivision", 1)
        config.setProperty("line_width", 1.0)
        config.setProperty("grid_size", 50)
        config.setProperty("color", QColor(0, 200, 255, 120)) # Cyan
        
        # Fixed for Krita 5.2: requires (name, generator, info, selection)
        empty_selection = Selection()
        grid_layer = doc.createFillLayer("TECH: Circuit Grid", "grid", config, empty_selection)
        grid_layer.setBlendingMode("screen")
        grid_layer.setOpacity(150) # ~60%
        
        doc.rootNode().addChildNode(grid_layer, None)
        
        print("✅ Circuit Grid generated via Procedural Fill")
        doc.refreshProjection()
        
    except Exception as e:
        error_msg = f"❌ Grid Gen Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()
