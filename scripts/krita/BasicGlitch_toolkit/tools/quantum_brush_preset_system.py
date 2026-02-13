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
        print("? No specialized Glitch/Tech brushes found. Checking fallbacks...")
        aesthetic_keywords = ["digital", "ink", "paint", "airbrush"]
        for name, preset in all_presets.items():
            if any(kw in name.lower() for kw in aesthetic_keywords):
                found_brushes.append(name)
                
    if not found_brushes:
        print("❌ No brushes matched any criteria.")
        return

    # Pick a random brush
    import random
    selected_brush = random.choice(found_brushes)
    
    # Activate the brush
    window = app.activeWindow()
    if window and window.views():
        window.views()[0].setCurrentBrushPreset(all_presets[selected_brush])
        
        # Notify user via status bar fallback
        print(f"✅ QUANTUM BRUSH SELECTED: {selected_brush}")
        try:
            window.activeView().showFloatingMessage(f"BRUSH: {selected_brush}", QIcon(), 1500, 1)
        except:
            pass

if __name__ == "__main__":
    run()