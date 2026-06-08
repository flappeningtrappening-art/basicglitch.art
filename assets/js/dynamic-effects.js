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
  'neon-limon': '--neon-limon',
  'neon': '--neon',
  'neon-mag': '--neon-mag',
  'neon-pur': '--neon-pur',
  'neon-2': '--neon-2',
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
    
    const actualColor = getComputedStyle(document.documentElement).getPropertyValue(neonVar).trim(); 
    setCSSVar(headerTitle, 'color', actualColor);
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
  // Add styles for featured card 3D effect
  const style = document.createElement('style');
  style.textContent = `
    /* Target only the first archive card and first gallery card */
    .archive-grid .archive-card:first-child,
    .gallery-grid .gallery-card:first-child {
      --neon-glow-color: var(--neon);
      --neon-glow-intensity: 0.4;
      position: relative;
      overflow: hidden;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* Override specific colors for Broboticus card (green theme) */
    .archive-grid .archive-card--grn:first-child {
      --neon-glow-color: var(--neon-2);
    }
    
    /* Override for gallery first card - use magenta */
    .gallery-grid .gallery-card:first-child {
      --neon-glow-color: var(--neon-mag);
    }
    
    /* The Racing Tracer (Tron/Snake Style) */
    .archive-grid .archive-card:first-child::before,
    .gallery-grid .gallery-card:first-child::before {
      content: '';
      position: absolute;
      width: 200%;
      height: 200%;
      top: -50%;
      left: -50%;
      background: conic-gradient(
        transparent 70%, 
        var(--neon-glow-color) 85%,
        transparent 100%
      );
      animation: snake-rotate 3s linear infinite;
      z-index: 0;
      pointer-events: none;
      opacity: var(--neon-glow-intensity);
      transition: opacity 0.3s ease;
    }
    
    /* Ensure card content is above tracer */
    .archive-grid .archive-card:first-child > *,
    .gallery-grid .gallery-card:first-child > * {
      position: relative;
      z-index: 2;
    }
    
    /* Hover State Intensity - tracer speeds up and glows brighter */
    .archive-grid .archive-card:first-child:hover::before,
    .gallery-grid .gallery-card:first-child:hover::before {
      --neon-glow-intensity: 0.9;
      animation-duration: 1.2s;
    }
    
    /* Hover effect on the card itself */
    .archive-grid .archive-card:first-child:hover,
    .gallery-grid .gallery-card:first-child:hover {
      transform: translateY(-6px);
      box-shadow: 0 0 30px var(--neon-glow-color);
    }
    
    /* Dark overlay to make content readable and tracer look like a border */
    .archive-grid .archive-card:first-child::after,
    .gallery-grid .gallery-card:first-child::after {
      content: '';
      position: absolute;
      inset: 2px;
      background: rgba(10, 10, 15, 0.95);
      border-radius: calc(var(--card-radius, 12px) - 2px);
      z-index: 1;
      pointer-events: none;
    }
    
    /* Keep images above the overlay */
    .archive-grid .archive-card:first-child img,
    .gallery-grid .gallery-card:first-child img {
      position: relative;
      z-index: 2;
    }
    
    /* Keep card body content above overlay */
    .archive-grid .archive-card:first-child .archive-card-body,
    .gallery-grid .gallery-card:first-child .card-info,
    .gallery-grid .gallery-card:first-child h3,
    .gallery-grid .gallery-card:first-child p {
      position: relative;
      z-index: 2;
      background: transparent;
    }
    
    /* Animation keyframes */
    @keyframes snake-rotate {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
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
  // Update header neon color
  updateHeaderNeon();
  
  // Update gallery card borders
  updateGalleryBorders();
  
  // Initialize 3D card effects (featured card only)
  initialize3DEffects();
  
  // Enhance section backgrounds
  enhanceSectionBackgrounds();
  
  // Enhance Instagram cards
  enhanceInstagramCards();
  
  // Update effects when gallery filters change
  const filterButtons = document.querySelectorAll('#category-filters button, #style-filters button');
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Small delay to allow gallery to re-render
      setTimeout(() => {
        updateGalleryBorders();
        // Re-apply any dynamic 3D effect fixes after filter change
        fixFirstCardAfterFilter();
      }, 100);
    });
  });
  
  // Update when filters are cleared
  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      setTimeout(() => {
        updateGalleryBorders();
        fixFirstCardAfterFilter();
      }, 100);
    });
  }
  
  // Observe gallery for dynamic content changes
  observeGalleryFor3DEffect();
  
  // Fix for archive page first card (ensures 3D effect applies)
  fixArchiveFirstCard();
}

// Helper function to ensure first card retains 3D effect after filter changes
function fixFirstCardAfterFilter() {
  const galleryGrid = document.getElementById('gallery-grid');
  if (galleryGrid) {
    const firstCard = galleryGrid.querySelector('.gallery-card:first-child');
    if (firstCard) {
      // Force a repaint to ensure CSS picks up the selector
      firstCard.style.transform = 'translateZ(0)';
      setTimeout(() => {
        firstCard.style.transform = '';
      }, 10);
    }
  }
}

// Helper function to fix archive first card (runs once on load)
function fixArchiveFirstCard() {
  const archiveGrid = document.querySelector('.archive-grid');
  if (archiveGrid) {
    const firstCard = archiveGrid.querySelector('.archive-card:first-child');
    if (firstCard) {
      // Ensure the card has proper styling
      firstCard.style.position = 'relative';
      firstCard.style.overflow = 'hidden';
    }
  }
}

// Observer for dynamically loaded gallery content
function observeGalleryFor3DEffect() {
  const galleryGrid = document.getElementById('gallery-grid');
  if (!galleryGrid) return;
  
  // Disconnect existing observer if any
  if (window._galleryObserver) {
    window._galleryObserver.disconnect();
  }
  
  // Create new observer
  window._galleryObserver = new MutationObserver((mutations) => {
    let shouldUpdate = false;
    
    mutations.forEach(mutation => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        shouldUpdate = true;
      }
    });
    
    if (shouldUpdate) {
      setTimeout(() => {
        updateGalleryBorders();
        // CSS selector will automatically apply to the new first child
      }, 50);
    }
  });
  
  window._galleryObserver.observe(galleryGrid, { 
    childList: true, 
    subtree: false 
  });
}

// Run when DOM is ready, and also when gallery data loads
document.addEventListener('DOMContentLoaded', () => {
  initDynamicEffects();
});

// Also re-run when gallery data is loaded (for dynamic gallery pages)
window.addEventListener('GALLERY_READY', () => {
  setTimeout(() => {
    updateGalleryBorders();
    fixFirstCardAfterFilter();
  }, 100);
});
