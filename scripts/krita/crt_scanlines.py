from krita import *

def refined_scanlines():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    layer = doc.createFillLayer("FX: CRT Scanlines", "pattern", InfoObject())
    layer.setOpacity(30)
    layer.setBlendingMode("multiply")
    doc.rootNode().addChildNode(layer, None)
    print("CRT Scanlines added.")

refined_scanlines()
