#!/usr/bin/env python3
import random

# These are your 8 signature site colors
hues = {
    "Neon Cyan": "#00fff7",
    "Neon Magenta": "#ff1ccf",
    "Neon Green": "#00ff3e",
    "Neon Orange": "#ff5f1f",
    "Neon Lime": "#d0ff00",
    "Neon Blue": "#0a7aff",
    "Neon Yellow": "#ffff00",
    "Neon Purple": "#c724ff"
}

def generate_palette():
    print("\n--- BasicGlitch Palette Generator ---")
    
    # Select 3 random signature colors
    selection = random.sample(list(hues.items()), 3)
    
    for name, code in selection:
        # Add a block character to show color if terminal supports it
        print(f"[*] {name}: {code}")
    
    print(f"[*] Void Base: #050505")
    print(f"[*] Static highlight: #e6eef8")
    print("-" * 35 + "\n")

if __name__ == "__main__":
    generate_palette()
