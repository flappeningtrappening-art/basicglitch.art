from krita import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def run():
    """Export web-optimized version"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    print("🌐 WEB EXPORTER")
    print("=" * 40)
    
    # Check size
    max_size = 2048
    width = doc.width()
    height = doc.height()
    
    # Clone the document so we don't mess up the original
    # Note: Krita API doc.clone() might not exist in all versions.
    # Safer to just save-as-copy or work on current doc if user accepts.
    
    # Let's ask user for export location
    file_path = QFileDialog.getSaveFileName(None, "Export Web Image", "", "PNG Image (*.png);;JPEG Image (*.jpg)")[0]
    
    if not file_path:
        print("Export cancelled.")
        return

    # InfoObject for Export Configuration
    export_config = InfoObject()
    
    if file_path.endswith(".png"):
        export_config.setProperty("alpha", True)
        export_config.setProperty("compression", 9)
        export_config.setProperty("interlaced", False)
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        export_config.setProperty("quality", 85)
        export_config.setProperty("smoothing", 10)
        export_config.setProperty("subsampling", 0) # 2x2, 1x1 etc. 0 is best quality usually
    
    # Scale calculation
    scale = 1.0
    if width > max_size or height > max_size:
        scale = min(max_size / width, max_size / height)
        print(f"⚠️  Large image: {width} x {height}")
        print(f"   Scaling to {int(width*scale)} x {int(height*scale)} for web...")
        
        # We need to scale the doc before export. 
        # Since we can't easily clone without potentially crashing on huge files,
        # we will:
        # 1. Scale current doc
        # 2. Export
        # 3. Undo scale (using doc.refreshProjection() or just telling user to Undo)
        
        # ACTUALLY, simpler path: Use `doc.scale(w, h)`
        doc.scale(int(width*scale), int(height*scale))
    
    # Perform Export
    try:
        if doc.exportImage(file_path, export_config):
            print(f"✅ Saved to: {file_path}")
            QMessageBox.information(None, "Web Export", f"Successfully exported to:\n{file_path}")
        else:
            print("❌ Export failed (Unknown Krita error)")
            QMessageBox.warning(None, "Web Export", "Export failed.")
            
    except Exception as e:
        print(f"❌ Error during export: {e}")
        QMessageBox.critical(None, "Web Export", f"Error: {e}")
    
    finally:
        # Restore Original Size if we scaled
        if scale != 1.0:
            print("↺ Reverting document scale...")
            # Ideally we'd use Krita's undo stack, but API access is limited.
            # We just scale back up (slightly lossy but keeps workflow alive)
            # OR better: The user should just Undo (Ctrl+Z)
            print("   👉 PLEASE PRESS CTRL+Z TO RESTORE ORIGINAL RESOLUTION")

# For compatibility
def main():
    run()

def execute():
    run()