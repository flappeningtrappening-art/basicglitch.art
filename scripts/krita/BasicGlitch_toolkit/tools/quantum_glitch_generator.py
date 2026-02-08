from krita import *
from PyQt5.QtGui import QColor
import random

def run():
    """Apply quantum glitch effects"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    base = doc.activeNode()
    if not base:
        print("No active layer")
        return
    
    print("🌀 QUANTUM GLITCH GENERATOR")
    print("=" * 40)
    
    # Create glitch layers group
    group = doc.createGroupLayer("FX: Quantum Glitch")
    doc.rootNode().addChildNode(group, base)
    
    # Create different glitch variations
    glitch_types = [
        ("Red Shift", QColor(255, 50, 50, 150), 5, 0),
        ("Green Shift", QColor(50, 255, 50, 150), -3, 4),
        ("Blue Shift", QColor(50, 50, 255, 150), 0, -5),
        ("Scanlines", QColor(0, 0, 0, 100), 0, 0)
    ]
    
    for name, color, offset_x, offset_y in glitch_types:
        layer = base.duplicate()
        layer.setName(f"GLITCH: {name}")
        
        if "Scanlines" in name:
            layer.setBlendingMode("multiply")
            layer.setOpacity(30)
        else:
            layer.setBlendingMode("screen")
            layer.setOpacity(70)
            layer.move(offset_x, offset_y)
        
        group.addChildNode(layer, None)
    
    print(f"✅ Quantum glitch applied")
    print(f"\n📁 Created group: 'FX: Quantum Glitch'")
    print(f"🎭 Layers created:")
    print(f"  • Red Shift: +5px horizontal")
    print(f"  • Green Shift: -3px horizontal, +4px vertical")
    print(f"  • Blue Shift: -5px vertical")
    print(f"  • Scanlines: 30% opacity multiply")
    
    print(f"\n🔧 Adjustments:")
    print(f"  • Toggle layer visibility for different effects")
    print(f"  • Adjust opacity in Layers docker")
    print(f"  • Move layers for different offset effects")

# For compatibility
def main():
    run()

def execute():
    run()
