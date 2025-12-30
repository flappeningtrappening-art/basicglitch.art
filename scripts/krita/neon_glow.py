from krita import *

def neon_stack_refined():
    doc = Krita.instance().activeDocument()
    base = doc.activeNode()
    if not doc or not base: return

    tight_blur = doc.width() * 0.005
    wide_blur = doc.width() * 0.02

    tight = base.duplicate()
    tight.setName("NEON: Tight")
    tight.setBlendingMode("screen")
    doc.rootNode().addChildNode(tight, base)

    wide = base.duplicate()
    wide.setName("NEON: Wide")
    wide.setBlendingMode("screen")
    wide.setOpacity(180)
    doc.rootNode().addChildNode(wide, tight)

    blur = Krita.instance().filter("gaussianblur")
    t_conf = blur.configuration()
    t_conf.setProperty("horizAmount", tight_blur)
    t_conf.setProperty("vertAmount", tight_blur)
    
    w_conf = blur.configuration()
    w_conf.setProperty("horizAmount", wide_blur)
    w_conf.setProperty("vertAmount", wide_blur)
    
    blur.apply(tight, 0, 0, doc.width(), doc.height(), t_conf)
    blur.apply(wide, 0, 0, doc.width(), doc.height(), w_conf)
    doc.refreshProjection()
    print("Neon stack applied.")

neon_stack_refined()
