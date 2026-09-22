import os
import re
import sys
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://basicglitch.art"
GALLERY_JSON = os.path.join(BASE_DIR, "assets/data/gallery.json")

# Generated /series/ pages come from the shared series data layer so the
# sitemap can never drift from what generate_series_pages.py actually emits.
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
from seo.series_lib import series_page_urls  # noqa: E402

# Pages whose static <img> tags are harvested for <image:image> entries.
# (Art pages take their image data from gallery.json instead.)
CORE_PAGES = [
    {"path": "", "priority": "1.0", "changefreq": "weekly", "images": True},
    {"path": "gallery.html", "priority": "0.9", "changefreq": "weekly", "images": "gallery_json:10"},
    {"path": "portfolio.html", "priority": "0.9", "changefreq": "monthly", "images": True},
    {"path": "broboticus.html", "priority": "0.9", "changefreq": "monthly", "images": True},
    {"path": "pup-fiction.html", "priority": "0.8", "changefreq": "monthly", "images": True},
    {"path": "commissions.html", "priority": "0.8", "changefreq": "monthly", "images": True},
    {"path": "apparel.html", "priority": "0.7", "changefreq": "monthly", "images": True},
    {"path": "about.html", "priority": "0.7", "changefreq": "monthly", "images": True},
    {"path": "contact.html", "priority": "0.6", "changefreq": "yearly", "images": False},
    {"path": "download-wallpapers.html", "priority": "0.6", "changefreq": "monthly", "images": True},
    # collection.html is meta noindex: filtered out by is_noindex() below.
    {"path": "terms.html", "priority": "0.3", "changefreq": "yearly", "images": False},
]

META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
SRC_ATTR = re.compile(r'\bsrc="([^"]+)"', re.I)
ALT_ATTR = re.compile(r'\balt="([^"]*)"', re.I)
SKIP_PREFIXES = ("assets/icons/", "assets/fonts/")


def is_noindex(file_path):
    """True when the page's own <meta name=robots> carries noindex.

    Keeps the sitemap in sync with meta robots (e.g. subscriber-only
    download-wallpapers.html) without a second hand-edited list.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(os.path.join(root, file_path or "index.html"), encoding="utf-8") as f:
            html = f.read()
    except OSError:
        return True  # unreadable/missing page: never list it
    for tag in META_TAG.findall(html):
        tl = tag.lower()
        if (f'name="robots"' in tl or f"name='robots'" in tl):
            return "noindex" in tl
    return False


def harvest_page_images(path):
    """Extract (absolute_url, alt) from static <img> tags on a core page."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             path or "index.html")
    with open(file_path, encoding="utf-8") as f:
        html = f.read()
    images = []
    seen = set()
    for tag in IMG_TAG.findall(html):
        src_m = SRC_ATTR.search(tag)
        if not src_m:
            continue
        src = src_m.group(1)
        if src.startswith(("http", "//")) or src.endswith(".svg"):
            continue
        if any(src.startswith(p) for p in SKIP_PREFIXES):
            continue
        if src in seen:
            continue
        seen.add(src)
        alt_m = ALT_ATTR.search(tag)
        alt = (alt_m.group(1) if alt_m else "").strip()
        if not alt:
            continue  # images without meaningful alt are not worth listing
        images.append((f"{BASE_URL}/{src.lstrip('/')}", alt))
    return images[:20]


def gallery_representative_images(limit):
    with open(GALLERY_JSON, encoding="utf-8") as f:
        gallery = __import__("json").load(f)
    out = []
    for item in gallery:
        title = item.get("title", "")
        alt = (item.get("alt_text") or f"{title} - digital art by BasicGlitch").strip()
        out.append((f"{BASE_URL}/{item.get('file', '')}", alt))
        if len(out) >= limit:
            break
    return out


def image_xml(images):
    blocks = []
    for loc, alt in images:
        blocks.append(
            "    <image:image>\n"
            f"      <image:loc>{xml_escape(loc)}</image:loc>\n"
            f"      <image:caption>{xml_escape(alt)}</image:caption>\n"
            "    </image:image>")
    return "\n".join(blocks)


