from krita import *

def glitch_shift_refined():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    red_layer = base.duplicate()
    red_layer.setName("GLITCH: Red Shift")
    red_layer.setBlendingMode("screen")
    doc.rootNode().addChildNode(red_layer, base)
    
    red_layer.move(int(doc.width() * -0.005), 0)
    print("Red channel offset. Hide G and B on this layer via Channels docker.")

glitch_shift_refined()
