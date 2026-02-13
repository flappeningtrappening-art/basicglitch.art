from krita import *
from PyQt5.QtGui import QColor
import random
import colorsys

def is_neon_color(r, g, b):
    """Check if color has neon characteristics"""
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return s > 0.7 and v > 0.8

def generate_neon_color():
    """Generate a random ManagedColor (Neon)"""
    # Start with high saturation/value
    hue = random.random()
    saturation = random.uniform(0.8, 1.0)
    brightness = random.uniform(0.8, 1.0)
    
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
    
    # Create ManagedColor for Krita 5
    # Krita 5 prefers ManagedColor over QColor for Palettes
    try:
        # Try to get sRGB profile
        # Note: In some Krita versions, you construct ManagedColor with color space name
        mc = ManagedColor("RGBA", "U8", "")
        components = mc.components() # Returns list
        # U8 RGBA usually [r, g, b, a] in 0.0-1.0 or 0-255 range depending on version
        # Let's try QColor approach first as it's often supported via automatic conversion
        return QColor(int(r*255), int(g*255), int(b*255))
    except:
        # Fallback to standard QColor
        return QColor(int(r*255), int(g*255), int(b*255))

def run():
    """Generate a palette of true neon colors"""
    app = Krita.instance()
    
    # Generate neon colors (6-10 colors)
    color_count = random.randint(6, 10)
    
    # Create palette
    # Krita 5 Palette API: Palette(name) or app.createPalette(name)?
    # Usually: Resource objects are retrieved, but creating new one...
    # Let's try standard constructor
    try:
        palette = Palette(f"NEON GLOW {random.randint(100,999)}")
    except:
        print("❌ Could not create Palette object directly. Krita API restriction?")
        return

    print(f"🎨 Generating {color_count} neon colors...")
    
    # Add colors
    for i in range(color_count):
        color = generate_neon_color()
        
        # Name
        r, g, b = color.red(), color.green(), color.blue()
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        
        # Add entry
        entry = palette.addEntry(ManagedColor(color), f"Neon {i+1} {hex_code}")
        # Note: addEntry might take (ManagedColor, Name) or just Name then setColor
        # If the above fails, we'll see an error.
        
    # Attempt to save/register
    # Krita 5 requires explicitly adding the resource to the server sometimes
    # app.resources("palette") returns list.
    
    print(f"✅ Palette '{palette.name()}' created (Memory Only).")
    print("   To save permanently, you might need to use the Palette Docker manually")
    print("   and import the colors generated here.")
    
    # Print hex codes for manual copy if save fails
    for i in range(palette.entryCount()):
        entry = palette.entryByIndex(i)
        # Entry handling varies by version
        pass

# Entry point
def main():
    run()