def main():
    lastmod = datetime.now().strftime("%Y-%m-%d")

    with open(GALLERY_JSON, encoding="utf-8") as f:
        import json
        gallery = json.load(f)
    art_by_slug = {}
    for item in gallery:
        slug = re.sub(r"[^\w\s-]", "", (item.get("title") or "").lower())
        slug = re.sub(r"[\s_\-]+", "-", slug).strip("-")
        art_by_slug[slug] = item

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n\n')

    sitemap_content += '  <!-- ── CORE PAGES ── -->\n'
    img_count = 0
    skipped = []
    for page in CORE_PAGES:
        path = page["path"]
        if is_noindex(path):
            skipped.append(path or "index.html")
            continue
        loc = f"{BASE_URL}/{path}" if path else f"{BASE_URL}/"
        sitemap_content += f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n'
        sitemap_content += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_content += f'    <priority>{page["priority"]}</priority>\n'
        if page.get("images"):
            if page["images"] == "gallery_json:10":
                images = gallery_representative_images(10)
            else:
                images = harvest_page_images(path)
            if images:
                sitemap_content += image_xml(images) + "\n"
                img_count += len(images)
        sitemap_content += '  </url>\n'

    sitemap_content += '\n  <!-- ── SERIES PAGES (generated) ── -->\n'
    series_pages = series_page_urls()
    for rel_path, rep_image in series_pages:
        if is_noindex(rel_path):
            skipped.append(rel_path)
            continue
        loc = f"{BASE_URL}/{rel_path}"
        sitemap_content += f'  <url>\n    <loc>{loc}</loc>\n'
        sitemap_content += f'    <lastmod>{lastmod}</lastmod>\n'
        sitemap_content += '    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n'
        if rep_image and os.path.exists(os.path.join(BASE_DIR, rep_image)):
            slug_title = rel_path.split("/")[-1][:-len(".html")].replace("-", " ").title()
            rep_abs = f"{BASE_URL}/{rep_image}"
            alt = f"{slug_title} - digital art series by BasicGlitch"
            sitemap_content += image_xml([(rep_abs, alt)]) + "\n"
            img_count += 1
        sitemap_content += '  </url>\n'

    sitemap_content += '\n  <!-- ── INDIVIDUAL ART PAGES ── -->\n'
    art_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")
    art_pages = []
    if os.path.exists(art_dir):
        for filename in sorted(os.listdir(art_dir)):
            if filename.endswith(".html"):
                art_pages.append(filename)

    for filename in art_pages:
        slug = filename[:-len(".html")]
        if is_noindex(os.path.join("art", filename)):
            skipped.append(f"art/{filename}")
            continue
        item = art_by_slug.get(slug, {})
        loc = f"{BASE_URL}/art/{filename}"
        sitemap_content += f'  <url>\n    <loc>{loc}</loc>\n'
        piece_date = (item.get("date") or "").strip()
        sitemap_content += f'    <lastmod>{piece_date or lastmod}</lastmod>\n'
        sitemap_content += '    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n'
        file_rel = item.get("file", "")
        if file_rel:
            title = item.get("title", "")
            alt = (item.get("alt_text") or f"{title} - digital art by BasicGlitch").strip()
            sitemap_content += image_xml([(f"{BASE_URL}/{file_rel}", alt)]) + "\n"
            img_count += 1
        sitemap_content += '  </url>\n'

    sitemap_content += '\n</urlset>'

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    core_skipped = [s for s in skipped if "/" not in s]
    series_skipped = [s for s in skipped if s.startswith("series/")]
    print(f"Sitemap updated: {len(CORE_PAGES) - len(core_skipped)} core pages, "
          f"{len(series_pages) - len(series_skipped)} series pages, "
          f"{len(art_pages) - len([s for s in skipped if s.startswith('art/')] )} art pages, "
          f"{img_count} <image:image> entries.")
    if skipped:
        print("Excluded (meta noindex): " + ", ".join(skipped))


if __name__ == "__main__":
    main()
