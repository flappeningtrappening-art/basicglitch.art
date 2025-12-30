from krita import *
import math

def spiral_symmetry():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    iterations = 8
    rotation_step = 360 / iterations
    scale_factor = 0.9 # Each copy is 90% size of the previous

    # Create a group to keep things organized
    group = doc.createGroupLayer("FX: Recursive Vortex")
    doc.rootNode().addChildNode(group, None)

    for i in range(1, iterations):
        clone = base.duplicate()
        clone.setName(f"Vortex Echo {i}")
        group.addChildNode(clone, None)
        
        # Note: In Krita Python, we use Move and Rotate
        # This script sets up the layers; you can then apply the 
        # specific rotation/scale to each echo layer.
        print(f"Echo {i} created. Apply {rotation_step * i} degree rotation and scale!")

spiral_symmetry()