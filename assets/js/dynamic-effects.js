/* ========================================================
   dynamic-effects.js
   Handles dynamic neon colors, gallery card borders, and
   Broboticus personalities/animations.
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

const broboticusList = [
  'balletboticus',
  'fishboticus',
  'karateboticus'
];

/* -------------------------------
   UTILITY FUNCTIONS
-------------------------------- */
function setCSSVar(element, varName, value) {
  element.style.setProperty(varName, value);
}

function randomFromArray(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

/* -------------------------------
   HEADER NEON DYNAMIC COLOR
-------------------------------- */
function updateHeaderNeon() {
  const headerTitle = document.querySelector('.brand');
  const hero = document.querySelector('.hero');

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

    // Image border = style
    const styleColorVar = styleColors[style] || '--neon';
    const img = card.querySelector('img');
    if (img) img.style.borderColor = `var(${styleColorVar})`;

    // Card border = category
    const cardColor = categoryBorderColors[category] || 'var(--fg)';
    card.style.border = `2px solid ${cardColor}`;
  });
}

/* -------------------------------
   BROBOTICUS DYNAMIC PLACEMENT
-------------------------------- */
function spawnBroboticus() {
  const broboticusContainer = document.body;
  const botName = randomFromArray(broboticusList);
  const bot = document.createElement('img');

  bot.src = `/assets/broboticus/${botName}.png`;
  bot.alt = botName;
  bot.className = 'robot-foreground animated';
  bot.style.position = 'fixed';
  bot.style.bottom = '0';
  bot.style.right = `${Math.random() * 80 + 10}%`;
  bot.style.width = 'clamp(120px,22vw,320px)';
  bot.style.zIndex = '9999';
  bot.style.pointerEvents = 'auto';

  broboticusContainer.appendChild(bot);

  // Optional: auto-remove after some time
  setTimeout(() => bot.remove(), 10000);
}

/* -------------------------------
   INITIALIZATION
-------------------------------- */
function initDynamicEffects() {
  updateHeaderNeon();
  updateGalleryBorders();
  spawnBroboticus();
}

/* Run once DOM is fully loaded */
document.addEventListener('DOMContentLoaded', () => {
  initDynamicEffects();

  // Optional: spawn a new Broboticus every 20-30s
  setInterval(spawnBroboticus, 25000);
});
