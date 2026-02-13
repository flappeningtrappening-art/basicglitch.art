# BasicGlitch Toolkit

**Version:** 2.0 (Quantum Edition)  
**Author:** Justin Lance (BasicGlitch)  
**Compatibility:** Krita 5.2+ (Windows/Linux)

The **BasicGlitch Toolkit** is a specialized Python plugin suite for Krita, designed to automate the creation of "Tech-Noir," "Cyber-Eclectic," and "Glitch Art" aesthetics. It streamlines the workflow from initial composition to web export.

---

## 🚀 How to Use
1.  **Open Krita** and open a document.
2.  Go to the menu: **Tools -> Scripts -> Basic Glitch**.
3.  Select any tool from the list to run it instantly.

---

## 🎨 Creative Tools (Generators & Effects)

### 🌀 Glitch & Distortion
*   **Quantum Glitch Generator:**
    *   **Effect:** Creates a "Quantum Glitch" group with Red, Green, and Blue offset layers (chromatic aberration) plus scanlines.
    *   **Use For:** Instant "bad signal" effects.
*   **Quantum Waveforms:**
    *   **Effect:** Generates complex interference patterns using overlapping "alternating" gradients (Carrier, Modulator, and Radial passes).
    *   **Use For:** Creating mathematical textures, "frequency" backgrounds, and moire-style glitch effects.
*   **Fractured Mirror:**
    *   **Effect:** Duplicates the active layer, mirrors it to the right half, and shifts it vertically by 20px.
    *   **Use For:** Creating non-perfect symmetrical compositions with a "broken" look.
*   **RGB Glitch:**
    *   **Effect:** Creates a duplicate layer set to "Addition" mode and shifts it horizontally.
    *   **Use For:** Simple, quick chromatic aberration.
*   **CRT Scanlines:**
    *   **Effect:** Generates a procedural Fill Layer with horizontal scanlines (multiply blend).
    *   **Use For:** Retro TV / Monitor aesthetic.

### 🖌️ Styling & Atmosphere
*   **Neural Style Transfer Bridge:**
    *   **Effect:** Generates a "Neural Processing" group with 3 passes: Structure (Edge Detect), Color (Random HSV Shift), and Dissonance (Pixelize).
    *   **Use For:** Adding complex, AI-like texture and noise to a flat image.
*   **Neon Glow:**
    *   **Effect:** Creates two duplicate layers set to "Screen" mode for "Tight" and "Wide" glow.
    *   **Use For:** Making bright objects look like neon lights. *Note: You must manually apply Gaussian Blur to these layers.*
*   **Fractal Detail Generator:**
    *   **Effect:** Generates procedural noise layers (Simplex, Perlin, Grid) set to Overlay mode.
    *   **Use For:** Adding high-frequency detail and texture to "tech" surfaces.
*   **Adaptive Tech Noir Gradient Mapper:**
    *   **Effect:** Adds a "Tech-Noir" (Dark Blue to Light Blue) gradient overlay.
    *   **Use For:** Unifying the color palette of a composition.
*   **Night Mode:**
    *   **Effect:** Adds a dark blue tint layer (Multiply).
    *   **Use For:** Quickly converting a day scene to a night scene.

### 📐 Composition & Layout
*   **Quantum Quadrants:**
    *   **Effect:** Sets up a 4-layer symmetry guide system (Source, Mirror H, Mirror V, Rotate 180).
    *   **Use For:** Creating complex mandalas or "impossible" geometry.
*   **Kaleidoscope Symmetry:**
    *   **Effect:** Centers the document origin for perfect symmetry.
    *   **Use For:** Prepping the canvas for the **Multibrush Tool (Q)**.
*   **Recursive Vortex:**
    *   **Effect:** Creates a group of 6 duplicates, each rotated 45° and scaled down 90%.
    *   **Use For:** Spirals, tunnels, and "falling" effects.
*   **Dimensional Composition Assistant:**
    *   **Effect:** Scans your layers and auto-groups them into categories (Background, Character, Tech, etc.) based on their names.
    *   **Use For:** Cleaning up a messy layer stack.

---

## 🛠️ Production Utilities

### 💾 Export & Pipeline
*   **Foundry Exporter:**
    *   **Action:** Exports the current document in 3 formats: **RAW** (Original PNG), **WEB** (Max 2500px PNG), and **THUMB** (Max 600px JPG).
    *   **Dest:** Saves directly to the Shared Drive (`.../foundry_transfer/`) for Linux processing.
*   **Web Exporter:**
    *   **Action:** Interactive export dialog. Auto-scales large images to 2048px max dimension and sets optimal web settings (PNG/JPG).
    *   **Use For:** Quick posting to social media/web.

### ⚙️ Workflow Enhancers
*   **Master Apparel:**
    *   **Action:** Creates a hidden group with accurate template guides for Hoodies, Tapestries, Caps, etc.
    *   **Use For:** Designing merchandise.
*   **Palette Gen:**
    *   **Action:** Generates a new color palette with random, mathematically verified "Neon" colors (High Saturation/Value).
*   **Metadata Stamper:**
    *   **Action:** Injects "Justin Lance / BasicGlitch" copyright info into the document metadata.
*   **Temporal Undo System:**
    *   **Action:** Saves a timestamped snapshot (`.kra`) of the current document to the `snapshots` folder.
    *   **Use For:** "Save State" functionality before trying a risky experiment.
*   **Quantum Brush Preset System:**
    *   **Action:** Randomly selects a brush tagged with "glitch," "tech," or "noise" (or a fallback).
    *   **Use For:** Breaking creative block by forcing a tool change.

---

## 📦 Installation
(If moving to a new machine)
1.  Copy the `BasicGlitch_toolkit` folder and `kritapykrita_BasicGlitch_toolkit.desktop` file.
2.  Place them in your Krita User Resources folder:
    *   **Windows:** `%AppData%\krita\pykrita`
    *   **Linux:** `~/.local/share/krita/pykrita/`
3.  Enable in **Settings -> Configure Krita -> Python Plugin Manager**.
4.  Restart Krita.
