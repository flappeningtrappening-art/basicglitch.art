/* ========================================================
   dynamic-effects.js (PATCHED SAFE VERSION)
   Stable neon styling without visual chaos
======================================================== */

/* -------------------------------
   CONFIGURATION
-------------------------------- */
const headerColors = {
  'glitch-circuit': '--neon-2',
  'mountains': '--neon-mag',
  'default': '--neon-blu'
};

const styleColors = {
  'Neon': '--neon-yel',
  'Psychedelia': '--neon-pur',
  'Surrealism': '--neon-blu',
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
   HEADER NEON SAFE FIX
-------------------------------- */
function updateHeaderNeon() {
  const headerTitle = document.querySelector('.brand');
  const hero = document.querySelector('.hero');

  if (!headerTitle || !hero) return;

  const bgType = hero.dataset.bg || 'default';
  const neonVar = headerColors[bgType] || headerColors.default;

  headerTitle.style.color = `var(${neonVar})`;
}

/* -------------------------------
   GALLERY CARD BORDER FIX
-------------------------------- */
function updateGalleryBorders() {
  const cards = document.querySelectorAll('.gallery-card');

  cards.forEach(card => {
    const style = card.getAttribute('data-style');
    const category = card.getAttribute('data-category');

    const img = card.querySelector('img');
    const styleColorVar = styleColors[style] || '--neon';

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

document.addEventListener('DOMContentLoaded', initDynamicEffects);
