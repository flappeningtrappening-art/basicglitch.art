import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
ART_DIR = os.path.join(BASE_DIR, 'art')

def slugify(title):
    s = (title or '').lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_\-]+', '-', s)
    return s.strip('-')

def build_art_page_html(item, slug):
    title = item.get('title', 'Untitled')
    file_rel = item.get('file', '')
    categories = item.get('categories', ['Cyber-Eclectic'])
    styles = item.get('styles', ['Surrealism'])
    description = item.get('description', '')
    date = item.get('date', '2026-01-01')
    
    series_cats = [c for c in categories if c not in ('Available for Purchase', 'New Arrivals', 'Personal Projects', 'Personal Project')]
    series_str = ' · '.join(series_cats) if series_cats else 'CYBER-ECLECTIC'
    
    clean_desc = re.sub(r'<[^>]+>', '', description).replace('"', '&quot;').strip()
    meta_desc = (clean_desc[:157] + '...') if len(clean_desc) > 160 else clean_desc
    
    is_video = item.get('type') == 'video' or file_rel.lower().endswith(('.mp4', '.mov', '.webm'))
    
    if is_video:
        media_html = f'''        <div class="video-container" style="position:relative; width:100%; border-radius:4px; overflow:hidden;">
          <video controls autoplay loop muted playsinline style="width:100%; height:auto; box-shadow:0 0 30px rgba(0,255,247,0.2);">
            <source src="../{file_rel}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>'''
    else:
        base, ext = os.path.splitext(file_rel)
        webp_rel = base + '.webp'
        png_rel = base + '.png'
        jpg_rel = base + '.jpg'
        
        has_webp = os.path.exists(os.path.join(BASE_DIR, webp_rel))
        fallback_rel = file_rel
        if not os.path.exists(os.path.join(BASE_DIR, fallback_rel)):
            if os.path.exists(os.path.join(BASE_DIR, png_rel)):
                fallback_rel = png_rel
            elif os.path.exists(os.path.join(BASE_DIR, jpg_rel)):
                fallback_rel = jpg_rel
        
        if has_webp:
            media_html = f'''        <picture>
          <source srcset="../{webp_rel}" type="image/webp">
          <img src="../{fallback_rel}" alt="{title} - Digital Art by BasicGlitch" style="width:100%; height:auto; box-shadow:0 0 30px rgba(0,0,0,0.8); border-radius:4px;">
        </picture>'''
        else:
            media_html = f'''        <img src="../{fallback_rel}" alt="{title} - Digital Art by BasicGlitch" style="width:100%; height:auto; box-shadow:0 0 30px rgba(0,0,0,0.8); border-radius:4px;">'''

    if '<p>' in description:
        desc_paragraphs = description
    else:
        parts = [p.strip() for p in description.split('\n\n') if p.strip()]
        if not parts:
            parts = [description]
        desc_paragraphs = '\n'.join([f'          <p>{p}</p>' for p in parts])

    inquire_subject = f"Inquiry: {title}"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Share+Tech+Mono&family=Rajdhani:wght@300..700&display=swap" rel="stylesheet">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="#050505">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/png" href="https://basicglitch.art/favicon.webp">
<link rel="canonical" href="https://basicglitch.art/art/{slug}.html">
<title>{title} | Cyber-Eclectic Digital Surrealism | BasicGlitch</title>
<meta name="description" content="{meta_desc}">

<!-- Social Media / Open Graph -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://basicglitch.art/art/{slug}.html">
<meta property="og:title" content="{title} | Cyber-Eclectic Digital Surrealism | BasicGlitch">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://basicglitch.art/{file_rel}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://basicglitch.art/art/{slug}.html">
<meta name="twitter:title" content="{title} | BasicGlitch">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://basicglitch.art/{file_rel}">

<link rel="stylesheet" href="../assets/css/style.css">
<style>
    .forensic-description p {{ margin-bottom: 22px; }}
    .forensic-description em {{ color: var(--neon-mag); font-style: normal; font-weight: bold; }}
    .art-details {{ padding: 25px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 8px; }}
    .back-nav-link {{ display: inline-flex; align-items: center; gap: 8px; color: var(--neon); font-family: 'Share Tech Mono', monospace; font-size: 0.9rem; text-decoration: none; margin-bottom: 25px; transition: opacity 0.2s; }}
    .back-nav-link:hover {{ opacity: 0.8; text-decoration: underline; }}
</style>
<script src="../assets/js/app.js?v=1.2" defer></script>
<script src="../assets/js/dynamic-effects.js" defer></script>
</head>
<body class="bg-tech-noir">

