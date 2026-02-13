from krita import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
import random
import traceback

def run():
    """Create fractal detail layers using fixed Krita 5 Noise Generators - V5 VISIBILITY FIX"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return
    
    print("🌀 GENERATING FRACTAL DETAILS (V5 - VISIBILITY & PROPERTY FIX)...")
    
    try:
        root = doc.rootNode()
        
        # 1. Create a unique group name
        group_id = random.randint(100, 999)
        group_name = f"FX_Fractal_Bundle_{group_id}"
        group = doc.createGroupLayer(group_name)
        root.addChildNode(group, None)
        
        empty_selection = Selection()
        
        # --- LAYER 1: PERLIN ---
        perlin = None
        # Trying 'noise' which is the standard ID for Perlin in Krita 5
        try:
            conf = InfoObject()
            conf.setProperty("frequency", 4.0)
            conf.setProperty("detail", 5)
            perlin = doc.createFillLayer(f"FRACTAL: Perlin ({group_id})", "noise", conf, empty_selection)
            if perlin:
                perlin.setBlendingMode("normal") # Normal mode so it's visible
                perlin.setOpacity(255) 
                group.addChildNode(perlin, None)
                print("   ✅ Manifested: Perlin")
        except:
            print("   ⚠️ Perlin 'noise' ID failed.")

        # --- LAYER 2: SIMPLEX ---
        try:
            conf2 = InfoObject()
            conf2.setProperty("frequency", 12.0)
            conf2.setProperty("seed", random.randint(0, 9999))
            simplex = doc.createFillLayer(f"FRACTAL: Simplex ({group_id})", "simplex_noise", conf2, empty_selection)
            if simplex:
                simplex.setBlendingMode("normal")
                simplex.setOpacity(255)
                group.addChildNode(simplex, None)
                print("   ✅ Manifested: Simplex")
        except:
            print("   ⚠️ Simplex ID failed.")

        # --- LAYER 3: THE GRID (The ultimate visibility check) ---
        try:
            conf3 = InfoObject()
            conf3.setProperty("color", QColor(0, 255, 255))
            conf3.setProperty("grid_size", 50)
            conf3.setProperty("line_width", 2.0) # Added
            conf3.setProperty("subdivision", 1)  # Added
            
            grid = doc.createFillLayer(f"FRACTAL: Grid Check ({group_id})", "grid", conf3, empty_selection)
            if grid:
                grid.setBlendingMode("normal")
                grid.setOpacity(255)
                grid.setVisible(True)
                group.addChildNode(grid, None)
                print("   ✅ Manifested: Grid Check")
        except:
            print("   ⚠️ Grid ID failed.")
            
        QMessageBox.information(None, "BasicGlitch", 
            f"Sequence {group_id} Complete.\n\n"
            "NOTE: 'FX_Fractal_Bundle' is a GROUP folder.\n"
            "Click the arrow next to it in the Layers docker to see the noise layers inside!")
            
    except Exception as e:
        error_msg = f"❌ Quantum Decoherence: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)
    
    doc.refreshProjection()

if __name__ == "__main__":
    run()