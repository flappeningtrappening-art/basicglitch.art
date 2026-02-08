from krita import *
from PyQt5.QtGui import QColor

def run():
    """Main function called by Krita - DO NOT RENAME"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        # Create warning message
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No document open!")
        msg.setInformativeText("Please open or create a document first.")
        msg.setWindowTitle("BasicGlitch - Quantum Quadrants")
        msg.exec_()
        return
    
    root = doc.rootNode()
    
    # Create a Group for the Quantum Effect
    group = doc.createGroupLayer("SYSTEM: Quantum Quadrants")
    root.addChildNode(group, None)
    
    # 1. The Source Layer - CORRECTED METHOD
    source = doc.createNode("QUADRANT 1: Source (Draw Here)", "paintlayer")
    source.setBlendingMode("normal")
    source.setOpacity(100)
    group.addChildNode(source, None)
    
    # 2. Create guide layers with colored borders
    colors = [
        ("QUADRANT 2: Mirror H", QColor(255, 100, 100, 77)),  # Red, 30% opacity
        ("QUADRANT 3: Mirror V", QColor(100, 255, 100, 77)),  # Green, 30% opacity
        ("QUADRANT 4: Rotate 180", QColor(100, 100, 255, 77))  # Blue, 30% opacity
    ]
    
    for name, color in colors:
        guide = doc.createNode(name, "paintlayer")
        guide.setBlendingMode("normal")
        guide.setOpacity(30)
        group.addChildNode(guide, source)
    
    # Optional: Select the source layer
    doc.setActiveNode(source)
    
    # Print to Krita's scripting console
    print("\n" + "="*50)
    print("QUANTUM QUADRANTS SETUP COMPLETE")
    print("="*50)
    print("✅ Created 'SYSTEM: Quantum Quadrants' group")
    print("✅ Layer 1: 'QUADRANT 1: Source (Draw Here)' - Draw here")
    print("✅ Layers 2-4: Guide layers (30% opacity, colored)")
    print("\nHOW TO USE:")
    print("1. Draw in the 'Source' layer")
    print("2. Duplicate it 3 times (Ctrl+J)")
    print("3. Apply transformations:")
    print("   • Copy → Layer → Transform → Mirror Layer Horizontally")
    print("   • Copy → Layer → Transform → Mirror Layer Vertically")
    print("   • Copy → Layer → Transform → Rotate 180°")
    print("\nRESULT: Non-Euclidean 'Impossible' Symmetry")

# Optional: Add alternative function names for compatibility
def main():
    """Alternative entry point"""
    run()

def execute():
    """Alternative entry point"""
    run()
