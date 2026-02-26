import json
import os
import re

# ========================================================
# FOUNDRY SITE GENERATOR
# ========================================================
# This script builds individual SEO pages for every art piece
# and ensures the sitemap is updated.
# ========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
ART_DIR = os.path.join(BASE_DIR, 'art')

# Create art directory if missing
if not os.path.exists(ART_DIR):
    os.makedirs(ART_DIR)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def get_template(item):
    slug = slugify(item['title'])
    title = f"{item['title']} | Cyber-Eclectic Digital Surrealism | BasicGlitch"
    description = item.get('description', f"Explore {item['title']}, a unique piece of digital surrealism by BasicGlitch. Available as wall art, clothing, and tapestries.")
    image_url = item['file'] # This will be the WebP path now
    master_png = image_url.rsplit('.', 1)[0] + ".png"
    
    # Forensic Content (Target: 300+ words)
    # If the item has a 'forensic_analysis' key, use it; otherwise use the expanded placeholder
    analysis = item.get('forensic_analysis', "")
    if len(analysis.split()) < 300:
        analysis = f"""
        <p><strong>{item['title']}</strong> represents a pivotal moment in the <em>{item.get('style', 'Cyber-Eclectic')}</em> series, serving as a forensic deep-dive into the aesthetics of digital entropy. This work functions as a visual autopsy of the technological sublime, where neon saturations collide with the stark, unforgiving structures of the <em>Tech-Noir</em> tradition. From a technical standpoint, the piece utilizes complex layering and "glitch-artifacts" to simulate a state of quantum superposition—existing simultaneously as a cohesive vision and a fragmented digital signal. This intentional dissonance is designed to provoke a sense of "cyber-eclectic" wonder, challenging the viewer to find order within the meticulously orchestrated chaos.</p>
        
        <p>The thematic core of <strong>{item['title']}</strong> explores the intersection of organic form and synthetic architecture. In this specific vision, <strong>BasicGlitch</strong> investigates how light behaves when filtered through the lens of digital decay. The spectral color palette is not merely aesthetic; it is a narrative tool used to highlight the fragility of our digital interfaces. Each pixelated fracture and chromatic aberration serves as a forensic marker, indicating where the "signal" of the original inspiration was compromised and rebuilt into something more resilient and vibrant. This process of destruction and reconstruction is central to the <strong>Foundry</strong> philosophy: taking raw, chaotic data and processing it into high-fidelity artistic intelligence.</p>
        
        <p>For collectors and enthusiasts of surrealism, this piece offers a masterclass in modern digital composition. Whether displayed in a high-tech gaming sanctuary, a minimalist modern office, or as a focal point in a curated gallery of "The Resistance," <strong>{item['title']}</strong> commands attention. It is more than wall art; it is a forensic record of a digital dream, rendered with the uncompromising precision that defines the <strong>BasicGlitch</strong> persona. This piece is available for high-end digital licensing or as a premium physical artifact on apparel and large-scale tapestries, ensuring that the vision can be integrated into both digital and physical spaces with equal impact.</p>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Share+Tech+Mono&family=Rajdhani:wght@300..700&display=swap" rel="stylesheet">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<link rel="icon" type="image/png" href="https://basicglitch.art/favicon.png">
<link rel="canonical" href="https://basicglitch.art/art/{slug}.html">
<title>{title}</title>
<meta name="description" content="{description}">

<!-- Social Media -->
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
<script src="../assets/js/app.js?v=1.1" defer></script>
<script src="../assets/js/terminal.js" defer></script>
</head>
<body class="bg-tech-noir">

<header class="site-header">
  <div class="header-inner container">
    <a href="../index.html" class="brand">BasicGlitch</a>
    <nav class="nav">
      <a class="nav-link" href="../gallery.html">Gallery</a>
      <a class="nav-link" href="../forge.html">Neural Forge</a>
      <a class="nav-link" href="../commissions.html">Commissions</a>
      <a class="nav-link" href="../apparel.html">Apparel</a>
      <a class="nav-link" href="../about.html">About</a>
    </nav>
  </div>
</header>

<main class="section neon-grid-section" style="padding-top: 100px;">
  <div class="container art-showcase">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 60px; align-items: start;">
      
      <!-- Image Column -->
      <div class="art-frame" style="border: 1px solid var(--border); padding: 10px; background: rgba(0,0,0,0.4);">
        <picture>
            <source srcset="../{image_url}" type="image/webp">
            <img src="../{master_png}" alt="{item['title']} - {item.get('style', 'Digital Art')} by BasicGlitch" style="width: 100%; height: auto; box-shadow: 0 0 30px rgba(0,0,0,0.8);">
        </picture>
        <button class="lore-terminal-btn" onclick="openTerminal()">ACCESS_TERMINAL_V1.0.4</button>
      </div>

      <!-- Content Column -->
      <div class="art-details">
        <h1 class="cyber-title" style="font-size: 2.5rem; margin-bottom: 10px;">
            <span class="cyber-text" data-text="{item['title'].upper()}">{item['title'].upper()}</span>
        </h1>
        <p class="cyber-subtitle" style="color: var(--neon); margin-bottom: 30px; font-family: 'Orbitron';">COLLECTION: {item.get('style', 'UNCATEGORIZED').upper()}</p>
        
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

    sitemap_urls = []

    for item in gallery:
        slug = slugify(item['title'])
        file_path = os.path.join(ART_DIR, f"{slug}.html")
        
        content = get_template(item)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        sitemap_urls.append(f"https://basicglitch.art/art/{slug}.html")
        print(f"Generated: {slug}.html")

    print(f"\nSUCCESS: Generated {len(gallery)} individual art pages.")
    
    # Update sitemap.xml
    update_sitemap(sitemap_urls)

def update_sitemap(new_urls):
    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    import datetime
    today = datetime.date.today().isoformat()
    
    # Create basic sitemap structure
    sitemap_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Static pages
    static_pages = [
        ("https://basicglitch.art/", 1.0),
        ("https://basicglitch.art/gallery.html", 0.8),
        ("https://basicglitch.art/forge.html", 0.9),
        ("https://basicglitch.art/portfolio.html", 0.9),
        ("https://basicglitch.art/pup-fiction.html", 0.9),
        ("https://basicglitch.art/commissions.html", 0.9),
        ("https://basicglitch.art/apparel.html", 0.8),
        ("https://basicglitch.art/about.html", 0.7),
        ("https://basicglitch.art/contact.html", 0.7)
    ]
    
    for url, priority in static_pages:
        sitemap_content += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n'
    
    # New art pages
    for url in new_urls:
        sitemap_content += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.6</priority>\n  </url>\n'
        
    sitemap_content += '</urlset>'
    
    with open(sitemap_path, 'w') as f:
        f.write(sitemap_content)
    print("Sitemap updated.")

if __name__ == "__main__":
    generate()
