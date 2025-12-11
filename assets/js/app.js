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
   Hero randomizer
   --------------------------- */
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
let filters = { category: [], style: [] };

function renderFilters(data){
  const cats = unique(data.map(i=>i.categories||[]));
  const styles = unique(data.map(i=>i.styles||[]));

  const catWrap = document.getElementById('category-filters');
  const styleWrap = document.getElementById('style-filters');
  if(!catWrap || !styleWrap) return;
  catWrap.innerHTML=''; styleWrap.innerHTML='';

  cats.forEach(c=>{
    const b = el('button',{className:'btn-small', type:'button'},[c]);
    b.addEventListener('click', ()=> toggleFilter('category', c, b));
    catWrap.appendChild(b);
  });
  styles.forEach(s=>{
    const b = el('button',{className:'btn-small', type:'button'},[s]);
    b.addEventListener('click', ()=> toggleFilter('style', s, b));
    styleWrap.appendChild(b);
  });

  const clearBtn = document.getElementById('clear-filters');
  if(clearBtn){
    clearBtn.addEventListener('click', ()=>{
      filters = {category:[], style:[]};
      Array.from(catWrap.children).forEach(b=>b.style.opacity=1);
      Array.from(styleWrap.children).forEach(b=>b.style.opacity=1);
      renderGrid(window.GALLERY);
    });
  }
}

function toggleFilter(type, value, btn){
  const arr = filters[type];
  const idx = arr.indexOf(value);
  if(idx === -1){ arr.push(value); btn.style.opacity = 1; }
  else { arr.splice(idx,1); btn.style.opacity = 0.6; }
  applyFilters();
}
function applyFilters(){
  let items = window.GALLERY.slice();
  if(filters.category.length) items = items.filter(it => filters.category.some(c => (it.categories||[]).includes(c)));
  if(filters.style.length) items = items.filter(it => filters.style.some(s => (it.styles||[]).includes(s)));
  renderGrid(items);
}

/* ---------------------------
   Render gallery grid
   --------------------------- */
function renderGrid(items){
  const grid = document.getElementById('gallery-grid');
  if(!grid) return;
  grid.innerHTML = '';
  if(!items.length){
    grid.appendChild(el('div',{className:'card'},[el('div',{},['No pieces match those filters.'])]));
    return;
  }

  items.forEach(it=>{
    const card = el('div',{className:'card gallery-card'});

    // Set dataset for dynamic-effects.js
    card.dataset.id = it.id || '';
    card.dataset.style = (it.styles && it.styles[0]) || '';
    card.dataset.category = (it.categories && it.categories[0]) || '';
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
  content.innerHTML = '';
  const img = document.createElement('img');
  img.src = item.file;
  img.alt = item.title || '';
  content.appendChild(img);
  lb.classList.remove('hidden');
  lb.setAttribute('aria-hidden','false');
  currentIndex = window.GALLERY.indexOf(item);
}
function closeLightbox(){
  const lb=document.getElementById('lightbox');
  if(lb){ lb.classList.add('hidden'); lb.setAttribute('aria-hidden','true'); }
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
  const closeBtn = document.getElementById('lb-close');
  const prevBtn = document.getElementById('lb-prev');
  const nextBtn = document.getElementById('lb-next');
  if(closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if(prevBtn) prevBtn.addEventListener('click', prevItem);
  if(nextBtn) nextBtn.addEventListener('click', nextItem);

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
   Init
   --------------------------- */
(async function init(){
  try{
    setHeroBackground();
    const data = await fetchGallery();
    window.GALLERY = data || [];
    renderFilters(window.GALLERY);
    renderGrid(window.GALLERY);
  }catch(err){
    console.error(err);
    const grid = document.getElementById('gallery-grid');
    if(grid) grid.innerHTML = '<div class="card">Error loading gallery — '+(err.message||err)+'</div>';
  }
})();
