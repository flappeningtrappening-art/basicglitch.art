from krita import *
from PyQt5.QtGui import QColor
import random

def run():
    """Generate neural network inspired patterns"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    # Create pattern layer
    layer = doc.createVectorLayer("PATTERN: Neural Network")
    doc.rootNode().addChildNode(layer, None)
    
    shapes = layer.shapes()
    color = QColor(0, 200, 255, 150)  # Cyan with transparency
    
    # Create network-like pattern
    for _ in range(50):
        # Start point
        x1 = random.randint(0, doc.width())
        y1 = random.randint(0, doc.height())
        
        # End point (somewhat connected)
        x2 = x1 + random.randint(-100, 100)
        y2 = y1 + random.randint(-100, 100)
        
        # Create line
        line = shapes.createLineShape(QPointF(x1, y1), QPointF(x2, y2))
        line.setStrokeColor(color)
        line.setStrokeWidth(random.uniform(0.5, 2.0))
        shapes.addShape(line)
        
        # Add node at start
        if random.random() > 0.7:
            node = shapes.createEllipseShape(
                QRectF(x1 - 3, y1 - 3, 6, 6)
            )
            node.setStrokeColor(color)
            node.setStrokeWidth(1.0)
            node.setFillColor(color)
            shapes.addShape(node)
    
    layer.updateProjection()
    
    print("✅ Neural pattern generated")
    print("   • Network-like connections")
    print("   • Vector layer (editable)")
    print("   • Adjust colors in Layers docker")

# For compatibility
def main():
    run()

def execute():
    run()
