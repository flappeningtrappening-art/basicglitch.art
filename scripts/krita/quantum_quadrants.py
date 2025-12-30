from krita import *

def setup_quantum_quadrants():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    root = doc.rootNode()
    
    # Create a Group for the Quantum Effect
    group = doc.createGroupLayer("SYSTEM: Quantum Quadrants")
    root.addChildNode(group, None)
    
    # 1. The Source Layer (What you draw on)
    source = doc.createPaintLayer("QUADRANT 1: Source (Draw Here)", "RGBA", "U8")
    group.addChildNode(source, None)
    
    print("--- QUANTUM QUADRANTS SETUP ---")
    print("1. Draw in the Source layer.")
    print("2. Duplicate this layer 3 times.")
    print("3. Apply transformations to the copies:")
    print("   - Copy 2: Mirror Horizontal")
    print("   - Copy 3: Mirror Vertical")
    print("   - Copy 4: Rotate 180 degrees")
    print("This creates Non-Euclidean 'Impossible' Symmetry.")

setup_quantum_quadrants()