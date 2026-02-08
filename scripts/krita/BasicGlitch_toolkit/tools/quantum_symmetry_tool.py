from krita import *
import random

def run():
    """Setup quantum symmetry for drawing"""
    app = Krita.instance()
    doc = app.activeDocument()
    
    if not doc:
        print("No document open")
        return
    
    print("🌀 QUANTUM SYMMETRY TOOL")
    print("=" * 40)
    
    # Calculate center
    center_x = doc.width() / 2
    center_y = doc.height() / 2
    
    # Generate symmetry parameters
    axes = random.choice([4, 6, 8, 12])
    noise_factor = random.uniform(0.1, 0.3)
    
    print(f"🎯 Symmetry Setup:")
    print(f"  • Center: ({center_x:.0f}, {center_y:.0f})")
    print(f"  • Axes: {axes}")
    print(f"  • Quantum Noise: {noise_factor:.2f}")
    
    print(f"\n🔧 Manual Setup:")
    print(f"  1. Select Multibrush Tool (Q)")
    print(f"  2. In Tool Options:")
    print(f"     • Type: 'Mirror' or 'Snowflake'")
    print(f"     • Brushes: {axes}")
    print(f"     • Center: ({center_x:.0f}, {center_y:.0f})")
    
    print(f"\n💡 Quantum Variations:")
    print(f"  • Adjust center slightly for imperfect symmetry")
    print(f"  • Try different axes counts")
    print(f"  • Rotate the symmetry center while drawing")

# For compatibility
def main():
    run()

def execute():
    run()
