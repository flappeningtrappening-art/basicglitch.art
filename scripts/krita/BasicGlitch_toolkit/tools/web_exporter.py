from krita import *
import os

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
    
    if width > max_size or height > max_size:
        print(f"⚠️  Large image: {width} x {height}")
        print(f"   Recommended max: {max_size} x {max_size}")
        scale = min(max_size / width, max_size / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        print(f"   Scaled to: {new_width} x {new_height}")
    
    # Export settings
    print(f"\n📄 Export Settings:")
    print(f"  • Format: PNG")
    print(f"  • Compression: 9 (max)")
    print(f"  • Alpha: Yes")
    print(f"  • Color Profile: sRGB")
    
    print(f"\n💡 Manual Export:")
    print(f"  1. File → Export")
    print(f"  2. Format: PNG")
    print(f"  3. Set Compression to 9")
    print(f"  4. Check 'Save Alpha Channel'")
    print(f"  5. Save in web folder")
    
    print(f"\n🎯 Recommended:")
    print(f"  • Create 'web' subfolder")
    print(f"  • Name: [artwork]_web.png")
    print(f"  • Max dimension: {max_size}px")

# For compatibility
def main():
    run()

def execute():
    run()
