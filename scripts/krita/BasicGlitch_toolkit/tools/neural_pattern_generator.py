from krita import *
from PyQt5.QtWidgets import QMessageBox
import traceback

def run():
    """Neural Pattern Generator: Optimized for Krita 5"""
    app = Krita.instance()
    doc = app.activeDocument()
    if not doc:
        QMessageBox.warning(None, "BasicGlitch", "No document open!")
        return

    print("🧠 GENERATING NEURAL PATTERN...")
    
    try:
        from krita import InfoObject
        config = InfoObject()
        config.setProperty("grid_size", 20)
        config.setProperty("line_width", 1.0)
        
        # Fixed for Krita 5.2: requires (name, generator, info, selection)
        empty_selection = Selection()
        
        # Create a procedural noise layer to simulate "neural" structures
        # Strategy: Use multiple IDs if one fails (like in fractal_generator)
        layer = None
        for proto_id in ["simplex_noise", "noise", "simplexnoise"]:
            try:
                layer = doc.createFillLayer("TECH: Neural Pattern", proto_id, config, empty_selection)
                if layer:
                    print(f"   ✅ Found Generator ID: {proto_id}")
                    break
            except:
                continue
        
        if layer:
            layer.setBlendingMode("soft_light")
            layer.setOpacity(100)
            doc.rootNode().addChildNode(layer, None)
            print("✅ Neural Pattern generated.")
            doc.refreshProjection()
        else:
            print("   ⚠️ Failed to manifest Neural Pattern layer.")
        
    except Exception as e:
        error_msg = f"❌ Pattern Gen Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        QMessageBox.critical(None, "BasicGlitch Error", error_msg)

if __name__ == "__main__":
    run()
