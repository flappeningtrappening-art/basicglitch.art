from krita import *
import math

def run():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: 
        print("Open a document and select a layer")
        return

    iterations = 6
    rotation_step = 45  # 45 degrees each
    
    # Create group
    group = doc.createGroupLayer("FX: Recursive Vortex")
    doc.rootNode().addChildNode(group, None)
    
    print("🌀 RECURSIVE VORTEX")
    print("=" * 40)
    
    for i in range(1, iterations):
        clone = base.duplicate()
        clone.setName(f"Vortex Echo {i}")
        group.addChildNode(clone, None)
        
        print(f"  • Created 'Vortex Echo {i}'")
        print(f"    Apply: Rotate {(rotation_step * i) % 360}°")
        print(f"    Scale: {(0.9 ** i):.1%} of original")
    
    print(f"\n✅ Created {iterations-1} vortex echoes")
    print(f"📁 Group: 'FX: Recursive Vortex'")
