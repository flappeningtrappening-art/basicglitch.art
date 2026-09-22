"""Shared data layer for generated /series/ pages.

Single source of truth chain:
  gallery.json categories  ->  series.json presentation config  ->  series/*.html

Design invariants (enforced here, verified in scripts/seo/group_check.py):
  * One generated page per non-flagship series category.
  * Flagship categories (Broboticus / Case Study 42 / Pup Fiction) keep their
    hand-authored canonical pages; generated /series/ pages are secondary.
  * Membership is category-driven: a piece appears on EVERY generated series
    page whose category it carries. Flagships are curated additions, not
    exclusions. A piece's primary category is the FIRST entry in its
    categories array (drives art-page crosslinks).
  * Retired categories carry a "redirect_to" slug and generate a meta-refresh
    + canonical stub so old URLs never 404.
  * Page copy derives ONLY from gallery.json data + this config. No invented lore.
"""
import json
import os
import re
from datetime import date

from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GALLERY_JSON = os.path.join(BASE_DIR, "assets/data/gallery.json")
SERIES_JSON = os.path.join(BASE_DIR, "assets/data/series.json")
SERIES_DIR = os.path.join(BASE_DIR, "series")
SITE_URL = "https://basicglitch.art"
CREATOR_URL = f"{SITE_URL}/about.html"

NON_SERIES_CATS = ("Available for Purchase", "New Arrivals",
                   "Personal Projects", "Personal Project", "Personal")


def load_gallery():
    with open(GALLERY_JSON, encoding="utf-8") as f:
        return json.load(f)


def load_series_config():
    with open(SERIES_JSON, encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    s = (text or "").lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_\-]+", "-", s)
    return s.strip("-")


def piece_slug(item):
    return slugify(item.get("title", ""))


def thumb_for(item):
    """600x600 square thumbnail used by gallery cards; exists for every piece."""
    rel = f"assets/images/gallery-thumbs/{item.get('id', '')}.jpg"
    return rel if os.path.exists(os.path.join(BASE_DIR, rel)) else item.get("file", "")


def raw_dimensions(file_rel):
    """(width, height) of the raw asset, for correct OG/lightbox dimensions."""
    full = os.path.join(BASE_DIR, file_rel or "")
    if file_rel and os.path.exists(full):
        try:
            with Image.open(full) as im:
                return im.size
        except Exception:
            pass
    return (1200, 1200)


def page_members(series_def, gallery):
    """Exact piece list for one series page.

    Members = every piece carrying this category. A piece may appear on
    several series pages; flagships are curated additions, not exclusions.
    """
    cat = series_def["category"]
    members = [it for it in gallery if cat in it.get("categories", [])]
    return sort_members(series_def, members)


def sort_members(series_def, members):
    mode = series_def.get("sort", "date_desc")
    if mode == "custom":
        order = {t: i for i, t in enumerate(series_def.get("display_order", []))}
        unknown = [m for m in members if m.get("title") not in order]
        if unknown:  # data safety: never drop a member silently
            ordered = [m for m in members if m.get("title") in order]
            ordered += sorted(unknown, key=lambda m: m.get("title", ""))
            return ordered
        return sorted(members, key=lambda m: order[m.get("title", "")])
    if mode == "date_asc":
        key = lambda m: (m.get("date", ""), m.get("title", ""))
        return sorted(members, key=key)
    if mode == "title":
        return sorted(members, key=lambda m: m.get("title", ""))
    # default: newest first, title as deterministic tie-break
    return sorted(members, key=lambda m: (m.get("date", ""), m.get("title", "")),
                  reverse=True)


def flagship_page(series_def):
    return series_def.get("flagship_page") or series_def.get("page") or None


def redirect_target(series_def):
    """Slug of the series page a retired category redirects to, if any."""
    return series_def.get("redirect_to") or None


def is_suppressed(series_def):
    """True when the owner has decided this category gets no generated page
    (e.g. all its members live on another series' page pending piece moves)."""
    return bool(series_def.get("suppress_page")) or bool(flagship_page(series_def))


def representative_image(series_def):
    rel = series_def.get("representative_image", "")
    if rel.lower().endswith((".mp4", ".mov", ".webm")):
        # Videos cannot be OG images; fall back to the square thumb.
        base = os.path.splitext(os.path.basename(rel))[0]
        rel = f"assets/images/gallery-thumbs/{base}.jpg"
    return rel


def build_redirect_stub_html(series_def, all_defs):
    """Meta refresh + canonical stub for a retired series URL."""
    name = series_def["name"]
    target_slug = redirect_target(series_def)
    target = next((d for d in all_defs if d.get("slug") == target_slug
                   and not redirect_target(d)), None)
    target_name = target["name"] if target else target_slug
    target_url = f"{SITE_URL}/series/{target_slug}.html"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} has moved | BasicGlitch</title>
