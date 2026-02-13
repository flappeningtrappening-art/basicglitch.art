from krita import *

def run():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base:
        print("No active document or layer!")
        return

    print("🪞 GENERATING FRACTURED MIRROR...")

    # 1. SETUP: Calculate the split line (Center)
    mid_point = doc.width() // 2
    
    # 2. CLONE: Create the mirrored side
    # In Krita 5, we use duplicate()
    mirror_node = base.duplicate()
    mirror_node.setName(f"GLITCH: Mirror of {base.name()}")
    
    # Add to root
    doc.rootNode().addChildNode(mirror_node, None)

    # 3. TRANSFORM: Offset and Fracture
    # Note: Krita move() is absolute coordinate or relative? 
    # Usually it's relative to the parent.
    mirror_node.move(mid_point, 20)
    
    # 4. AESTHETIC: Blending
    mirror_node.setBlendingMode("addition")
    mirror_node.setOpacity(180)

    doc.refreshProjection()
    print("✅ FRACTURED MIRROR APPLIED")
    print("   👉 TIP: Manually Mirror this layer (Layer -> Transform -> Mirror Horizontally)")

if __name__ == "__main__":
    run()