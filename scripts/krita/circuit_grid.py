from krita import *

def tech_grid_refined():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    # Creates a dedicated vector layer for technical detailing and grids
    grid = doc.createVectorLayer("TECH: Background Grid")
    grid.setOpacity(150) # Approx 60%
    doc.rootNode().addChildNode(grid, None)
    
    print("[SUCCESS] Tech Vector Layer Created.")
    print("Use the 'Grid' or 'Line' tools on this layer for mathematical precision.")

tech_grid_refined()
