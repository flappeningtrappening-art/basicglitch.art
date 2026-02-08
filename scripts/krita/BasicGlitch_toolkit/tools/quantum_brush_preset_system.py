from krita import *

def run():
    """Quantum Brush Preset System: Smart Brush Switching"""
    app = Krita.instance()
    
    # Krita resource management for brushes
    # We try to find brushes that fit the 'BasicGlitch' aesthetic
    aesthetic_keywords = ["glitch", "noise", "circuit", "tech", "pixel", "marker"]
    
    print("🖌️ QUANTUM BRUSH PRESET SYSTEM")
    print("=" * 40)
    
    all_presets = app.resources("preset")
    found_brushes = []
    
    for name, preset in all_presets.items():
        if any(kw in name.lower() for kw in aesthetic_keywords):
            found_brushes.append(name)
            
    if not found_brushes:
        print("? No specialized Glitch/Tech brushes found in your library.")
        print("  Recommendation: Tag your favorites with 'glitch' or 'tech'.")
        return

    # Pick a random brush from the 'aesthetic' list
    import random
    selected_brush = random.choice(found_brushes)
    
    # Activate the brush
    app.activeWindow().views()[0].setCurrentBrushPreset(all_presets[selected_brush])
    
    print(f"✅ QUANTUM STATE COLLAPSED: Brush Selected")
    print(f"   • Active Brush: {selected_brush}")
    print(f"   • Aesthetic match: Verified")
    
    # Notify user
    app.activeWindow().activeView().showFloatingMessage(
        f"BRUSH SYNCED: {selected_brush}", 
        QIcon(), 2000, 1
    )

if __name__ == "__main__":
    run()