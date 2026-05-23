import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
ART_DIR = os.path.join(BASE_DIR, 'art')

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def get_template(item):
    slug = slugify(item['title'])
    title = f"{item['title']} | Cyber-Eclectic Digital Surrealism | BasicGlitch"
    description = item.get('description', f"Explore {item['title']}, a unique piece of digital surrealism by BasicGlitch.")
    image_url = item['file']
    master_png = image_url.rsplit('.', 1)[0] + ".png"
    analysis = item.get('forensic_analysis', "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Share+Tech+Mono&family=Rajdhani:wght@300..700&display=swap" rel="stylesheet">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<link rel="icon" type="image/png" href="https://basicglitch.art/favicon.webp">
<link rel="canonical" href="https://basicglitch.art/art/{slug}.html">
<title>{title}</title>
<meta name="description" content="{description}">

<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://basicglitch.art/{image_url}">

<link rel="stylesheet" href="../assets/css/style.css">
<style>
    .forensic-description p {{ margin-bottom: 25px; }}
    .forensic-description em {{ color: var(--neon-mag); font-style: normal; font-weight: bold; }}
    .art-details {{ padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 8px; }}
    .lore-terminal-btn {{ margin-top: 20px; font-family: 'Share Tech Mono', monospace; color: var(--muted); cursor: pointer; font-size: 0.8rem; border: none; background: none; }}
</style>
<script src="../assets/js/app.js?v=1.3" defer></script>
</head>
<body class="bg-tech-noir">

<header class="site-header">
  <div class="header-inner container">
    <a href="../index.html" class="brand">BasicGlitch</a>
    <nav class="nav">
      <a class="nav-link" href="../gallery.html"><img src="../assets/icons/gallery.svg" alt="Gallery Icon"> Gallery</a>
      <a class="nav-link" href="../portfolio.html"><img src="../assets/icons/grid.svg" alt="Portfolio Icon"> Portfolio</a>
      <a class="nav-link" href="../commissions.html"><img src="../assets/icons/commissions.svg" alt="Commissions Icon"> Commissions</a>
      <a class="nav-link" href="../apparel.html"><img src="../assets/icons/physical-products.svg" alt="Apparel Icon"> Apparel</a>
      <a class="nav-link" href="../about.html"><img src="../assets/icons/about.svg" alt="About Icon"> About</a>
      <a class="nav-link" href="../contact.html"><img src="../assets/icons/contact.svg" alt="Contact Icon"> Contact</a>
    </nav>
  </div>
</header>

<main class="section neon-grid-section" style="padding-top: 100px;">
  <div class="container art-showcase">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 60px; align-items: start;">
      
      <div class="art-frame" style="border: 1px solid var(--border); padding: 10px; background: rgba(0,0,0,0.4);">
        <picture>
            <source srcset="../{image_url}" type="image/webp">
            <img src="../{master_png}" alt="{item['title']} - Digital Art by BasicGlitch" style="width: 100%; height: auto; box-shadow: 0 0 30px rgba(0,0,0,0.8); cursor: pointer;" onclick="openLightbox('{item['id']}')">
        </picture>
      </div>

      <div class="art-details">
        <h1 class="cyber-title" style="font-size: 2.5rem; margin-bottom: 10px;">
            <span class="cyber-text" data-text="{item['title'].upper()}">{item['title'].upper()}</span>
        </h1>
        <p class="cyber-subtitle" style="color: var(--neon); margin-bottom: 30px; font-family: 'Orbitron';">COLLECTION: {item.get('styles', ['SURREALISM'])[0].upper()}</p>
        
        <div class="forensic-description" style="font-family: 'Share Tech Mono', monospace; color: var(--fg); line-height: 1.8; font-size: 1.05rem; text-align: justify;">
            {analysis}
        </div>

        <div style="margin-top: 40px; border-top: 1px solid var(--border); padding-top: 30px;">
            <h3 style="font-family: 'Orbitron'; color: #fff; margin-bottom: 20px;">ACQUIRE THIS VISION</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <a href="../commissions.html#standard-rates" class="btn-neon" style="text-align: center;">VIEW RATES</a>
                <a href="../contact.html?subject=Inquiry: {item['title']}" class="btn-neon" style="text-align: center; border-color: var(--neon-mag); color: var(--neon-mag);">SEND INQUIRY</a>
            </div>
        </div>
      </div>
    </div>
  </div>
</main>

<!-- Lightbox -->
<div id="lightbox" class="lightbox hidden" aria-hidden="true">
  <div class="lb-content" id="lb-content"></div>
  <button id="lb-close" class="lb-btn"><img src="../assets/icons/close.svg" alt="Close" style="width: 24px; filter: invert(1);"></button>
  <button id="lb-prev" class="lb-nav" style="left: 20px;"><img src="../assets/icons/back.svg" alt="Previous" style="width: 24px; filter: invert(1);"></button>
  <button id="lb-next" class="lb-nav" style="right: 20px;"><img src="../assets/icons/forward.svg" alt="Next" style="width: 24px; filter: invert(1);"></button>
</div>

<footer class="site-footer">
  <div class="footer-inner container">
    <p>© 2025 BASICGLITCH | FORENSIC ART SYSTEM</p>
  </div>
</footer>
</body>
</html>
"""

def generate():
    with open(GALLERY_JSON, 'r') as f:
        gallery = json.load(f)

    for item in gallery:
        slug = slugify(item['title'])
        file_path = os.path.join(ART_DIR, f"{slug}.html")
        content = get_template(item)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Generated: {slug}.html")

if __name__ == "__main__":
    generate()
