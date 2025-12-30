from krita import *

def apply_fractured_mirror():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base:
        print("No active document or layer!")
        return

    # 1. SETUP: Calculate the split line (Center)
    mid_point = doc.width() / 2
    
    # 2. CLONE: Create the mirrored side
    mirror_node = base.duplicate()
    mirror_node.setName(f"GLITCH: Mirror of {base.name()}")
    doc.rootNode().addChildNode(mirror_node, base)

    # 3. TRANSFORM: Flip and Offset
    # We move the cloned layer to the right half
    # AND we add the 'Fracture' (Vertical shift of 20 pixels)
    mirror_node.move(int(mid_point), 20)
    
    # 4. GLITCH AESTHETIC: Lower opacity slightly to create overlap glow
    mirror_node.setOpacity(220) # Approx 85%
    mirror_node.setBlendingMode("screen") # Great for Neon overlap

    # 5. USER INSTRUCTION (The manual flip)
    doc.refreshProjection()
    print("--- FRACTURED MIRROR APPLIED ---")
    print("1. Select the new layer: 'GLITCH: Mirror...'")
    print("2. Go to: Layer -> Transform -> Mirror Layer Horizontally")
    print("3. RESULT: Perfect glitch symmetry with a 20px vertical fracture.")

apply_fractured_mirror()