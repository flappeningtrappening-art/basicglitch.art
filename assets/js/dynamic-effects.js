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
  'default': '--neon-2'
};

const styleColors = {
  // Define your style mappings here
  'Neon': '--neon',
  'Character': '--neon-2',
  'Landscape': '--neon-mag'
  // Add more as needed
};

const categoryBorderColors = {
  // Define your category mappings here
  'Available for Purchase': 'var(--neon-limon)',
  'Broboticus': 'var(--neon-pur)'
  // Add more as needed
};

/* -------------------------------
   HEADER NEON UPDATE FUNCTION
-------------------------------- */
function updateHeaderNeon() {
  const hero = document.getElementById('hero');
  const headerTitle = document.querySelector('.title'); // Adjust selector if needed

  if (hero && headerTitle && typeof setCSSVar === 'function') {
    const bgType = hero.dataset.bg || 'default';
    const neonVar = headerColors[bgType] || headerColors['default'];
    
    setCSSVar(headerTitle, 'color', `var(${neonVar})`);
  }
}

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
