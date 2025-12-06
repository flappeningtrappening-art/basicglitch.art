/* app.js — gallery loader, filters, lightbox, hero randomizer */

/* ---------------------------
   Config - adjust paths if needed
   --------------------------- */
const GALLERY_JSON = '/data/gallery.json';
const GALLERY_BASE = '/assets/images/gallery/'; // full images
const THUMB_BASE = '/assets/images/gallery/thumbs/'; // thumbnails
const HERO_CHOICES = [
  '/assets/images/mountains.png',
  '/assets/images/circuit-glitch.png'
]; // only these two randomized between header & hero

/* ---------------------------
   Utility helpers
   --------------------------- */
function el(tag, props={}, children=[]){
  const e = document.createElement(tag);
  Object.assign(e, props);
  (children||[]).forEach(c => e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
  return e;
}
function unique(arr){ return [...new Set(arr.flat())]; }

/* ---------------------------
   Hero randomizer (header + hero same image)
   - choose between HERO_CHOICES only
   - apply as background for .hero-bg and header background accent
   --------------------------- */
function setHeroBackground(){
  const pick = HERO_CHOICES[Math.floor(Math.random()*HERO_CHOICES.length)];
  const heroBg = document.querySelector('.hero-bg');
  const header = document.querySelector('.site-header');

  if(heroBg) heroBg.style.backgroundImage = `url("${pick}")`;
  // dimmed overlay already present in CSS; keep it at ~0.25. If you want darker: change overlay opacity.
  if(header){
    header.style.backgroundImage = `linear-gradient(180deg, rgba(5,5,5,0.6), rgba(5,5,5,0.35)), url("${pick}")`;
    header.style.backgroundSize = 'cover';
    header.style.backgroundPosition = 'center';
    header.style.backgroundBlendMode = 'overlay';
    header.style.opacity = '1';
  }
}

async function fetchGallery(){
  try{
    const res = await fetch('/data/gallery.json', { cache:'no-store' });

    if(!res.ok){
      console.error('gallery.json not found at /data/gallery.json');
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
  catWrap.innerHTML=''; styleWrap.innerHTML='';

  cats.forEach(c=>{
    const b = el('button',{className:'btn-small'},[c]);
    b.addEventListener('click', ()=> toggleFilter('category', c, b));
    catWrap.appendChild(b);
  });
  styles.forEach(s=>{
    const b = el('button',{className:'btn-small'},[s]);
    b.addEventListener('click', ()=> toggleFilter('style', s, b));
    styleWrap.appendChild(b);
  });

  document.getElementById('clear-filters').addEventListener('click', ()=> {
    filters = {category:[], style:[]};
    renderGrid(window.GALLERY);
  });
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
   Each item expected: { id, title, file, categories:[], styles:[], date, description, price }
   - Thumbs are expected at THUMB_BASE + filename
   - If thumbnail not found, fallback to the full image.
   --------------------------- */
function renderGrid(items){
  const grid = document.getElementById('gallery-grid');
  grid.innerHTML = '';
  if(!items.length){
    grid.appendChild(el('div',{className:'card'},[el('div',{},['No pieces match those filters.'])]));
    return;
  }

  items.forEach(it=>{
    const card = el('div',{className:'card gallery-card'});
    // thumbnail fallback logic
    const filename = (it.file || '').split('/').pop();
    let thumbUrl = THUMB_BASE + filename;
    // image element
    const img = el('img',{src:thumbUrl, alt: it.title || '', loading:'lazy'});
    // fallback: if thumbnail 404, browser will log; we also attempt lazy switch to full
    img.onerror = function(){
      img.onerror = null;
      img.src = it.file || (GALLERY_BASE + filename);
    };

    // title + meta
    const h3 = el('h3',{},[it.title || 'Untitled']);
    const meta = el('p',{className:'muted'},[(it.categories||[]).join(' • ')]);

    // color class for category accent (pick first category)
    if(it.categories && it.categories.length){
      const catClass = 'category-' + it.categories[0].replace(/\s+/g,'');
      h3.classList.add(catClass);
    }

    // actions
    const actions = el('div',{className:'row'});
    const viewBtn = el('button',{className:'btn-small'},['View']);
    viewBtn.addEventListener('click', ()=> openLightbox(it.id));
    const orderLink = el('a',{className:'btn-small', href:'https://ko-fi.com/basicglitch', target:'_blank', rel:'noopener'},['Order']);
    actions.appendChild(viewBtn);
    actions.appendChild(orderLink);

    // description small
    const desc = el('p',{className:'muted'},[it.description || '']);

    // assemble
    card.appendChild(img);
    card.appendChild(h3);
    card.appendChild(meta);
    card.appendChild(desc);
    card.appendChild(actions);

    // data attributes for filtering (optional)
    card.dataset.id = it.id;
    grid.appendChild(card);
  });
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
  content.innerHTML = '';
  const img = document.createElement('img');
  img.src = item.file;
  img.alt = item.title || '';
  content.appendChild(img);
  lb.classList.remove('hidden');
  lb.setAttribute('aria-hidden','false');
  currentIndex = window.GALLERY.indexOf(item);
}
function closeLightbox(){ const lb=document.getElementById('lightbox'); lb.classList.add('hidden'); lb.setAttribute('aria-hidden','true'); }
function prevItem(){ if(currentIndex > 0) openLightbox(window.GALLERY[currentIndex-1].id); }
function nextItem(){ if(currentIndex < window.GALLERY.length - 1) openLightbox(window.GALLERY[currentIndex+1].id); }

/* keyboard & touch */
document.addEventListener('keydown', (e)=>{ if(e.key==='Escape') closeLightbox(); if(e.key==='ArrowLeft') prevItem(); if(e.key==='ArrowRight') nextItem(); });
const lbContent = document.getElementById('lb-content');
if(lbContent){
  let touchStartX = 0, touchEndX = 0;
  lbContent.addEventListener('touchstart', (e)=>{ touchStartX = e.changedTouches[0].screenX; }, false);
  lbContent.addEventListener('touchend', (e)=>{ touchEndX = e.changedTouches[0].screenX; if(touchEndX <= touchStartX - 40) nextItem(); if(touchEndX >= touchStartX + 40) prevItem(); }, false);
}

/* attach lightbox UI controls */
document.addEventListener('DOMContentLoaded', ()=> {
  const closeBtn = document.getElementById('lb-close');
  const prevBtn = document.getElementById('lb-prev');
  const nextBtn = document.getElementById('lb-next');
  if(closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if(prevBtn) prevBtn.addEventListener('click', prevItem);
  if(nextBtn) nextBtn.addEventListener('click', nextItem);

  // mobile nav toggle
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mainNav = document.getElementById('main-nav');
  const siteHeader = document.getElementById('site-header');
  if(mobileToggle){
    mobileToggle.addEventListener('click', ()=>{
      const open = mainNav.classList.toggle('nav-open');
      mobileToggle.classList.toggle('toggle-active');
      mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      siteHeader.classList.toggle('header-mobile-open', open);
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
