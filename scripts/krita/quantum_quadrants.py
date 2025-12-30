from krita import *

def create_quantum_quadrants():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    root = doc.rootNode()
    
    # Create a Group for the Quantum Effect
    group = doc.createGroupLayer("SYSTEM: Quantum Quadrants")
    root.addChildNode(group, None)
    
    # 1. The Source Layer (What you draw on)
    source = doc.createPaintLayer("DRAW HERE (Top Left)", "RGBA", "U8")
    group.addChildNode(source, None)
    
    # Note: Full 'Clone Layer' setup via API requires specific node types.
    # For now, this script sets up the layer structure for your composition.
    print("--- QUANTUM QUADRANTS SETUP ---")
    print("1. Draw in the 'DRAW HERE' layer.")
    print("2. Duplicate this layer 3 times.")
    print("3. Apply: Mirror Horizontal, Mirror Vertical, and Rotate 180 to the copies.")
    print("4. This creates Non-Euclidean 'Impossible' Symmetry.")

create_quantum_quadrants()
