# BasicGlitch.art - Project Brain

## 1. Core Vision
A high-saturation, immersive digital portfolio for Justin Lance (BasicGlitch). The site serves as a gallery for "Neon Surrealism," "Tech-Noir," and psychedelic character design, blending 90s electronic aesthetics with modern web interactions.

## 2. Technical Stack
- **Frontend:** Vanilla HTML5, CSS3 (Custom Variables, Keyframe Animations), and Modern JavaScript.
- **Interactions:** Custom 3D CSS transforms for commission cards, perspective-based hover effects.
- **Visuals:** SVG filters, backdrop-filters for glassmorphism (where applicable), and dual-layered animated neon grids.

## 3. Key Features
- **The Neon Grid:** A signature animated background using `linear-gradient` and `background-size` to create a moving 3D floor effect.
- **Randomized Instagram Feed:** A client-side JavaScript engine that shuffles images from `assets/images/raw` to provide a dynamic "Social Feed" feel on every page load.
- **Cyber-Commission Tiers:** 4-tier service menu (Nano, Binary, Quantum, Singularity) with interactive 3D card flips.

## 4. Recent Updates & Fixes
- **About Page Refactor:**
    - Centered the Artist Avatar using explicit margin auto and flex alignment to fix desktop centering issues.
    - Simplified the Bio Container styling: moved from semi-transparent blue to `background: transparent` and `backdrop-filter: none` to allow the background grid to remain sharp and visible behind the text.
    - Integrated a neon border to maintain the "Cyber" aesthetic without obscuring background patterns.
- **Feed Logic:** Switched from a static 6-image grid to a shuffle algorithm that selects from 20+ assets in the `raw` directory.
- **Asset Cleanup:** Removed `glowspore.png` from the codebase and the shuffle rotation as per user request.

## 5. Maintenance Notes
- **Adding New Art to Feed:** Simply drop the new image into `assets/images/raw/` and add the filename to the `rawImages` array in `about.html`.
- **Styling Conventions:** All neon accents should use variables like `--neon` (Cyan), `--neon-mag` (Magenta), or `--neon-pur` (Purple) to ensure site-wide consistency.
