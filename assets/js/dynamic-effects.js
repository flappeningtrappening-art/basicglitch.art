/* ========================================================
   dynamic-effects.js
   Handles header neon colors and gallery card border logic.
   Broboticus spawning and animation removed by request.
======================================================== */

/* -------------------------------
   CONFIGURATION
-------------------------------- */
const headerColors = {
  'glitch-circuit': '--neon-2',      // green
  'mountains': '--neon-mag',         // magenta
  'default': '--neon-blu'            // fallback blue
};

const styleColors = {
  'Neon': '--neon-yel',
  'Psychedelia': '--neon-pur',
  'Surrealism': '--neon-blu',
  'Broboticus': '--neon-org',
  'Animation': '--neon-mag',
  'Geometric': '--neon',
  'Glitch': '--neon-2',
  'Landscape': '--neon-limon'
};

const categoryBorderColors = {
  'personal-project': 'var(--neon-pur)',
  'broboticus': 'var(--neon-org)',
  'for-sale': 'var(--neon)'
};

/* -------------------------------
   UTILITY FUNCTIONS
-------------------------------- */
function setCSSVar(element, varName, value) {
  if (!element) return;
  element.style.setProperty(varName, value);
}

/* -------------------------------
   HEADER NEON DYNAMIC COLOR
-------------------------------- */
function updateHeaderNeon() {
  const headerTitle = document.querySelector('.brand');
  const hero = document.querySelector('#hero');

  if (!headerTitle || !hero) return;

  const bgType = hero.dataset.bg || 'default';
  const neonVar = headerColors[bgType] || headerColors['default'];
  setCSSVar(headerTitle, 'color', `var(${neonVar})`);
}

/* -------------------------------
   GALLERY CARD BORDER COLORS
-------------------------------- */
function updateGalleryBorders() {
  const cards = document.querySelectorAll('.gallery-card');

  cards.forEach(card => {
    const style = card.dataset.style;
    const category = card.dataset.category;

    const styleColorVar = styleColors[style] || '--neon';
    const img = card.querySelector('img');

    if (img) {
      img.style.borderColor = `var(${styleColorVar})`;
      img.style.borderWidth = '2px';
      img.style.borderStyle = 'solid';
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
