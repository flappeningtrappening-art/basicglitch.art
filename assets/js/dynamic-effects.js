/* ========================================================
   dynamic-effects.js
   Handles header neon colors and gallery card border logic.
======================================================== */

/* -------------------------------
   CONFIGURATION & LOOKUP TABLE
-------------------------------- */
const headerColors = {
  // Map keys from app.js to the actual CSS variables
  'glitch1': '--neon-limon',
  'glitch2': '--neon',
  'glitch3': '--neon-mag',
  'glitch-default': '--neon-pur',
  
  // FIX 1: You must define the 'default' key for the fallback logic to work
  'default': '--neon-2' // Use the color variable you want for the fallback here
};


/* -------------------------------
   MAIN EFFECT LOGIC
-------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Define the elements needed to run the effect
    //    (This fixes the "hero is not defined" error)
    const hero = document.getElementById('hero');
    const headerTitle = document.querySelector('.title'); // Check this selector in index.html

    // Safety check: ensure required elements exist AND setCSSVar is available (from app.js)
    if (hero && headerTitle && typeof setCSSVar === 'function') {
        
        // 2. Read the color key set by app.js (e.g., 'glitch1')
        const bgType = hero.dataset.bg || 'default';
        
        // 3. Look up the CSS variable (e.g., '--neon-limon') using the key
        const neonVar = headerColors[bgType] || headerColors['default'];

        // 4. Apply the color variable to the title element
        //    (setCSSVar must be defined in app.js)
        setCSSVar(headerTitle, 'color', `var(${neonVar})`);
    }
});
/* -------------------------------
   GALLERY CARD BORDER COLORS
-------------------------------- */
function updateGalleryBorders() {
  const cards = document.querySelectorAll('.gallery-card');

  cards.forEach(card => {
    const style = card.dataset.style || '';
    const category = card.dataset.category || '';

    const styleColorVar = styleColors[style] || '--fg';
    const img = card.querySelector('img');

    if (img) {
      img.style.border = `2px solid var(${styleColorVar})`;
    }

    const cardColor = categoryBorderColors[category] || 'var(--fg)';
    card.style.border = `2px solid ${cardColor}`;
  });
}

/* -------------------------------
   INITIALIZATION
-------------------------------- */
function initDynamicEffects() {
  updateHeaderNeon();
  updateGalleryBorders();
}

/* Run on DOM ready */
document.addEventListener('DOMContentLoaded', initDynamicEffects);
