import json
import os
import re
from html import escape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY_JSON = os.path.join(BASE_DIR, 'assets/data/gallery.json')
ART_DIR = os.path.join(BASE_DIR, 'art')
SITE_URL = 'https://basicglitch.art'
CREATOR_URL = f'{SITE_URL}/about.html'

# Categories that describe availability rather than a series.
NON_SERIES_CATS = ('Available for Purchase', 'New Arrivals',
                   'Personal Projects', 'Personal Project', 'Personal')


def jsonld_escape(s):
    """Escape a string for safe inclusion inside a JSON-LD <script> block."""
    return (s or '').replace('&', '&amp;').replace('<', '&lt;') \
                     .replace('>', '&gt;').replace('\\', '\\\\') \
                     .replace('"', '\\"')


def slugify(title):
    s = (title or '').lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_\-]+', '-', s)
    return s.strip('-')

def img_dimensions(file_rel):
    """Return width/height attribute strings for an image path (empty if unknown)."""
    from PIL import Image
    full = os.path.join(BASE_DIR, file_rel)
    if not os.path.exists(full):
        return ''
    try:
        with Image.open(full) as im:
            w, h = im.size
        return f' width="{w}" height="{h}"'
    except Exception:
        return ''

def build_art_page_html(item, slug, gallery):
    title = item.get('title', 'Untitled')
    file_rel = item.get('file', '')
    categories = item.get('categories', ['Cyber-Eclectic'])
    styles = item.get('styles', ['Surrealism'])
    description = item.get('description', '')
    date = item.get('date', '2026-01-01')

    img_alt = (item.get('alt_text') or '').strip() \
        or f"{title} - digital art by BasicGlitch"
    img_alt_attr = escape(img_alt, quote=True)
    
    series_cats = [c for c in categories if c not in NON_SERIES_CATS]
    series_str = ' · '.join(series_cats) if series_cats else 'CYBER-ECLECTIC'
    series_name = series_cats[0] if series_cats else 'Cyber-Eclectic'
    
    plain_desc = re.sub(r'<[^>]+>', '', description)
    plain_desc = re.sub(r'\s+', ' ', plain_desc).strip()
    if len(plain_desc) > 160:
        plain_desc = plain_desc[:157].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
    meta_desc = escape(plain_desc, quote=True)
    
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
          <img src="../{fallback_rel}" alt="{img_alt}"{img_dimensions(fallback_rel)} loading="eager" fetchpriority="high" style="width:100%; height:auto; box-shadow:0 0 30px rgba(0,0,0,0.8); border-radius:4px;">
        </picture>'''
        else:
            media_html = f'''        <img src="../{fallback_rel}" alt="{img_alt}"{img_dimensions(fallback_rel)} loading="eager" fetchpriority="high" style="width:100%; height:auto; box-shadow:0 0 30px rgba(0,0,0,0.8); border-radius:4px;">'''

    if '<p>' in description:
        desc_paragraphs = description
    else:
        parts = [p.strip() for p in description.split('\n\n') if p.strip()]
        if not parts:
            parts = [description]
        desc_paragraphs = '\n'.join([f'          <p>{p}</p>' for p in parts])

    inquire_subject = f"Inquiry: {title}"

    canonical_url = f"{SITE_URL}/art/{slug}.html"
    image_abs = f"{SITE_URL}/{file_rel}"

    # ── "More from this series" cross-links (3 siblings, fallback: recent) ──
    # Deterministic rotation: each member links the next siblings in the
    # date-ordered family cycle, wrapping around. A plain "3 newest" window
    # would starve every older member of the family of inlinks (whole pages
    # orphaned); the rotation gives every piece both outbound links and
    # inbound links from its family while staying deterministic.
    #
    # Family definition, in priority order (all strictly from gallery.json):
    #   1. series categories (e.g. "Sangre de Cristos")
    #   2. any other shared category (e.g. "Personal")
    #   3. the standalone club: pieces sharing no category with any other
    #      piece keep each other company instead of becoming orphans.
    def family_of(item, all_items):
        cats = item.get('categories', [])
        for scope in (series_cats, cats):
            if scope:
                members = [it for it in all_items
                           if any(c in it.get('categories', []) for c in scope)]
                if len(members) >= 2:
                    return members, (scope[0] if scope == series_cats
                                     else next(c for c in scope
                                               if any(c in it.get('categories', [])
                                                      for it in all_items
                                                      if it is not item)))
        loners = [it for it in all_items
                  if not any(any(c in other.get('categories', [])
                                 for other in all_items if other is not it)
                             for c in it.get('categories', []))]
        if len(loners) >= 2 and item in loners:
            return loners, 'Standalone Works'
        return [], None

    family, family_label = family_of(item, gallery)
    if family:
        family.sort(key=lambda it: it.get('date', ''), reverse=True)
        k = next((i for i, it in enumerate(family)
                  if it.get('title') == title), 0)
        # The other members, ordered starting after the current piece,
        # wrapping at the end of the cycle.
        series_items = [family[(k + j) % len(family)]
                        for j in range(1, len(family))]
    else:
        series_items = []
    related = series_items[:3]
    primary = list(related)
    extra_label = None
    if len(related) < 3:
        # Small series: top the row up with recent pieces under an honest label.
        have = {it.get('title') for it in related}
        pool = [it for it in gallery
                if it.get('title') != title and it.get('title') not in have]
        pool.sort(key=lambda it: it.get('date', ''), reverse=True)
        extra = pool[:3 - len(related)]
        if extra:
            extra_label = 'RECENT FROM THE FOUNDRY'
            related = related + extra
    if family_label and len(family) >= 2:
        related_label = family_label.upper()
    else:
        related_label = 'RECENT FROM THE FOUNDRY'
    # Heading: "MORE FROM <FAMILY>" when the piece has a family; plain
    # label otherwise.
    related_heading = (f'MORE FROM {related_label}'
                       if family_label and len(family) >= 2
                       else related_label)
    # When the heading itself says "Recent from the Foundry", per-card
    # sub-labels would be redundant.
    if not family_label or len(family) < 2:
        extra_label = None

    crosslinks_html = ''
    if related:
        cards = []
        for it in related:
            r_slug = slugify(it.get('title', ''))
            r_title = it.get('title', 'Untitled')
            r_file = it.get('file', '')
            r_thumb = f'assets/images/gallery-thumbs/{it.get("id", "")}.jpg'
            if not os.path.exists(os.path.join(BASE_DIR, r_thumb)):
                r_thumb = r_file
            r_alt = escape((it.get('alt_text') or f"{r_title} - digital art by BasicGlitch"), quote=True)
            is_extra = extra_label and it not in primary
            sub = (f'\n        <span class="series-card-sub">{escape(extra_label)}</span>'
                   if is_extra else '')
            cards.append(
                f'''      <a class="series-card-link" href="../art/{r_slug}.html">
        <img src="../{r_thumb}" alt="{r_alt}" width="600" height="600" loading="lazy">
        <span class="series-card-name">{escape(r_title)}</span>{sub}
      </a>''')
        crosslinks_html = (
            f'\n    <div class="series-crosslinks">\n'
            f'      <h2 class="series-crosslinks-title">{escape(related_heading)}</h2>\n'
            + '\n'.join(cards) +
            f'\n      <a class="series-crosslinks-all" href="../gallery.html">VIEW THE FULL ARCHIVE →</a>\n'
            f'    </div>'
        )

    # ── JSON-LD: VisualArtwork + BreadcrumbList, strictly from gallery.json ──
    artwork_node = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "name": title,
        "url": canonical_url,
        "creator": {
            "@type": "Person",
            "name": "BasicGlitch",
            "url": CREATOR_URL,
        },
    }
    if plain_desc:
        artwork_node["description"] = plain_desc
    artwork_node["image"] = image_abs
    artwork_node["dateCreated"] = date
    artwork_node["genre"] = series_name
    if styles:
        artwork_node["keywords"] = ", ".join(styles)
    artwork_node["artMedium"] = "Digital Art"
    artwork_node["license"] = f"{SITE_URL}/terms.html"
    artwork_node["isFamilyFriendly"] = True

    breadcrumb_node = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "BasicGlitch",
                "item": f"{SITE_URL}/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "The Archive",
                "item": f"{SITE_URL}/gallery.html",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": canonical_url,
            },
        ],
    }

    def jsonld_script(node):
        payload = json.dumps(node, ensure_ascii=False, indent=2)
        payload = payload.replace('</', '<\\/')
        return f'<script type="application/ld+json">\n{payload}\n</script>'

    art_jsonld = jsonld_script(artwork_node)
    breadcrumb_jsonld = jsonld_script(breadcrumb_node)

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
<link rel="icon" type="image/webp" href="https://basicglitch.art/favicon.webp">
<link rel="canonical" href="{canonical_url}">
<title>{title} | Cyber-Eclectic Digital Surrealism | BasicGlitch</title>
<meta name="description" content="{meta_desc}">

<!-- Social Media / Open Graph -->
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{title} | Cyber-Eclectic Digital Surrealism | BasicGlitch">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="{image_abs}">
<meta property="og:image:alt" content="{img_alt_attr}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{canonical_url}">
<meta name="twitter:title" content="{title} | BasicGlitch">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="{image_abs}">

{art_jsonld}
{breadcrumb_jsonld}

<link rel="stylesheet" href="../assets/css/style.css">
<style>
    .art-description p {{ margin-bottom: 22px; }}
    .art-description em {{ color: var(--neon-mag); font-style: normal; font-weight: bold; }}
    .art-details {{ padding: 25px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 8px; }}
    .back-nav-link {{ display: inline-flex; align-items: center; gap: 8px; color: var(--neon); font-family: 'Share Tech Mono', monospace; font-size: 0.9rem; text-decoration: none; margin-bottom: 25px; transition: opacity 0.2s; }}
    .back-nav-link:hover {{ opacity: 0.8; text-decoration: underline; }}
    /* Mobile: 44px minimum tap targets for back link and CTA buttons */
    @media (max-width: 768px) {{
      .back-nav-link {{ padding: 15px 0; }}
      .btn-neon {{ padding: 12px 18px; }}
    }}
    /* ── MORE FROM THIS SERIES cross-links ── */
    .series-crosslinks {{ margin-top: 55px; }}
    .series-crosslinks-title {{ font-family: 'Orbitron'; color: #fff; margin-bottom: 18px; font-size: 1.1rem; }}
    .series-crosslinks {{ display: block; border-top: 1px solid var(--border); padding-top: 25px; }}
    .series-card-link {{ display: inline-flex; flex-direction: column; width: 200px; max-width: 31%; margin: 0 12px 12px 0; text-decoration: none; }}
    .series-card-link img {{ width: 100%; height: 200px; object-fit: cover; border-radius: 4px; border: 1px solid var(--border); transition: border-color 0.2s; }}
    .series-card-link:hover img {{ border-color: var(--neon); }}
    .series-card-name {{ font-family: 'Share Tech Mono', monospace; font-size: 0.78rem; color: var(--fg); margin-top: 8px; line-height: 1.3; }}
    .series-card-sub {{ display: block; font-family: 'Share Tech Mono', monospace; font-size: 0.62rem; letter-spacing: 0.15em; color: var(--muted); margin-top: 3px; }}
    .series-card-link:hover .series-card-name {{ color: var(--neon); text-decoration: underline; }}
    .series-card-link:focus-visible {{ outline: 2px solid var(--neon); outline-offset: 2px; }}
    .series-crosslinks-all {{ display: inline-block; margin-top: 10px; color: var(--neon); font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; text-decoration: none; padding: 13px 0; }}
    .series-crosslinks-all:hover {{ text-decoration: underline; }}
    @media (max-width: 768px) {{
      .series-card-link {{ width: 100%; max-width: none; flex-direction: row; align-items: center; margin: 0 0 14px; }}
      .series-card-link img {{ width: 96px; height: 96px; flex-shrink: 0; }}
      .series-card-name {{ margin: 0 0 0 12px; }}
    }}
</style>
<script src="../assets/js/app.js?v=1.2" defer></script>
<script src="../assets/js/dynamic-effects.js" defer></script>
</head>
<body class="bg-tech-noir" data-lightbox-mode="static">

<header class="site-header">
  <div class="header-inner container">
    <a href="../index.html" class="brand">BasicGlitch</a>
    <nav class="nav">
      <a class="nav-link" href="../gallery.html"><img src="../assets/icons/gallery.svg" alt="Gallery Icon" width="18" height="18"> Gallery</a>
      <a class="nav-link" href="../portfolio.html"><img src="../assets/icons/grid.svg" alt="Portfolio Icon" width="18" height="18"> Portfolio</a>
      <a class="nav-link" href="../broboticus.html"><img src="../assets/icons/robot.svg" alt="Broboticus Icon" width="18" height="18"> Broboticus</a>
      <a class="nav-link" href="../commissions.html"><img src="../assets/icons/commissions.svg" alt="Commissions Icon" width="18" height="18"> Commissions</a>
      <a class="nav-link" href="../apparel.html"><img src="../assets/icons/physical-products.svg" alt="Apparel Icon" width="18" height="18"> Apparel</a>
      <a class="nav-link" href="../about.html"><img src="../assets/icons/about.svg" alt="About Icon" width="18" height="18"> About</a>
      <a class="nav-link" href="../contact.html"><img src="../assets/icons/contact.svg" alt="Contact Icon" width="18" height="18"> Contact</a>
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
        
        <div class="art-description" style="font-family: 'Share Tech Mono', monospace; color: var(--fg); line-height: 1.8; font-size: 1.02rem; text-align: justify;">
{desc_paragraphs}
        </div>

        <div style="margin-top: 35px; border-top: 1px solid var(--border); padding-top: 25px;">
            <h2 style="font-family: 'Orbitron'; color: #fff; margin-bottom: 18px; font-size: 1.1rem;">ACQUIRE THIS VISION</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <a href="../commissions.html#standard-rates" class="btn-neon" style="text-align: center; font-size: 0.85rem; padding: 12px 20px;">VIEW RATES</a>
                <a href="../contact.html?subject={inquire_subject}" class="btn-neon" style="text-align: center; border-color: var(--neon-mag); color: var(--neon-mag); font-size: 0.85rem; padding: 12px 20px;">SEND INQUIRY</a>
            </div>
        </div>
      </div>

    </div>
{crosslinks_html}
  </div>
</main>

<footer class="site-footer">
  <div class="footer-inner container">
    <p>© 2026 BASICGLITCH | CYBER-ECLECTIC DIGITAL SURREALISM</p>
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

        html_content = build_art_page_html(item, slug, gallery)
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
