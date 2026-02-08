from krita import *
from PyQt5.QtGui import QColor
import random
import colorsys
from krita import *
from PyQt5.QtGui import QColor

def is_neon_color(r, g, b):
    """Check if color has neon characteristics (high saturation + high brightness)"""
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return s > 0.7 and v > 0.8  # High saturation and brightness

def generate_neon_color():
    """Generate a random neon color"""
    # Start with fully saturated color
    hue = random.random()  # 0.0 to 1.0
    
    # Neon colors are high saturation (0.8-1.0) and high brightness (0.8-1.0)
    saturation = random.uniform(0.8, 1.0)
    brightness = random.uniform(0.8, 1.0)
    
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
    return QColor(int(r*255), int(g*255), int(b*255))

def generate_neon_palette(count=8):
    """Generate a palette of unique neon colors"""
    colors = []
    attempts = 0
    max_attempts = count * 10
    
    while len(colors) < count and attempts < max_attempts:
        color = generate_neon_color()
        
        # Ensure uniqueness (not too similar to existing colors)
        unique = True
        for existing in colors:
            # Calculate color difference
            diff = (abs(color.red() - existing.red()) + 
                   abs(color.green() - existing.green()) + 
                   abs(color.blue() - existing.blue()))
            if diff < 100:  # Colors too similar
                unique = False
                break
        
        if unique:
            colors.append(color)
        
        attempts += 1
    
    # If we couldn't get enough unique, fill with any neon
    while len(colors) < count:
        colors.append(generate_neon_color())
    
    return colors

def neon_color_name(color):
    """Generate descriptive name for neon color"""
    r, g, b = color.red(), color.green(), color.blue()
    hex_code = f"#{r:02x}{g:02x}{b:02x}"
    
    # Simple hue-based naming
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    hue_deg = int(h * 360)
    
    if hue_deg < 15 or hue_deg >= 345:
        hue_name = "Red"
    elif hue_deg < 45:
        hue_name = "Orange"
    elif hue_deg < 75:
        hue_name = "Yellow"
    elif hue_deg < 165:
        hue_name = "Green"
    elif hue_deg < 195:
        hue_name = "Cyan"
    elif hue_deg < 255:
        hue_name = "Blue"
    elif hue_deg < 285:
        hue_name = "Purple"
    else:
        hue_name = "Magenta"
    
    # Add intensity descriptor
    intensity = "Ultra" if v > 0.95 else "Bright" if v > 0.9 else "Neon"
    
    return f"{intensity} {hue_name} {hex_code}"

def run():
    """Generate a palette of true neon colors"""
    app = Krita.instance()
    
    # Generate neon colors (6-10 colors)
    color_count = random.randint(6, 10)
    neon_colors = generate_neon_palette(color_count)
    
    # Create palette
    palette = Palette(f"NEON GLOW Palette ({color_count} colors)")
    
    # Add neon colors
    for i, color in enumerate(neon_colors):
        name = neon_color_name(color)
        palette.addEntry(name)
        palette.setColor(i, color)
    
    # Add utility colors (black, white, dark gray for contrast)
    offset = len(neon_colors)
    
    palette.addEntry("╔ BLACK (contrast)")
    palette.setColor(offset, QColor(0, 0, 0))
    
    palette.addEntry("╠ WHITE (highlight)")
    palette.setColor(offset + 1, QColor(255, 255, 255))
    
    palette.addEntry("╚ DARK GRAY (shadows)")
    palette.setColor(offset + 2, QColor(30, 30, 30))
    
    # Save palette
    try:
        resource = app.resource("palette")
        if resource:
            resource.trigger()
        
        print(f"🎨 Created neon palette with {color_count} glowing colors")
        print("   Check: Window → Dockers → Resource Manager → Palettes")
        print(f"   Palette: '{palette.name()}'")
        
        # Show colors in console
        for i, color in enumerate(neon_colors):
            hex_code = f"#{color.red():02x}{color.green():02x}{color.blue():02x}"
            print(f"   {i+1}. {hex_code}")
            
    except Exception as e:
        print(f"Error saving palette: {e}")
        print(f"Palette created in memory: '{palette.name()}'")

# Test function
def test_neon():
    """Test neon color generation"""
    print("Testing neon color generation...")
    for _ in range(5):
        color = generate_neon_color()
        print(f"  #{color.red():02x}{color.green():02x}{color.blue():02x} - " +
              f"S:{colorsys.rgb_to_hsv(color.red()/255,color.green()/255,color.blue()/255)[1]:.2f} " +
              f"V:{colorsys.rgb_to_hsv(color.red()/255,color.green()/255,color.blue()/255)[2]:.2f}")
