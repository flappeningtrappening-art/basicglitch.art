/* ========================================================
   dynamic-effects.js
   Handles header neon colors and gallery card border logic.
======================================================== */

/* -------------------------------
   CONFIGURATION
-------------------------------- */
const headerColors = {
  'glitch-circuit': '--neon-2',      
  'mountains': '--neon-mag',         
  'default': '--neon-blu'            
}; // fallback to 'default' if dataset.bg is missing
  const bgType = hero.dataset.bg || ['default'];
  const neonVar = headerColors[bgType] || headerColors['default'];
  setCSSVar(headerTitle, 'color', `var(${neonVar})`);

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