<link rel="canonical" href="{target_url}">
<meta http-equiv="refresh" content="0; url={target_url}">
<link rel="icon" type="image/webp" href="{SITE_URL}/favicon.webp">
<style>
  body {{ background: #050505; color: #e0e0e0; font-family: 'Share Tech Mono', monospace;
    display: flex; align-items: center; justify-content: center; min-height: 100vh;
    margin: 0; text-align: center; padding: 20px; }}
  a {{ color: #00fff7; }}
</style>
</head>
<body>
<main>
  <p>The {name} series has moved.</p>
  <p>Redirecting to <a href="{target_url}">{target_name}</a>…</p>
</main>
</body>
</html>
'''


def build_series_page_html(series_def, gallery, all_defs):
    name = series_def["name"]
    slug = series_def["slug"]
    members = page_members(series_def, gallery)
    canonical_url = f"{SITE_URL}/series/{slug}.html"
    is_flagship = bool(series_def.get("page"))

    rep_rel = representative_image(series_def)
    rep_abs = f"{SITE_URL}/{rep_rel}"
    rep_w, rep_h = raw_dimensions(rep_rel)
    rep_alt = (series_def.get("representative_alt")
               or f"{name} - digital art series by BasicGlitch")

    description = (series_def.get("description") or "").strip()
    meta_desc = (series_def.get("meta_description") or description or "").strip()
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"

    card_class = series_def.get("card_class", "")
    kicker = (series_def.get("label") or series_def["category"]).upper()
    generated = date.today().isoformat()
    count = len(members)

    def esc(s):
        from html import escape
        return escape(s or "", quote=True)

    # ── grid cards (gallery-grid styling, lazy thumbs, real dims) ──
    cards = []
    for it in members:
        art_slug = piece_slug(it)
        title = it.get("title", "Untitled")
        t_rel = thumb_for(it)
        t_abs = f"{SITE_URL}/{t_rel}"
        tw, th = raw_dimensions(t_rel)
        is_video = (it.get("type") == "video"
                    or (it.get("file") or "").lower().endswith((".mp4", ".mov", ".webm")))
        badge = ('<span class="video-badge" '
                 'style="position:absolute;top:10px;left:10px;background:var(--neon-mag);'
                 'color:#000;padding:2px 8px;font-family:\'Share Tech Mono\';'
                 'font-size:0.7rem;font-weight:bold;border-radius:2px;z-index:2;">'
                 'MOTION_SIGNAL</span>') if is_video else ""
        cards.append(f'''      <a class="card gallery-card" href="../art/{art_slug}.html" aria-label="{esc(title)} - view piece page">
        <span class="series-thumb-wrap">
          <img src="../{t_rel}" alt="{esc((it.get('alt_text') or f'{title} - digital art by BasicGlitch'))}" width="{tw}" height="{th}" loading="lazy" decoding="async">{badge}
        </span>
        <h3>{esc(title)}</h3>
      </a>''')
    grid_html = "\n".join(cards)

    # ── cross-references (real data only) ──
    xref_html = ""
    for xr in series_def.get("cross_references", []):
        text = xr.get("text", "")
        href = xr.get("href", "")
        label = xr.get("label", "")
        if not (text and href):
            continue
        xref_html += (f'    <p class="series-xref">\n'
                      f'      <a href="{esc(href)}" class="series-xref-link">{esc(text)}</a>\n'
                      f'    </p>\n')

    # ── related series strip: other series pages, honest adjacency ──
    related = series_def.get("related_series", [])
    if related:
        links = []
        for rel in related:
            target = next((d for d in all_defs if d["category"] == rel), None)
            if not target:
                continue
            cls = target.get("card_class", "").replace("series-card--", "")
            links.append(f'<a class="series-also-link sa-{cls}" '
                         f'href="{target["slug"]}.html">{esc(target["name"])}</a>')
        if links:
            xref_html += ('    <p class="series-xref series-also">\n'
                          '      ALSO IN THIS UNIVERSE: ' + " · ".join(links) + "\n"
                          '    </p>\n')

    flagship_note = ""
    fp = flagship_page(series_def)
    if is_flagship and fp:
        flagship_note = (f'    <p class="series-flagship-note">\n'
                         f'      This series has a full story page: '
                         f'<a href="../{esc(fp)}">open the {esc(name)} flagship page</a>.\n'
                         f'    </p>\n')

    # ── JSON-LD: CollectionPage + BreadcrumbList, strictly real data ──
    collection_node = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": name,
        "url": canonical_url,
        "description": description or meta_desc,
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": "BasicGlitch", "url": f"{SITE_URL}/"},
        "creator": {"@type": "Person", "name": "BasicGlitch", "url": CREATOR_URL},
        "image": rep_abs,
        "hasPart": [
            {
                "@type": "WebPage",
                "name": it.get("title", "Untitled"),
                "url": f"{SITE_URL}/art/{piece_slug(it)}.html",
                "image": f"{SITE_URL}/{it.get('file', '')}",
            } for it in members
        ],
    }
    breadcrumb_node = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "BasicGlitch",
             "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Portfolio",
             "item": f"{SITE_URL}/portfolio.html"},
            {"@type": "ListItem", "position": 3, "name": name,
             "item": canonical_url},
        ],
    }

    def jsonld_script(node):
        payload = json.dumps(node, ensure_ascii=False, indent=2)
        payload = payload.replace("</", "<\\/")
        return f'<script type="application/ld+json">\n{payload}\n</script>'

    desc_paragraphs = "\n".join(
        f"      <p>{esc(p.strip())}</p>" for p in description.split("\n\n") if p.strip()
    ) or f"      <p>{esc(description)}</p>"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Share+Tech+Mono&family=Rajdhani:wght@300..700&display=swap" rel="stylesheet">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="#050505">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/webp" href="{SITE_URL}/favicon.webp">
<link rel="canonical" href="{canonical_url}">
<title>{esc(name)} | BasicGlitch</title>
<meta name="description" content="{esc(meta_desc)}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{esc(name)} | BasicGlitch">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:image" content="{esc(rep_abs)}">
<meta property="og:image:width" content="{rep_w}">
<meta property="og:image:height" content="{rep_h}">
<meta property="og:image:alt" content="{esc(rep_alt)}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{canonical_url}">
<meta name="twitter:title" content="{esc(name)} | BasicGlitch">
<meta name="twitter:description" content="{esc(meta_desc)}">
<meta name="twitter:image" content="{esc(rep_abs)}">

{jsonld_script(collection_node)}
{jsonld_script(breadcrumb_node)}

<link rel="stylesheet" href="../assets/css/style.css">
<style>
    .series-hero {{ padding: 120px 20px 40px; text-align: center; background: #000; position: relative; overflow: hidden; }}
    .series-hero::before {{ content: ''; position: absolute; inset: 0;
      background-image: linear-gradient(rgba(0,255,247,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,247,0.03) 1px, transparent 1px);
      background-size: 60px 60px; pointer-events: none; }}
    .series-kicker {{ font-family: 'Share Tech Mono', monospace; font-size: 0.72rem;
      letter-spacing: 0.35em; color: var(--neon); text-transform: uppercase; margin-bottom: 14px; }}
    .series-title {{ font-family: 'Orbitron', sans-serif; font-weight: 900;
      font-size: clamp(1.8rem, 6vw, 3.2rem); color: #fff; margin: 0 0 12px; line-height: 1.15; }}
    .series-count {{ font-family: 'Share Tech Mono', monospace; font-size: 0.75rem;
      letter-spacing: 0.2em; color: var(--muted); }}
    .series-count strong {{ color: var(--neon); }}
    .series-intro {{ max-width: 820px; margin: 0 auto; padding: 30px 20px 10px; }}
    .series-intro p {{ font-family: 'Chakra Petch', sans-serif; color: var(--fg);
      line-height: 1.85; font-size: 1.02rem; margin: 0 0 1.2em; opacity: 0.92; }}
    .series-grid-section {{ padding: 30px 20px 70px; background: var(--bg); }}
    .series-thumb-wrap {{ position: relative; display: block; }}
    .series-xref {{ max-width: 860px; margin: 26px auto 0; padding: 0 20px;
      font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; line-height: 1.8; }}
    .series-xref-link {{ color: var(--neon); text-decoration: none;
      border-bottom: 1px dashed rgba(0,255,247,0.4); padding: 2px 0; }}
    .series-xref-link:hover {{ text-decoration: underline; }}
    .series-also {{ color: var(--muted); letter-spacing: 0.08em; font-size: 0.75rem; }}
    .series-also-link {{ color: var(--neon); text-decoration: none; padding: 4px 2px; }}
    .series-also-link:hover {{ text-decoration: underline; }}
    .sa-grn {{ color: var(--neon-2); }} .sa-cyn {{ color: var(--neon); }}
    .sa-mag {{ color: var(--neon-mag); }} .sa-pur {{ color: var(--neon-pur); }}
    .sa-org {{ color: var(--neon-org); }} .sa-blu {{ color: var(--neon-blu); }}
    .sa-red {{ color: #ff3b3b; }} .sa-yel {{ color: #ffe44d; }}
    .series-flagship-note {{ max-width: 860px; margin: 18px auto 0; padding: 0 20px;
      font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: var(--muted); }}
    .series-flagship-note a {{ color: var(--neon-2); text-decoration: none;
      border-bottom: 1px dashed rgba(0,255,62,0.4); }}
    .series-flagship-note a:hover {{ text-decoration: underline; }}
    .series-generated {{ text-align: center; font-family: 'Share Tech Mono', monospace;
      font-size: 0.62rem; letter-spacing: 0.2em; color: var(--muted); opacity: 0.7;
      padding: 0 20px 30px; }}
    @media (max-width: 640px) {{
      .series-hero {{ padding-top: 100px; }}
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

<main>
  <section class="series-hero">
    <p class="series-kicker">// {esc(kicker)}</p>
    <h1 class="series-title">{esc(name)}</h1>
    <p class="series-count"><strong>{count}</strong> {"PIECE" if count == 1 else "PIECES"} IN THIS SERIES</p>
  </section>

  <section class="series-intro">
{desc_paragraphs}
{xref_html}{flagship_note}  </section>

  <section class="series-grid-section">
    <div class="container">
      <div class="gallery-grid {card_class}">
{grid_html}
      </div>
    </div>
  </section>

  <p class="series-generated">SERIES ARCHIVE // AUTO-GENERATED FROM THE FOUNDRY REGISTRY // {generated}</p>
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


def generate_all(verbose=True):
    gallery = load_gallery()
    defs = load_series_config()
    if not os.path.exists(SERIES_DIR):
        os.makedirs(SERIES_DIR)
    valid = set()
    written = 0
    stubs = 0
    seen_slugs = set()
    for sd in defs:
        if sd["slug"] in seen_slugs:
            continue
        seen_slugs.add(sd["slug"])
        # Flagship categories keep their hand-authored canonical page;
        # duplicate category entries (Broboticus / Case Study 42) collapse
        # onto one slug. Suppressed categories get no page by owner decision.
        if is_suppressed(sd):
            if verbose:
                why = (f"flagship: {flagship_page(sd)}" if flagship_page(sd)
                       else "suppressed by owner decision")
                print(f"  skip {sd['category']} ({why})")
            continue
        path = os.path.join(SERIES_DIR, f"{sd['slug']}.html")
        # Retired categories become redirect stubs (meta refresh + canonical).
        if redirect_target(sd):
            with open(path, "w", encoding="utf-8") as f:
                f.write(build_redirect_stub_html(sd, defs))
            valid.add(f"{sd['slug']}.html")
            stubs += 1
            if verbose:
                print(f"  series/{sd['slug']}.html  ({sd['category']} -> "
                      f"redirect stub to {redirect_target(sd)})")
            continue
        html = build_series_page_html(sd, gallery, defs)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        valid.add(f"{sd['slug']}.html")
        written += 1
        if verbose:
            n = len(page_members(sd, gallery))
            print(f"  series/{sd['slug']}.html  ({sd['category']} -> {n} pieces)")
    removed = 0
    for existing in os.listdir(SERIES_DIR):
        if existing.endswith(".html") and existing not in valid:
            os.remove(os.path.join(SERIES_DIR, existing))
            print(f"  removed stale series page: {existing}")
            removed += 1
    print(f"Series pages: {written} generated, {stubs} redirect stubs, {removed} removed.")
    return written


def regenerate_for_category(category, verbose=True):
    """Regenerate every series page affected by a category change."""
    gallery = load_gallery()
    defs = load_series_config()
    affected = [d for d in defs if d["category"] == category]
    if not affected:
        return 0
    if not os.path.exists(SERIES_DIR):
        os.makedirs(SERIES_DIR)
    for sd in affected:
        path = os.path.join(SERIES_DIR, f"{sd['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_series_page_html(sd, gallery, defs))
        if verbose:
            n = len(page_members(sd, gallery))
            print(f"  regenerated series/{sd['slug']}.html ({sd['category']} -> {n} pieces)")
    return len(affected)


def series_page_urls():
    """(path, representative_image) for every sitemap-eligible series page.
    Flagship, owner-suppressed, and retired-redirect categories are excluded."""
    defs = load_series_config()
    out = []
    seen = set()
    for d in defs:
        if is_suppressed(d) or redirect_target(d) or d["slug"] in seen:
            continue
        seen.add(d["slug"])
        out.append((f"series/{d['slug']}.html", representative_image(d)))
    return out


if __name__ == "__main__":
    generate_all()
