from krita import *
from PyQt5.QtGui import QColor

def run():
    """RGB Glitch: High-fidelity Chromatic Aberration via Layer Separation"""
    app = Krita.instance()
    doc = app.activeDocument()
    if not doc:
        print("No document open")
        return
    
    base = doc.activeNode()
    if not base:
        print("No active layer")
        return
    
    print("🌈 RGB GLITCH SYSTEM - DECOUPLING CHANNELS")
    
    # 1. Create the Glitch Group
    group = doc.createGroupLayer(f"RGB_GLITCH: {base.name()}")
    doc.rootNode().addChildNode(group, base)
    
    # 2. Channel Config (Shift amounts)
    # We use small % based offsets for resolution independence
    shift_x = int(doc.width() * 0.005)
    shift_y = int(doc.height() * 0.002)
    
    # 3. Create RED Channel
    red = base.duplicate()
    red.setName("CHANNEL: Red_Shift")
    group.addChildNode(red, None)
    # Move RED right
    red.move(shift_x, 0)
    # Tint RED (Using Krita's HSV filter to isolate red)
    hsv = app.filter("hsvadjustment")
    cfg = hsv.configuration()
    cfg.setProperty("colorize", True)
    cfg.setProperty("h", 0) # Red
    cfg.setProperty("s", 100)
    hsv.setConfiguration(cfg)
    hsv.apply(red, 0, 0, doc.width(), doc.height())
    red.setBlendingMode("screen")
    
    # 4. Create BLUE Channel
    blue = base.duplicate()
    blue.setName("CHANNEL: Blue_Shift")
    group.addChildNode(blue, None)
    # Move BLUE left
    blue.move(-shift_x, shift_y)
    # Tint BLUE
    cfg.setProperty("h", 240) # Blue
    hsv.setConfiguration(cfg)
    hsv.apply(blue, 0, 0, doc.width(), doc.height())
    blue.setBlendingMode("screen")
    
    # 5. Hide the original to see the effect clearly
    # base.setVisible(False) 
    
    print("✅ RGB Glitch Channels Created")
    print(f"   • Red Shift: +{shift_x}px")
    print(f"   • Blue Shift: -{shift_x}px, +{shift_y}px")
    print("   • Blend Mode: Screen (Additive Color)")

if __name__ == "__main__":
    run()