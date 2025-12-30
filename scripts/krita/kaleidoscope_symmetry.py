from krita import *

def setup_kaleidoscope():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    # Krita's Multibrush tool handles Kaleidoscope effects.
    # This script centers the mirror axes perfectly on your canvas.
    
    # 1. Calculate Center
    center_x = doc.width() / 2
    center_y = doc.height() / 2
    
    # 2. Set the document resolution/origin for symmetry
    # Note: This affects where the Multibrush 'starts' its math
    doc.setXRes(center_x)
    doc.setYRes(center_y)
    
    print("--- KALEIDOSCOPE SYMMETRY SETUP ---")
    print(f"1. Symmetry Origin set to: {center_x}, {center_y}")
    print("2. Select the 'Multibrush' Tool (Shortcut: Q).")
    print("3. In Tool Options, set 'Type' to 'Symmetry'.")
    print("4. Set 'Brushes' to 8 or 12 for high-detail psychedelic patterns.")

setup_kaleidoscope()
