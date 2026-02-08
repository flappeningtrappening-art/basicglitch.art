from krita import *
from PyQt5.QtGui import QColor

def run():
    """Apply a tech-noir gradient overlay"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    # Create gradient layer
    try:
        # Simple gradient using fill layer
        from krita import InfoObject
        
        # Dark to light blue gradient for tech-noir
        config = InfoObject()
        config.setProperty("type", "linear")
        config.setProperty("repeat", "none")
        config.setProperty("color1", QColor(10, 20, 40))    # Dark blue
        config.setProperty("color2", QColor(100, 150, 200)) # Light blue
        config.setProperty("start", QPointF(0, 0))
        config.setProperty("end", QPointF(doc.width(), doc.height()))
        
        gradient_layer = doc.createFillLayer("FX: Tech-Noir Gradient", "gradient", config)
        gradient_layer.setBlendingMode("overlay")
        gradient_layer.setOpacity(50)  # 50% opacity
        
        doc.rootNode().addChildNode(gradient_layer, None)
        
        print("✅ Tech-Noir Gradient applied")
        print("   • Dark to light blue gradient")
        print("   • Overlay blend mode")
        print("   • 50% opacity - adjust in Layers docker")
        
    except Exception as e:
        print(f"Error creating gradient: {e}")
        print("\nAlternative: Create paint layer and fill manually")

# For compatibility
def main():
    run()

def execute():
    run()
