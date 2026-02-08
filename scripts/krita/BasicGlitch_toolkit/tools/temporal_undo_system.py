from krita import *
import time
import os

def run():
    """Create a high-speed temporal snapshot of the current document"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("Error: No active document for temporal snapshot.")
        return
    
    print("⏳ TEMPORAL UNDO SYSTEM - SNAPSHOT START")
    
    # Define snapshot directory
    # We save to the project's 'notes/snapshots' for cross-partition safety
    snapshot_dir = os.path.expanduser("~/monetization/basic-glitch-art/notes/snapshots/")
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)
        
    # Create unique timestamped filename
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    doc_name = doc.name().split('.')[0].replace(' ', '_').lower()
    filename = f"snapshot_{doc_name}_{timestamp}.kra"
    full_path = os.path.join(snapshot_dir, filename)
    
    # Save a background copy
    # Note: saveAs returns True/False
    doc.setBatchmode(True)
    success = doc.saveAs(full_path)
    
    if success:
        print(f"✅ TEMPORAL SNAPSHOT SECURED")
        print(f"   • Path: {full_path}")
        print(f"   • Restore Point: {timestamp}")
        
        # UI notification
        MessageBox = Krita.instance().messageBox
        MessageBox(f"Temporal Snapshot Secured!\n\nFile: {filename}\nStored in /notes/snapshots/", "Success")
    else:
        print(f"❌ FAILED TO SECURE SNAPSHOT")

if __name__ == "__main__":
    run()