from krita import *
import colorsys
import random

def run():
    """Generate quantum color harmonies"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    print("🌈 QUANTUM COLOR HARMONY")
    print("=" * 40)
    
    # Base colors for cyber-surrealism
    base_palettes = {
        "teal_pink": ["#0a9396", "#94d2bd", "#ee9b00", "#bb3e03", "#9b2226"],
        "amber_blue": ["#001219", "#005f73", "#0a9396", "#94d2bd", "#e9d8a6"],
        "matrix_green": ["#003b00", "#008f11", "#00ff41", "#b5ff00", "#ffff00"],
        "cyber_violet": ["#240046", "#3c096c", "#5a189a", "#7b2cbf", "#9d4edd"],
        "neon_dystopia": ["#ff9e00", "#ff0055", "#00ffcc", "#7700ff", "#000000"]
    }
    
    # Select random palette
    palette_name = random.choice(list(base_palettes.keys()))
    colors = base_palettes[palette_name]
    
    # Create variations (quantum superposition)
    variations = []
    for hex_code in colors[:3]:  # First 3 colors only
        rgb = tuple(int(hex_code[i:i+2], 16) for i in (1, 3, 5))
        h, l, s = colorsys.rgb_to_hls(*[x/255 for x in rgb])
        
        # Create 2 variations
        for i in range(2):
            h_var = (h + random.random() * 0.1 - 0.05) % 1.0
            s_var = min(1.0, max(0, s + random.random() * 0.2 - 0.1))
            l_var = min(1.0, max(0, l + random.random() * 0.15 - 0.075))
            
            r_var, g_var, b_var = colorsys.hls_to_rgb(h_var, l_var, s_var)
            hex_var = '#{:02x}{:02x}{:02x}'.format(
                int(r_var * 255),
                int(g_var * 255),
                int(b_var * 255)
            )
            variations.append(hex_var)
    
    # Display results
    print(f"🎯 Selected Palette: {palette_name}")
    print(f"\n🎨 Base Colors:")
    for i, color in enumerate(colors, 1):
        print(f"  {i}. {color}")
    
    print(f"\n🌀 Quantum Variations:")
    for i, color in enumerate(variations, 1):
        print(f"  {i}. {color}")
    
    print(f"\n💡 Usage Tips:")
    print("  • Use base colors for main elements")
    print("  • Use variations for accents/details")
    print("  • Try different blend modes (overlay, screen, color dodge)")

# For compatibility
def main():
    run()

def execute():
    run()
