/* ========================================================
   dynamic-effects.js
   Handles header neon colors and gallery card border logic.
   UPDATED FOR 3D CARD COMPATIBILITY
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
  'Landscape': '--neon-mag',
  'Glitch': '--neon-pur',
  'Animation': '--neon-mag',
  'Geometric': '--neon',
  'Surrealism': '--neon-blu',
  'Broboticus': '--neon-org',
  'Psychedelia': '--neon-pur'
  // Add more as needed
};

const categoryBorderColors = {
  // Define your category mappings here
  'Available for Purchase': 'var(--neon-limon)',
  'Broboticus': 'var(--neon-pur)',
  'Neon': 'var(--neon-yel)',
  'Glitch': 'var(--neon-2)',
  'Animation': 'var(--neon-mag)',
  'Geometric': 'var(--neon)',
  'Surrealism': 'var(--neon-blu)',
  'Psychedelia': 'var(--neon-pur)',
  'Character': 'var(--neon-org)'
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
   GALLERY CARD NEON GLOW EFFECTS (UPDATED FOR 3D CARDS)
-------------------------------- */
function updateGalleryBorders() {
  const cards = document.querySelectorAll('.gallery-card');

  cards.forEach(card => {
    const style = card.dataset.style || '';
    const category = card.dataset.category || '';
    
    // Get color for this card
    const styleColorVar = styleColors[style] || '--fg';
    const categoryColor = categoryBorderColors[category] || 'var(--fg)';
    
    // Create or update neon glow effect using CSS variables
    card.style.setProperty('--neon-glow-color', `var(${styleColorVar})`);
    card.style.setProperty('--neon-glow-intensity', '0.4');
    
    // Remove old border styles that conflict with 3D transforms
    card.style.border = '';
    
    const img = card.querySelector('img');
    if (img) {
      // Use box-shadow for glow effect instead of border
      img.style.border = '';
      img.style.boxShadow = `0 0 15px ${categoryColor}, 0 0 30px ${categoryColor} inset`;
      img.style.transition = 'box-shadow 0.3s ease, transform 0.3s ease';
    }
    
    // Add hover effect for enhanced neon glow
    card.addEventListener('mouseenter', () => {
      if (img) {
        img.style.boxShadow = `0 0 25px ${categoryColor}, 0 0 40px ${categoryColor} inset`;
      }
      card.style.setProperty('--neon-glow-intensity', '0.7');
    });
    
    card.addEventListener('mouseleave', () => {
      if (img) {
        img.style.boxShadow = `0 0 15px ${categoryColor}, 0 0 30px ${categoryColor} inset`;
      }
      card.style.setProperty('--neon-glow-intensity', '0.4');
    });
  });
}

/* -------------------------------
   3D CARD COMPATIBILITY HELPERS
-------------------------------- */
function initialize3DEffects() {
  // Add CSS for neon glow effects that work with 3D transforms
  const style = document.createElement('style');
  style.textContent = `
    .neon-3d-card {
      --neon-glow-color: var(--neon);
      --neon-glow-intensity: 0.4;
    }
    
    .neon-3d-card::before {
      content: '';
      position: absolute;
      top: -2px;
      left: -2px;
      right: -2px;
      bottom: -2px;
      background: var(--neon-glow-color);
      border-radius: calc(var(--card-radius) + 2px);
      opacity: var(--neon-glow-intensity);
      filter: blur(10px);
      z-index: -1;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    
    .neon-3d-card:hover::before {
      opacity: calc(var(--neon-glow-intensity) + 0.3);
      filter: blur(15px);
    }
    
    /* Ensure gallery images have proper glow */
    .gallery-card img {
      position: relative;
      z-index: 2;
    }
  `;
  document.head.appendChild(style);
}

/* -------------------------------
   SECTION BACKGROUND ENHANCEMENTS
-------------------------------- */
function enhanceSectionBackgrounds() {
  // Add subtle pulsing animation to neon grid sections
  const neonSections = document.querySelectorAll('.neon-grid-section');
  
  neonSections.forEach(section => {
    // Add data attribute for identification
    section.dataset.neonEnhanced = 'true';
    
    // Add subtle parallax effect on scroll
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'gridPulse 4s ease-in-out infinite';
        } else {
          entry.target.style.animation = '';
        }
      });
    }, { threshold: 0.1 });
    
    observer.observe(section);
  });
  
  // Add the gridPulse animation
  const pulseStyle = document.createElement('style');
  pulseStyle.textContent = `
    @keyframes gridPulse {
      0%, 100% { opacity: 0.7; }
      50% { opacity: 0.85; }
    }
    
    .neon-grid-section::before {
      animation: gridMove 30s linear infinite, gridPulse 4s ease-in-out infinite;
    }
  `;
  document.head.appendChild(pulseStyle);
}

/* -------------------------------
   INSTAGRAM CARD ENHANCEMENTS
-------------------------------- */
function enhanceInstagramCards() {
  const instagramCards = document.querySelectorAll('.instagram-card.neon-3d-card');
  
  instagramCards.forEach(card => {
    // Add subtle neon border effect
    const frame = card.querySelector('.instagram-frame');
    if (frame) {
      frame.style.position = 'relative';
      frame.style.overflow = 'hidden';
      
      // Add neon edge effect
      const edgeGlow = document.createElement('div');
      edgeGlow.style.position = 'absolute';
      edgeGlow.style.top = '0';
      edgeGlow.style.left = '0';
      edgeGlow.style.right = '0';
      edgeGlow.style.bottom = '0';
      edgeGlow.style.borderRadius = '12px';
      edgeGlow.style.background = 'linear-gradient(45deg, var(--neon-mag), var(--neon))';
      edgeGlow.style.opacity = '0.1';
      edgeGlow.style.pointerEvents = 'none';
      edgeGlow.style.zIndex = '1';
      frame.appendChild(edgeGlow);
    }
  });
}

/* -------------------------------
   INITIALIZATION
-------------------------------- */
function initDynamicEffects() {
  updateHeaderNeon();
  updateGalleryBorders();
  initialize3DEffects();
  enhanceSectionBackgrounds();
  enhanceInstagramCards();
  
  // Update effects when gallery filters change
  const filterButtons = document.querySelectorAll('#category-filters button, #style-filters button');
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Small delay to allow gallery to re-render
      setTimeout(updateGalleryBorders, 100);
    });
  });
  
  // Update when filters are cleared
  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      setTimeout(updateGalleryBorders, 100);
    });
  }
}

/* Run on DOM ready */
document.addEventListener('DOMContentLoaded', initDynamicEffects);

/* Export functions for use in app.js */
if (typeof window !== 'undefined') {
  window.updateGalleryBorders = updateGalleryBorders;
  window.enhanceSectionBackgrounds = enhanceSectionBackgrounds;
}

// Mouse movement for gradient shift
document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    document.body.style.setProperty('--mouse-x', x);
    document.body.style.setProperty('--mouse-y', y);
});

// Scroll Glitch Effect
let isScrolling;
window.addEventListener('scroll', () => {
    document.body.classList.add('scroll-glitch-active');
    
    window.clearTimeout(isScrolling);
    isScrolling = setTimeout(() => {
        document.body.classList.remove('scroll-glitch-active');
    }, 150); // Stop glitch 150ms after scrolling stops
}, { passive: true });
