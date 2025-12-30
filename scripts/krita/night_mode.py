from krita import *

def night_mode_refined():
    doc = Krita.instance().activeDocument()
    filt = doc.createFilterLayer("ATMOSPHERE: Night Mode", "colorbalance", InfoObject())
    doc.rootNode().addChildNode(filt, None)
    print("Night Mode Filter Layer added.")

night_mode_refined()
