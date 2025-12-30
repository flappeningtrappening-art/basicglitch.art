import random

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
    print("--- BasicGlitch Palette Generator ---")
    selection = random.sample(list(hues.items()), 3)
    for name, code in selection:
        print(f"[*] {name}: {code}")
    print(f"[*] Void Base: #050505")
    print(f"[*] Static highlight: #e6eef8")

generate_palette()
