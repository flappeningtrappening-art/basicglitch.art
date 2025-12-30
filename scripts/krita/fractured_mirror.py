from krita import *

def apply_fractured_mirror():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    mid_point = doc.width() / 2
    mirror_node = base.duplicate()
    mirror_node.setName(f"GLITCH: Mirror of {base.name()}")
    doc.rootNode().addChildNode(mirror_node, base)

    mirror_node.move(int(mid_point), 20)
    mirror_node.setOpacity(220) 
    mirror_node.setBlendingMode("screen") 

    doc.refreshProjection()
    print("Select new layer and Go to: Layer -> Transform -> Mirror Horizontally.")

apply_fractured_mirror()
