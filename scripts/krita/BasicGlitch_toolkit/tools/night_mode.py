from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Simple night mode - blue tint overlay"""
    doc = Krita.instance().activeDocument()
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("🌙 APPLYING NIGHT MODE...")
    
    try:
        from krita import InfoObject
        config = InfoObject()
        
        # Dark blue color for night
        night_blue = QColor(30, 50, 100)  # RGB: 30,50,100
        config.setProperty("color", night_blue)
        
        # Fixed for Krita 5.2: requires (name, generator, info, selection)
        empty_selection = Selection()
        night_layer = doc.createFillLayer("NIGHT MODE: Blue Tint", "color", config, empty_selection)
        night_layer.setBlendingMode("multiply")
        night_layer.setOpacity(40)  # Adjustable
        
        doc.rootNode().addChildNode(night_layer, None)
        
        print("✅ Night mode applied")
        doc.refreshProjection()
        
    except Exception as e:
        error_msg = f"❌ Night Mode Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()