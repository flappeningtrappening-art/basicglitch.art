import os
from datetime import datetime

def main():
    base_url = "https://basicglitch.art"
    lastmod = datetime.now().strftime("%Y-%m-%d")
    
    core_pages = [
        {"path": "", "priority": "1.0", "changefreq": "weekly"},
        {"path": "gallery.html", "priority": "0.9", "changefreq": "weekly"},
        {"path": "portfolio.html", "priority": "0.9", "changefreq": "monthly"},
        {"path": "broboticus.html", "priority": "0.9", "changefreq": "monthly"},
        {"path": "pup-fiction.html", "priority": "0.8", "changefreq": "monthly"},
        {"path": "commissions.html", "priority": "0.8", "changefreq": "monthly"},
        {"path": "apparel.html", "priority": "0.7", "changefreq": "monthly"},
        {"path": "about.html", "priority": "0.7", "changefreq": "monthly"},
        {"path": "contact.html", "priority": "0.6", "changefreq": "yearly"},
        {"path": "download-wallpapers.html", "priority": "0.6", "changefreq": "monthly"},
        {"path": "collection.html", "priority": "0.6", "changefreq": "monthly"},
        {"path": "terms.html", "priority": "0.3", "changefreq": "yearly"},
    ]
    
    art_dir = "art"
    art_pages = []
    if os.path.exists(art_dir):
        for filename in sorted(os.listdir(art_dir)):
            if filename.endswith(".html"):
                art_pages.append(f"art/{filename}")

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
    
    sitemap_content += '  <!-- ── CORE PAGES ── -->\n'
    for page in core_pages:
        path = page["path"]
        loc = f"{base_url}/{path}" if path else f"{base_url}/"
        sitemap_content += f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{page["changefreq"]}</changefreq>\n    <priority>{page["priority"]}</priority>\n  </url>\n'
    
    sitemap_content += '\n  <!-- ── INDIVIDUAL ART PAGES ── -->\n'
    for page in art_pages:
        sitemap_content += f'  <url>\n    <loc>{base_url}/{page}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
    
    sitemap_content += '\n</urlset>'
    
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_content)
    
    print(f"Sitemap updated with {len(core_pages)} core pages and {len(art_pages)} art pages.")

if __name__ == "__main__":
    main()
