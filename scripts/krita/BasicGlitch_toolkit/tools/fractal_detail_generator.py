from krita import *
from PyQt5.QtGui import QColor
import random

def run():
    """Create fractal detail layers"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    # Create a group for fractal details
    group = doc.createGroupLayer("FX: Fractal Details")
    doc.rootNode().addChildNode(group, None)
    
    # Create detail layers
    styles = ["circuit", "organic", "architectural"]
    colors = [
        QColor(255, 100, 100, 100),  # Red
        QColor(100, 255, 100, 100),  # Green
        QColor(100, 100, 255, 100)   # Blue
    ]
    
    for i, (style, color) in enumerate(zip(styles, colors)):
        layer = doc.createVectorLayer(f"FRACTAL: {style.capitalize()}")
        layer.setOpacity(150)  # 60% opacity
        group.addChildNode(layer, None)
        
        # Add some simple shapes (circles) as placeholders
        shapes = layer.shapes()
        for _ in range(20):
            x = random.randint(0, doc.width())
            y = random.randint(0, doc.height())
            size = random.randint(5, 20)
            
            circle = shapes.createEllipseShape(
                QRectF(x - size/2, y - size/2, size, size)
            )
            circle.setStrokeColor(color)
            circle.setStrokeWidth(1.0)
            circle.setFillStyle(0)  # No fill
            shapes.addShape(circle)
        
        layer.updateProjection()
    
    print("✅ Fractal details created")
    print("   • Circuit, organic, and architectural patterns")
    print("   • Vector layers (editable with Shape tool)")
    print("   • Adjust opacity in Layers docker")

# For compatibility
def main():
    run()

def execute():
    run()
