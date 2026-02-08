from krita import *
import random

def run():
    """Neural Style Bridge: Procedural Style Transfer via Krita Filter Chains"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    node = doc.activeNode()
    if not node:
        print("No active layer")
        return

    print("🧠 NEURAL STYLE BRIDGE - PROCESSING...")
    
    # 1. Create a "Neural Processing" Group
    group = doc.createGroupLayer(f"STYLE_TRANSFER: {node.name()}")
    doc.rootNode().addChildNode(group, node)
    
    # 2. Duplicate Base for Processing
    # We create multiple passes to simulate 'Neural Layers'
    
    # Pass A: The 'Structure' Pass (Edge Detection / Sketch)
    sketch = node.duplicate()
    sketch.setName("STYLE: Structure_Pass")
    group.addChildNode(sketch, None)
    
    # Apply Edge Detection filter
    edge_filter = app.filter("edge detection")
    edge_filter.apply(sketch, 0, 0, doc.width(), doc.height())
    sketch.setBlendingMode("overlay")
    sketch.setOpacity(40)
    
    # Pass B: The 'Color' Pass (Hue Shift / Saturation)
    color_pass = node.duplicate()
    color_pass.setName("STYLE: Color_Quantum_Shift")
    group.addChildNode(color_pass, None)
    
    # Apply HSV adjustment
    hsv_filter = app.filter("hsvadjustment")
    hsv_config = hsv_filter.configuration()
    hsv_config.setProperty("h", random.randint(-180, 180))
    hsv_config.setProperty("s", 50)
    hsv_filter.setConfiguration(hsv_config)
    hsv_filter.apply(color_pass, 0, 0, doc.width(), doc.height())
    color_pass.setBlendingMode("color")
    
    # Pass C: The 'Glitch' Pass (Halftoning / Pixelize)
    glitch = node.duplicate()
    glitch.setName("STYLE: Neural_Dissonance")
    group.addChildNode(glitch, None)
    
    pixel_filter = app.filter("pixelize")
    pixel_config = pixel_filter.configuration()
    pixel_config.setProperty("pixelWidth", 4)
    pixel_config.setProperty("pixelHeight", 4)
    pixel_filter.setConfiguration(pixel_config)
    pixel_filter.apply(glitch, 0, 0, doc.width(), doc.height())
    glitch.setBlendingMode("screen")
    glitch.setOpacity(30)
    
    print("✅ NEURAL STYLE TRANSFER COMPLETE")
    print("   • Structure Pass: Edge Detection / Overlay")
    print("   • Color Pass: Random Hue Shift / Color Blend")
    print("   • Dissonance Pass: Pixelation / Screen Blend")

if __name__ == "__main__":
    run()