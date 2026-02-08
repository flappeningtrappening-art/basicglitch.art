from krita import *

def run():
    doc = Krita.instance().activeDocument()
    if not doc:
        print("No document open")
        return
    
    base = doc.activeNode()
    if not base:
        print("No active layer")
        return

    # Calculate blur sizes
    tight_blur = max(2, int(doc.width() * 0.005))
    wide_blur = max(5, int(doc.width() * 0.02))

    # Create duplicate layers
    tight = base.duplicate()
    tight.setName("NEON: Tight Glow")
    tight.setBlendingMode("screen")
    doc.rootNode().addChildNode(tight, base)

    wide = base.duplicate()
    wide.setName("NEON: Wide Glow")
    wide.setBlendingMode("screen")
    wide.setOpacity(180)  # 70% opacity
    doc.rootNode().addChildNode(wide, tight)

    doc.refreshProjection()
    
    print("✅ Neon glow layers created")
    print(f"\n🔧 Apply Gaussian Blur:")
    print(f"  1. Select 'NEON: Tight Glow' layer")
    print(f"  2. Filters → Blur → Gaussian Blur")
    print(f"  3. Radius: {tight_blur}px")
    print(f"\n  4. Select 'NEON: Wide Glow' layer")
    print(f"  5. Filters → Blur → Gaussian Blur")
    print(f"  6. Radius: {wide_blur}px")
    
    print(f"\n💡 Adjustments:")
    print(f"  • Change blend modes (add, screen, color dodge)")
    print(f"  • Adjust opacity in Layers docker")
    print(f"  • Add color adjustments for different neon colors")
