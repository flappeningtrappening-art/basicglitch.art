/* app.js — gallery loader, filters, lightbox, hero randomizer */

/* ---------------------------
   Config - adjust paths if needed
   --------------------------- */
const FORGE_API = 'https://scene-trust-annotation-significant.trycloudflare.com'; 
const GALLERY_JSON = 'assets/data/gallery.json';
const GALLERY_BASE = 'assets/images/raw/'; // full images
const THUMB_BASE = 'assets/images/gallery-thumbs/'; // thumbnails
const HERO_CHOICES = [
  { path: 'assets/images/hero/glitch1.webp', key: 'glitch1' },
  { path: 'assets/images/hero/glitch2.webp', key: 'glitch2' },
  { path: 'assets/images/hero/glitch3.jpg', key: 'glitch3' },
  { path: 'assets/images/hero/glitch4.webp', key: 'glitch-default' }
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
    } else if (pickKey.includes('glitch-ai')) {
      bgKey = 'neon-2'; // Green/Matrix style
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
const seriesFilter = document.createElement('select');
seriesFilter.id = 'series-filter';
seriesFilter.innerHTML = '<option value="All">All Series</option><option value="SANGRE DE CRISTOS SERIES">SANGRE DE CRISTOS SERIES</option><option value="CASE STUDY 42 — BROBOTICUS">CASE STUDY 42 — BROBOTICUS</option><option value="MASTERS REMIXED">MASTERS REMIXED</option><option value="PUP FICTION">PUP FICTION</option><option value="CYBER SAVANNA">CYBER SAVANNA</option><option value="PACHYDERMIS TRIPTYCH">PACHYDERMIS TRIPTYCH</option><option value="SPIRAL STUDIES">SPIRAL STUDIES</option><option value="SKULLASTIC ENDEAVOR">SKULLASTIC ENDEAVOR</option><option value="MYCOLOGY SERIES">MYCOLOGY SERIES</option><option value="GAIA DIPTYCH">GAIA DIPTYCH</option><option value="HAND-DRAWN INK">HAND-DRAWN INK</option><option value="PERSONAL / AUTOBIOGRAPHICAL">PERSONAL / AUTOBIOGRAPHICAL</option>';
styleWrap.appendChild(seriesFilter);

seriesFilter.addEventListener('change', (e) => {
    filters.series = e.target.value === 'All' ? [] : [e.target.value];
    renderGallery();
});
