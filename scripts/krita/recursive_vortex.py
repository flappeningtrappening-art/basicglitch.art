from krita import *

def spiral_symmetry():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    iterations = 8
    for i in range(1, iterations):
        clone = base.duplicate()
        clone.setName(f"Vortex Echo {i}")
        doc.rootNode().addChildNode(clone, base)
        print(f"Echo {i} created. Rotate layer manually.")

spiral_symmetry()
