/* app.js — gallery loader, filters, lightbox, hero randomizer */

/* ---------------------------
   Config - adjust paths if needed
   --------------------------- */
const GALLERY_JSON = '/assets/data/gallery.json';
const GALLERY_BASE = '/assets/images/raw/'; // full images
const THUMB_BASE = '/assets/images/gallery-thumbs/'; // thumbnails
const HERO_CHOICES = [
  { path: '/assets/images/hero/glitch1.png', key: 'glitch1' },
  { path: '/assets/images/hero/glitch2.png', key: 'glitch2' },
  { path: '/assets/images/hero/glitch3.jpg', key: 'glitch3' },
  { path: '/assets/images/hero/glitch4.png', key: 'glitch-default' }
];

/* ---------------------------
   Utility helpers
   --------------------------- */
function el(tag, props={}, children=[]){
  const e = document.createElement(tag);
  Object.assign(e, props);
  (children||[]).forEach(c => e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
  return e;
}
function setCSSVar(element, property, value) {
    if (element && element.style) {
        element.style.setProperty(property, value);
    }
}
function unique(arr){ return [...new Set(arr.flat())]; }

/* ---------------------------
   3D Card Compatibility Helper
   --------------------------- */
function initialize3DCardCompatibility() {
  // Ensure lightbox works with 3D transformed elements
  document.addEventListener('click', function(e) {
    const card = e.target.closest('.neon-3d-card');
    if (card && e.target.tagName === 'IMG') {
      // If clicking an image inside a 3D card, temporarily flatten it
      // for better lightbox transition
      card.style.transform = 'translateZ(0)';
      card.style.transition = 'transform 0.2s ease';
      
      // Restore after a short delay
      setTimeout(() => {
        card.style.transform = '';
        card.style.transition = '';
      }, 50);
    }
  });
  
  // Make sure lightbox z-index is above everything
  const lightbox = document.getElementById('lightbox');
  if (lightbox) {
    lightbox.style.zIndex = '10000';
  }
}

/* ---------------------------
   Hero randomizer
   --------------------------- */
function setBrandColor(){
  const brand = document.querySelector('.brand');
  if(brand){
    // Pick 1-8
    const num = Math.floor(Math.random() * 8) + 1;
    brand.classList.add(`brand-neon-${num}`);
  }
}

function setHeroBackground(){
  // Check if there are choices available
  if(HERO_CHOICES.length === 0) return;

  // 1. Pick a random object from the array (e.g., { path: '...', key: 'glitch1' })
  const pickObject = HERO_CHOICES[Math.floor(Math.random() * HERO_CHOICES.length)];
  
  // 2. Extract the path and the key from the chosen object
  const pickPath = pickObject.path;
  const pickKey = pickObject.key; // This holds the exact key (e.g., 'glitch1')

  // 3. Select HTML elements
  const heroBg = document.querySelector('.hero-bg');
  const header = document.querySelector('.site-header');
  const hero = document.getElementById('hero'); // Now finds the element with id="hero"

  // 4. Apply the image path (using pickPath)
  if(heroBg) heroBg.style.backgroundImage = `url("${pickPath}")`;
  if(header){
    // Update header styling - using the path from the object
    header.style.backgroundImage = `linear-gradient(180deg, rgba(5,5,5,0.6), rgba(5,5,5,0.35)), url("${pickPath}")`;
    header.style.backgroundSize = 'cover';
    header.style.backgroundPosition = 'center';
    header.style.backgroundBlendMode = 'overlay';
    header.style.opacity = '1';
  }

  // 5. Update dataset.bg so dynamic-effects.js can read it
  if(hero && pickKey) {
    let bgKey = 'default';
    
    // Map the pickKey to the appropriate bgKey for dynamic-effects.js
    if (pickKey.includes('glitch1')) {
      bgKey = 'neon-limon';
    } else if (pickKey.includes('glitch2')) {
      bgKey = 'neon';
    } else if (pickKey.includes('glitch3')) {
      bgKey = 'neon-mag';
    } else if (pickKey.includes('glitch4') || pickKey.includes('glitch-default')) {
      // Note: Your HERO_CHOICES has 'glitch-default' for glitch4
      bgKey = 'neon-pur';
    }
    
    hero.dataset.bg = bgKey;
  }
}

/* ---------------------------
   Fetch gallery data
   --------------------------- */
async function fetchGallery(){
  try{
    const res = await fetch(GALLERY_JSON, { cache:'no-store' });
    if(!res.ok){
      console.error(`gallery.json not found at ${GALLERY_JSON}`);
      return [];
    }
    return await res.json();
  }catch(err){
    console.error('Fetch failed:', err);  
    return [];
  }
}

/* ---------------------------
   Filters & Rendering
   --------------------------- */
let filters = { style: [] };

function renderFilters(data){
  const styles = unique(data.map(i=>i.styles||[]));

  const styleWrap = document.getElementById('style-filters');
  if(!styleWrap) return;
  styleWrap.innerHTML='';

  styles.forEach(s=>{
    const b = el('button',{className:'btn-small', type:'button'},[s]);
    b.addEventListener('click', ()=> toggleFilter('style', s, b));
    styleWrap.appendChild(b);
  });

  const clearBtn = document.getElementById('clear-filters');
  if(clearBtn){
    clearBtn.addEventListener('click', ()=>{
      filters = {style:[]};
      document.querySelectorAll('.btn-small').forEach(b => b.classList.remove('active'));
      renderGrid(window.GALLERY);
    });
  }
}

function toggleFilter(type, value, btn){
  const arr = filters[type];
  const idx = arr.indexOf(value);
  if(idx === -1){ 
    arr.push(value); 
    btn.classList.add('active'); 
  }
  else { 
    arr.splice(idx,1); 
    btn.classList.remove('active'); 
  }
  applyFilters();
}
function applyFilters(){
  let items = window.GALLERY.slice();
  if(filters.style.length) items = items.filter(it => filters.style.some(s => (it.styles||[]).includes(s)));
  renderGrid(items);
}

/* ---------------------------
   Render gallery grid
   --------------------------- */
function renderGrid(items, simplified = false){
  const grid = document.getElementById('gallery-grid');
  if(!grid) return;
  grid.innerHTML = '';
  if(!items.length){
    grid.appendChild(el('div',{className:'card'},[el('div',{},['No pieces match those filters.'])]));
    return;
  }

  items.forEach(it=>{
    // Get the first category for CSS class
    const firstCategory = (it.categories && it.categories[0]) || 'Glitch';
    const categoryClass = 'category-' + firstCategory.replace(/\s+/g, '-');
    
    const thumbSrc = THUMB_BASE + it.id + '.jpg';
    const largeSrc = it.file.startsWith('/') ? it.file : '/' + it.file;
    
    // Construct Card Contents
    const cardChildren = [
      // Image
      el('img', {
        src: thumbSrc,
        alt: `${it.title} | BasicGlitch`,
        loading: 'lazy',
        className: 'gallery-image',
        'data-large': largeSrc
      }),
      // Title
      el('h3', { style: simplified ? 'text-align: center; margin-top: 15px;' : 'margin-top: 15px;' }, [it.title || 'Untitled'])
    ];

    // Add Description and Price if NOT simplified
    if (!simplified) {
      if (it.description) {
        cardChildren.push(el('p', { className: 'muted', style: 'font-size: 0.9rem; margin: 10px 0;' }, [it.description]));
      }
      if (it.price) {
        cardChildren.push(el('p', { className: 'price', style: 'color: var(--neon-2); font-weight: bold;' }, [`$${it.price}`]));
      }
    }
    
    // Create card
    const card = el('div',{
      className: `card gallery-card ${categoryClass}`,
    }, cardChildren);

    // Robust click listener for Lightbox
    card.addEventListener('click', (e) => {
      e.preventDefault();
      openLightbox(it.id);
    });
    
    // Set dataset for effects
    card.dataset.id = it.id || '';
    card.dataset.style = (it.styles && it.styles[0]) || '';
    card.dataset.category = firstCategory;
    
    grid.appendChild(card);
  });

  if(typeof updateGalleryBorders === 'function') updateGalleryBorders();
}

/* ---------------------------
   LIGHTBOX
   --------------------------- */
let currentIndex = 0;
function openLightbox(id){
  const item = window.GALLERY.find(i => i.id === id);
  if(!item) return;
  
  const lb = document.getElementById('lightbox');
  const content = document.getElementById('lb-content');
  if(!lb || !content) return;
  
  // TEMPORARILY REMOVE 3D TRANSFORM from clicked card for better lightbox experience
  const clickedCard = document.querySelector(`.gallery-card[data-id="${id}"]`);
  if (clickedCard) {
    clickedCard.style.transform = 'none';
    clickedCard.style.transition = 'none';
  }
  
  content.innerHTML = '';
  const img = document.createElement('img');
  
  // Use the full image path from JSON
  img.src = item.file.startsWith('/') ? item.file : '/' + item.file;
  img.alt = item.title || '';
  
  // Add title and description to lightbox
  const title = document.createElement('h3');
  title.textContent = item.title || '';
  
  const desc = document.createElement('p');
  desc.textContent = item.description || '';
  
  content.appendChild(title);
  content.appendChild(img);
  content.appendChild(desc);
  
  lb.classList.remove('hidden');
  lb.setAttribute('aria-hidden','false');
  currentIndex = window.GALLERY.indexOf(item);
}
function closeLightbox(){
  const lb = document.getElementById('lightbox');
  if(lb){ 
    lb.classList.add('hidden'); 
    lb.setAttribute('aria-hidden','true'); 
    
    // RESTORE 3D TRANSFORM when lightbox closes
    document.querySelectorAll('.gallery-card').forEach(card => {
      card.style.transform = '';
      card.style.transition = '';
    });
  }
}
function prevItem(){ if(currentIndex > 0) openLightbox(window.GALLERY[currentIndex-1].id); }
function nextItem(){ if(currentIndex < window.GALLERY.length-1) openLightbox(window.GALLERY[currentIndex+1].id); }

/* keyboard & touch */
document.addEventListener('keydown', e=>{
  if(e.key==='Escape') closeLightbox();
  if(e.key==='ArrowLeft') prevItem();
  if(e.key==='ArrowRight') nextItem();
});

const lbContent = document.getElementById('lb-content');
if(lbContent){
  let touchStartX = 0, touchEndX = 0;
  const swipeThreshold = 50;
  lbContent.addEventListener('touchstart', e=>{ touchStartX = e.changedTouches[0].screenX; }, false);
  lbContent.addEventListener('touchend', e=>{
    touchEndX = e.changedTouches[0].screenX;
    if(touchEndX <= touchStartX - swipeThreshold) nextItem();
    if(touchEndX >= touchStartX + swipeThreshold) prevItem();
  }, false);
}

/* attach lightbox UI controls and mobile nav toggle */
document.addEventListener('DOMContentLoaded', ()=>{
  const lightbox = document.getElementById('lightbox');
  const closeBtn = document.getElementById('lb-close');
  const prevBtn = document.getElementById('lb-prev');
  const nextBtn = document.getElementById('lb-next');
  
  if(closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if(prevBtn) prevBtn.addEventListener('click', prevItem);
  if(nextBtn) nextBtn.addEventListener('click', nextItem);

  // Close on background click
  if(lightbox) {
    lightbox.addEventListener('click', (e) => {
      if(e.target === lightbox) closeLightbox();
    });
  }

  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mainNav = document.getElementById('main-nav');
  const siteHeader = document.querySelector('.site-header') || document.getElementById('site-header');
  if(mobileToggle){
    mobileToggle.addEventListener('click', ()=>{
      const open = mainNav?.classList.toggle('nav-open');
      mobileToggle.classList.toggle('toggle-active');
      mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if(siteHeader) siteHeader.classList.toggle('header-mobile-open', open);
    });
  }
});

/* ---------------------------
   COLLECTION ENGINE
   --------------------------- */
const COLLECTION_CONFIG = {
  'broboticus': {
    title: 'The Broboticus Series',
    desc: 'An ongoing study of robotic personality and leisure.',
    filter: (item) => (item.categories||[]).includes('Broboticus')
  },
  'neon': {
    title: 'Environmental Horizons',
    desc: 'Atmospheric landscapes and digital environments.',
    filter: (item) => (item.styles||[]).includes('Landscape') && !(item.categories||[]).includes('Broboticus')
  },
  'abstract': {
    title: 'The Psychedelic Void',
    desc: 'Geometric symmetry and vibrant psychedelia.',
    filter: (item) => (item.styles||[]).includes('Psychedelia') || (item.styles||[]).includes('Geometric')
  }
};

function initCollectionPage(data) {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const config = COLLECTION_CONFIG[id];
  
  if (!config) {
    document.getElementById('collection-title').textContent = 'ARCHIVE NOT FOUND';
    document.getElementById('collection-desc').textContent = 'The requested data stream appears corrupted.';
    return;
  }
  
  // Set Header
  document.getElementById('collection-title').textContent = config.title;
  document.getElementById('collection-desc').textContent = config.desc;
  document.title = `${config.title} | BasicGlitch`;
  
  // Filter Data
  const items = data.filter(config.filter);
  renderGrid(items, true); // SIMPLIFIED VIEW FOR PORTFOLIO
}

/* ---------------------------
   FORMS HANDLING (AJAX)
   --------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  const forms = [
    { id: 'signup-form', statusId: 'signup-status' },
    { id: 'contact-form', statusId: 'contact-status' }
  ];

  forms.forEach(({ id, statusId }) => {
    const form = document.getElementById(id);
    const status = document.getElementById(statusId);

    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Basic feedback
        status.textContent = 'TRANSMITTING...';
        status.style.color = 'var(--neon)';
        
        const data = new FormData(form);
        const action = form.action; // Get URL from HTML form action attribute

        // Validation: Check if default ID is still present
        if (action.includes('YOUR_FORM_ID')) {
           status.textContent = 'ERROR: CONFIGURATION MISSING (Set Formspree ID)';
           status.style.color = 'red';
           return;
        }

        try {
          const response = await fetch(action, {
            method: form.method,
            body: data,
            headers: {
              'Accept': 'application/json'
            }
          });

          if (response.ok) {
            status.textContent = 'TRANSMISSION RECEIVED. WELCOME TO THE GRID.';
            status.style.color = 'var(--neon-2)';
            form.reset();
          } else {
            const result = await response.json();
            if (Object.hasOwn(result, 'errors')) {
              status.textContent = result.errors.map(error => error.message).join(", ");
            } else {
              status.textContent = 'TRANSMISSION FAILED. RETRY.';
            }
            status.style.color = 'var(--neon-org)';
          }
        } catch (error) {
          status.textContent = 'NETWORK ERROR. SIGNAL LOST.';
          status.style.color = 'red';
        }
        
        // Clear status after 5s
        setTimeout(() => {
          if (status.textContent.includes('RECEIVED')) status.textContent = '';
        }, 5000);
      });
    }
  });
});

/* ---------------------------
   Init
   --------------------------- */
(async function init(){
  try{
    setBrandColor();
    setHeroBackground();
    
    // FETCH DATA ONCE
    const data = await fetchGallery();
    window.GALLERY = data || [];

    // ROUTER LOGIC
    if(document.getElementById('collection-view')) {
      // We are on collection.html
      initCollectionPage(window.GALLERY);
      initialize3DCardCompatibility();
    } 
    else if(document.getElementById('gallery-grid')) {
      // We are on gallery.html
      renderFilters(window.GALLERY);
      renderGrid(window.GALLERY, false); // FULL VIEW FOR GALLERY
      initialize3DCardCompatibility();
    }
    
    // ANTI-SPAM: Decrypt email on interaction
    const emailLinks = document.querySelectorAll('.secure-contact-link');
    if(emailLinks.length > 0) {
      emailLinks.forEach(link => {
        const revealEmail = () => {
          const u = link.dataset.user;
          const d = link.dataset.domain;
          if(!u || !d) return;
          const addr = `${u}@${d}`;
          link.href = `mailto:${addr}`;
          link.textContent = addr;
          link.classList.remove('glitch-link');
          // Remove listeners once decrypted
          link.removeEventListener('mouseover', revealEmail);
          link.removeEventListener('click', revealEmail);
        };
        
        link.addEventListener('mouseover', revealEmail);
        link.addEventListener('click', revealEmail);
        // Also decrypt after 3 seconds automatically for usability
        setTimeout(revealEmail, 3000);
      });
    }
  }catch(err){
    console.error(err);
    const grid = document.getElementById('gallery-grid');
    if(grid) grid.innerHTML = '<div class="card">Error loading gallery — '+(err.message||err)+'</div>';
  }
})();
