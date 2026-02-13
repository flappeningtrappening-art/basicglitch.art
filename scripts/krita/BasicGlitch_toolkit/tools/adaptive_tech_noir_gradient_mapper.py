from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Apply a tech-noir gradient overlay"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("🌃 APPLYING TECH-NOIR GRADIENT...")
    
    try:
        from krita import InfoObject
        
        # Dark to light blue gradient for tech-noir
        config = InfoObject()
        config.setProperty("type", "linear")
        config.setProperty("repeat", "none")
        config.setProperty("color1", QColor(10, 20, 40))    # Dark blue
        config.setProperty("color2", QColor(100, 150, 200)) # Light blue
        config.setProperty("start", QPointF(0, 0))
        config.setProperty("end", QPointF(doc.width(), doc.height()))
        
        # Fixed for Krita 5.2: requires (name, generator, info, selection)
        empty_selection = Selection()
        gradient_layer = doc.createFillLayer("FX: Tech-Noir Gradient", "gradient", config, empty_selection)
        gradient_layer.setBlendingMode("overlay")
        gradient_layer.setOpacity(50)  # 50% opacity
        
        doc.rootNode().addChildNode(gradient_layer, None)
        
        print("✅ Tech-Noir Gradient applied")
        doc.refreshProjection()
        
    except Exception as e:
        error_msg = f"❌ Gradient Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()