<header class="site-header">
  <div class="header-inner container">
    <a href="../index.html" class="brand">BasicGlitch</a>
    <nav class="nav">
      <a class="nav-link" href="../gallery.html"><img src="../assets/icons/gallery.svg" alt="Gallery Icon"> Gallery</a>
      <a class="nav-link" href="../portfolio.html"><img src="../assets/icons/grid.svg" alt="Portfolio Icon"> Portfolio</a>
      <a class="nav-link" href="../broboticus.html"><img src="../assets/icons/robot.svg" alt="Broboticus Icon"> Broboticus</a>
      <a class="nav-link" href="../commissions.html"><img src="../assets/icons/commissions.svg" alt="Commissions Icon"> Commissions</a>
      <a class="nav-link" href="../apparel.html"><img src="../assets/icons/physical-products.svg" alt="Apparel Icon"> Apparel</a>
      <a class="nav-link" href="../about.html"><img src="../assets/icons/about.svg" alt="About Icon"> About</a>
      <a class="nav-link" href="../contact.html"><img src="../assets/icons/contact.svg" alt="Contact Icon"> Contact</a>
    </nav>
  </div>
</header>

<main class="section neon-grid-section" style="padding-top: 100px;">
  <div class="container art-showcase">
    <a href="../gallery.html" class="back-nav-link">‹ RETURN TO ARCHIVE</a>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 60px; align-items: start;">
      
      <!-- Image/Video Column -->
      <div class="art-frame" style="border: 1px solid var(--border); padding: 12px; background: rgba(0,0,0,0.5); border-radius: 8px;">
{media_html}
      </div>

      <!-- Content Column -->
      <div class="art-details">
        <h1 class="cyber-title" style="font-size: 2.3rem; margin-bottom: 10px;">
            <span class="cyber-text" data-text="{title.upper()}">{title.upper()}</span>
        </h1>
        <p class="cyber-subtitle" style="color: var(--neon); margin-bottom: 25px; font-family: 'Orbitron'; font-size: 0.95rem;">COLLECTION: {series_str.upper()}</p>
        
        <div class="forensic-description" style="font-family: 'Share Tech Mono', monospace; color: var(--fg); line-height: 1.8; font-size: 1.02rem; text-align: justify;">
{desc_paragraphs}
        </div>

        <div style="margin-top: 35px; border-top: 1px solid var(--border); padding-top: 25px;">
            <h3 style="font-family: 'Orbitron'; color: #fff; margin-bottom: 18px; font-size: 1.1rem;">ACQUIRE THIS VISION</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <a href="../commissions.html#standard-rates" class="btn-neon" style="text-align: center; font-size: 0.85rem; padding: 12px 20px;">VIEW RATES</a>
                <a href="../contact.html?subject={inquire_subject}" class="btn-neon" style="text-align: center; border-color: var(--neon-mag); color: var(--neon-mag); font-size: 0.85rem; padding: 12px 20px;">SEND INQUIRY</a>
            </div>
        </div>
      </div>

    </div>
  </div>
</main>

<footer class="site-footer">
  <div class="footer-inner container">
    <p>© 2025 BASICGLITCH | FORENSIC ART SYSTEM</p>
  </div>
</footer>

<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "0793c7934a22436cb1af2c9f24d6d22d"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''
    return html

def main():
    if not os.path.exists(GALLERY_JSON):
        print(f"Error: {GALLERY_JSON} not found!")
        return

    with open(GALLERY_JSON, 'r', encoding='utf-8') as f:
        gallery = json.load(f)

    if not os.path.exists(ART_DIR):
        os.makedirs(ART_DIR)

    valid_slugs = set()
    generated_count = 0

    for item in gallery:
        slug = slugify(item.get('title', ''))
        filename = f"{slug}.html"
        valid_slugs.add(filename)
        filepath = os.path.join(ART_DIR, filename)

        html_content = build_art_page_html(item, slug)
        with open(filepath, 'w', encoding='utf-8') as out:
            out.write(html_content)
        generated_count += 1

    print(f"Successfully generated {generated_count} art pages in {ART_DIR}")

    removed_count = 0
    for existing_file in os.listdir(ART_DIR):
        if existing_file.endswith('.html') and existing_file not in valid_slugs:
            old_path = os.path.join(ART_DIR, existing_file)
            os.remove(old_path)
            print(f"Removed stale / duplicate art page: {existing_file}")
            removed_count += 1

    print(f"Cleanup complete: Removed {removed_count} stale files. Total active art pages: {len(valid_slugs)}")

if __name__ == '__main__':
    main()
