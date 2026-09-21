"""Generate card-sized webp variants of raw images for preview slots.

Hand-authored pages show raw images inside small preview containers (archive
cards, portfolio strips, insta grid). Chrome's lazy-load distance threshold
still fetches near-viewport "lazy" images at page load on mobile, so serving
full-res (up to 2880px) into ~350px cards wrecks LCP for no visual gain.

This writes assets/images/card/<same-name>.webp at <= 800px (2x a card at
retina), skipping files that are already small enough. Art pages keep
pointing at assets/images/raw/ for the full-resolution view, and wallpaper
downloads are untouched.

Usage: python3 scripts/make_card_images.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "images", "raw")
CARD = os.path.join(ROOT, "assets", "images", "card")
MAX_DIM = 800

# Every raw image referenced as a *preview* by hand-authored pages
# (index archive cards + insta feed pool + download-wallpapers previews).
NAMES = [
    "fishboticus", "sunflowerboticus", "pup-fiction-scene1", "sangre_de_cristo_dusk",
    "skyline_reclaimation", "discworld", "dust_to_dust", "loveofthegame", "spiral_geometry",
    "gaia_of_the_wasteland", "guitarbot_og", "artist_broboticus_og", "starbot_waiting_in_the_sky",
    "a_mycological_phenomenon", "floral", "ranchboticus", "balletboticus", "vitruvian_broboticus",
    "brobotosaurus_wrex", "cubist_chef", "mycology_yourcology", "pachydermis", "karateboticus1",
    "chefboticus", "aesthetic_sangre_de_cristo", "literal_traphouse", "aesthetic_laser_colorado",
    "apex_rendering", "monument_memory", "sentinel_stream", "screambot", "marilyn_monbroe",
    "sangre_de_cristo_midnight_v2",
]


def main():
    os.makedirs(CARD, exist_ok=True)
    made = skipped = missing = 0
    for name in NAMES:
        src = os.path.join(RAW, name + ".webp")
        dst = os.path.join(CARD, name + ".webp")
        if not os.path.exists(src):
            print("missing raw:", name)
            missing += 1
            continue
        with Image.open(src) as im:
            w, h = im.size
            if max(w, h) <= MAX_DIM:
                skipped += 1
                continue
            scale = MAX_DIM / max(w, h)
            nw, nh = round(w * scale), round(h * scale)
            resized = im.resize((nw, nh), Image.LANCZOS)
            resized.save(dst, "WEBP", quality=80, method=6)
        made += 1
    print(f"generated {made}, already-small {skipped}, missing {missing}")


if __name__ == "__main__":
    main()
