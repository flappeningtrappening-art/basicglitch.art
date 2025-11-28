/* app.js — gallery loader, filters, lightbox with swipe support */
async function fetchGallery(){
  const res = await fetch('/data/gallery.json', {cache:'no-store'});
  if(!res.ok) throw new Error('gallery.json not found — upload data/gallery.json and populate entries');
  return res.json();
}

function unique(arr){ return [...new Set(arr.flat())]; }
function el(tag, props={}, children=[]){ 
  const e=document.createElement(tag); 
  Object.assign(e,props); 
  (children||[]).forEach(c=> e.appendChild(typeof c==='string'? document.createTextNode(c):c)); 
  return e; 
}

function renderFilters(data){
  const cats = unique(data.map(i=>i.categories||[]));
  const styles = unique(data.map(i=>i.styles||[]));
  const catWrap = document.getElementById('category-filters');
  const styleWrap = document.getElementById('style-filters');
  catWrap.innerHTML=''; styleWrap.innerHTML='';
  cats.forEach(c=>{
    const b=el('button',{className:'btn-small'},[c]);
    b.addEventListener('click', ()=> toggleFilter('category', c, b));
    catWrap.appendChild(b); 
  });
  styles.forEach(s=>{
    const b=el('button',{className:'btn-small'},[s]);
    b.addEventListener('click', ()=> toggleFilter('style', s, b));
    styleWrap.appendChild(b);
  });
  document.getElementById('clear-filters').addEventListener('click', ()=> { 
    filters={category:[],style:[]}; 
    renderGrid(window.GALLERY); 
  });
}

let filters = {category:[], style:[]};
function toggleFilter(type, value, btn){ 
  const arr=filters[type]; 
  const idx=arr.indexOf(value); 
  if(idx===-1){ arr.push(value); btn.style.opacity=1 } 
  else { arr.splice(idx,1); btn.style.opacity=0.7 } 
  applyFilters(); 
}

function applyFilters(){ 
  let items = window.GALLERY.slice(); 
  if(filters.category.length) items = items.filter(it=> filters.category.some(c=> (it.categories||[]).includes(c))); 
  if(filters.style.length) items = items.filter(it=> filters.style.some(s=> (it.styles||[]).includes(s))); 
  if(items.length===0) console.warn('No gallery items match these filters'); 
  renderGrid(items); 
}

function renderGrid(items){ 
  const grid = document.getElementById('gallery-grid'); 
  grid.innerHTML=''; 
  if(!items.length){ 
    grid.appendChild(el('div',{className:'card'},[el('div',{},['No pieces match those filters.'])])); 
    return; 
  } 
  items.forEach(it=>{
    const card=el('div',{className:'card'});
    const img=el('img',{src:it.file, alt:it.title, loading:'lazy'});
    const h3=el('h3',{},[it.title]);
    const meta=el('p',{className:'muted'},[(it.categories||[]).join(' • ')]);
    const actions=el('div',{className:'row'},[]);
    const viewBtn=el('button',{className:'btn-small'},['View']);
    viewBtn.addEventListener('click', ()=> openLightbox(it.id));
    const orderLink=el('a',{className:'btn-small', href:'https://ko-fi.com/basicglitch', target:'_blank', rel:'noopener'},['Order']);
    actions.appendChild(viewBtn); 
    actions.appendChild(orderLink);
    card.appendChild(img); 
    card.appendChild(h3); 
    card.appendChild(meta); 
    card.appendChild(actions); 
    grid.appendChild(card); 
  }); 
}

function openLightbox(id){ 
  const item = window.GALLERY.find(i=> i.id===id); 
  if(!item) return; 
  const lb = document.getElementById('lightbox'); 
  const content = document.getElementById('lb-content'); 
  content.innerHTML = ''; 
  const img = document.createElement('img'); 
  img.src = item.file; 
  img.alt = item.title; 
  content.appendChild(img); 
  lb.classList.remove('hidden'); 
  lb.setAttribute('aria-hidden','false'); 
  currentIndex = window.GALLERY.indexOf(item); 
}

function closeLightbox(){ 
  const lb=document.getElementById('lightbox'); 
  lb.classList.add('hidden'); 
  lb.setAttribute('aria-hidden','true'); 
}

function prevItem(){ if(currentIndex>0) openLightbox(window.GALLERY[currentIndex-1].id); }
function nextItem(){ if(currentIndex < window.GALLERY.length-1) openLightbox(window.GALLERY[currentIndex+1].id); }

document.getElementById('lb-close').addEventListener('click', closeLightbox);
document.getElementById('lb-prev').addEventListener('click', prevItem);
document.getElementById('lb-next').addEventListener('click', nextItem);
document.addEventListener('keydown', (e)=>{
  if(e.key==='Escape') closeLightbox();
  if(e.key==='ArrowLeft') prevItem();
  if(e.key==='ArrowRight') nextItem();
});

/* touch swipe support for mobile */
let touchStartX = 0;
let touchEndX = 0;
const lbContent = document.getElementById('lb-content');
if(lbContent){
  lbContent.addEventListener('touchstart', (e)=>{ touchStartX = e.changedTouches[0].screenX; }, false);
  lbContent.addEventListener('touchend', (e)=>{ touchEndX = e.changed
