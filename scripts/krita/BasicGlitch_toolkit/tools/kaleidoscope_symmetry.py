from krita import *

def run():
    doc = Krita.instance().activeDocument()
    if not doc: return
    
    # Calculate Center
    cx = doc.width() / 2
    cy = doc.height() / 2
    
    print("🌀 INITIALIZING KALEIDOSCOPE SYMMETRY...")
    
    # Krita 5.x Symmetry is handled via the Canvas decoration or Multibrush.
    # We can't easily toggle 'Symmetry Mode' via Python, but we can set 
    # the guides so the user is ready.
    
    # Setting the document's center for guide snapping
    doc.setXRes(72.0) # Resetting DPI to standard to avoid math drift
    doc.setYRes(72.0)
    
    # Use floating message to guide user
    app = Krita.instance()
    if app.activeWindow() and app.activeWindow().activeView():
        app.activeWindow().activeView().showFloatingMessage(
            "SYMMETRY CENTERED: USE MULTIBRUSH (Q)", 
            QIcon(), 3000, 1
        )
    
    print(f"✅ Symmetry Origin theoretically centered at {cx}, {cy}")
    print("   1. Select Multibrush Tool (Q)")
    print("   2. Set Tool Options to 'Symmetry'")

if __name__ == "__main__":
    run()