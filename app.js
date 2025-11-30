// ==============================
// Basic.Glitch — Gallery & Lightbox
// ==============================

// Load gallery JSON
const galleryGrid = document.getElementById('gallery-grid');
const categoryFilters = document.getElementById('category-filters');
const styleFilters = document.getElementById('style-filters');
const clearFiltersBtn = document.getElementById('clear-filters');
let galleryData = [];

// Fetch gallery data
fetch('./data/gallery.json')
  .then(res => res.json())
  .then(data => {
    galleryData = data;
    renderGallery(galleryData);
    setupFilters(galleryData);
  })
  .catch(err => console.error('Error loading gallery data:', err));

// ==============================
// Render Gallery
// ==============================
function renderGallery(data) {
  galleryGrid.innerHTML = '';

  data.forEach(item => {
    const card = document.createElement('div');
    card.classList.add('card', 'gallery-item');
    card.setAttribute('data-category', item.category);
    card.setAttribute('data-style', item.style);

    card.innerHTML = `
      <img src="assets/images/${item.path}" alt="${item.title}" class="gallery-img" />
      <h3>${item.title}</h3>
      <p class="muted">${item.description || ''}</p>
    `;

    card.addEventListener('click', () => openLightbox(item));
    galleryGrid.appendChild(card);
  });
}

// ==============================
// Filter Setup
// ==============================
function setupFilters(data) {
  const categories = [...new Set(data.map(item => item.category))];
  const styles = [...new Set(data.map(item => item.style))];

  // Populate category filters
  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'btn-small filter-btn';
    btn.innerText = cat;
    btn.addEventListener('click', () => applyFilter('category', cat));
    categoryFilters.appendChild(btn);
  });

  // Populate style filters
  styles.forEach(sty => {
    const btn = document.createElement('button');
    btn.className = 'btn-small filter-btn';
    btn.innerText = sty;
    btn.addEventListener('click', () => applyFilter('style', sty));
    styleFilters.appendChild(btn);
  });

  clearFiltersBtn.addEventListener('click', () => renderGallery(galleryData));
}

// ==============================
// Apply Filter
// ==============================
function applyFilter(type, value) {
  const filtered = galleryData.filter(item => item[type] === value);
  renderGallery(filtered);
}

// ==============================
// Lightbox
// ==============================
const lightbox = document.getElementById('lightbox');
const lbContent = document.getElementById('lb-content');
const lbClose = document.getElementById('lb-close');
const lbPrev = document.getElementById('lb-prev');
const lbNext = document.getElementById('lb-next');
let currentIndex = 0;
let lightboxItems = [];

function openLightbox(item) {
  lightboxItems = galleryData;
  currentIndex = galleryData.findIndex(i => i.path === item.path);
  showLightbox(currentIndex);
  lightbox.classList.remove('hidden');
  lightbox.setAttribute('aria-hidden', 'false');
}

function showLightbox(index) {
  const item = lightboxItems[index];
  lbContent.innerHTML = `<img src="assets/images/${item.path}" alt="${item.title}" style="max-width:100%; max-height:80vh; display:block; margin:0 auto;">`;
}

lbClose.addEventListener('click', closeLightbox);
lbPrev.addEventListener('click', () => navigateLightbox(-1));
lbNext.addEventListener('click', () => navigateLightbox(1));

function navigateLightbox(dir) {
  currentIndex = (currentIndex + dir + lightboxItems.length) % lightboxItems.length;
  showLightbox(currentIndex);
}

function closeLightbox() {
  lightbox.classList.add('hidden');
  lightbox.setAttribute('aria-hidden', 'true');
}
