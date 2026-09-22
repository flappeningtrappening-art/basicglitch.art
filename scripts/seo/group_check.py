"""Per-group verification for the SEO sweep (server + Playwright in one process).

Usage: python3 scripts/seo/group_check.py art|hand
Exits non-zero on any failure.
"""
import functools
import http.server
import json
import re
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

PORT = 8000
BASE = f"http://localhost:{PORT}"
FAILS = []


def check(cond, msg):
    if cond:
        print(f"  ok: {msg}")
    else:
        FAILS.append(msg)
        print(f"  FAIL: {msg}")


def start_server():
    """Reuse an already-running server on :8000 when present (the workspace
    preview serves this same project root from disk). Otherwise start one."""
    import urllib.request
    try:
        with urllib.request.urlopen(f"{BASE}/index.html", timeout=3) as r:
            if r.status == 200:
                print(f"reusing existing server on :{PORT}")
                return None
    except Exception:
        pass
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=".")
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def load_jsonld(html):
    out = []
    for b in re.findall(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            html, re.S):
        try:
            out.append(json.loads(b))
        except Exception:
            out.append(None)
    return out


def new_page(browser, viewport=None):
    ctx = browser.new_context(viewport=viewport or {"width": 1440, "height": 900})
    page = ctx.new_page()
    page.route("**/beacon.min.js*", lambda r: r.fulfill(
        status=200, content_type="application/javascript", body="/* stub */"))
    page.route("**/cdn-cgi/rum*", lambda r: r.fulfill(
        status=200, content_type="application/json",
        headers={"access-control-allow-origin": "*"}, body="{}"))
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("response", lambda r: errors.append(f"HTTP {r.status}: {r.url}")
            if r.status >= 400 and "localhost:8000" in r.url else None)
    return ctx, page, errors


ART_SAMPLES = [
    ("art/broboticus-the-original.html", "Broboticus: The Original", "Broboticus"),
    ("art/sangre-de-cristos-neon.html", "Sangre De Cristos: Neon", "Sangre de Cristos"),
    ("art/gaia-of-the-wasteland.html", "Gaia of the Wasteland", "Gaia Diptych"),
    ("art/sidepiece-dimepiece.html", "Sidepiece Dimepiece", "Cyber-Eclectic"),
]

HAND_PAGES = ["index.html", "gallery.html", "portfolio.html", "about.html",
              "commissions.html", "apparel.html", "contact.html",
              "download-wallpapers.html", "terms.html", "pup-fiction.html"]


def run_art(browser):
    # inner-child.html is one of the two pages with no series: fallback label
    no_series_path = "art/inner-child.html"
    print(f"\n— {no_series_path} (no-series fallback)")
    ctx, page, errors = new_page(browser)
    page.goto(f"{BASE}/{no_series_path}", wait_until="domcontentloaded")
    page.wait_for_timeout(400)
    head_txt = page.locator(".series-crosslinks-title").inner_text()
    check("RECENT" in head_txt, f"no-series page: recent fallback label ({head_txt!r})")
    links = page.locator(".series-crosslinks a.series-card-link")
    check(links.count() == 3, f"no-series page: 3 recent links (found {links.count()})")
    ctx.close()

    for path, title, series in ART_SAMPLES:
        print(f"\n— {path}")
        ctx, page, errors = new_page(browser)
        page.goto(f"{BASE}/{path}", wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        html = page.content()
        nodes = load_jsonld(html)
        check(all(n is not None for n in nodes) and nodes,
              f"{path}: all JSON-LD parses")
        types = [n.get("@type") for n in nodes if n]
        check("VisualArtwork" in types, f"{path}: VisualArtwork present ({types})")
        check("BreadcrumbList" in types, f"{path}: BreadcrumbList present")

        va = next((n for n in nodes if n and n.get("@type") == "VisualArtwork"), {})
        check(va.get("name") == title, f"{path}: VA.name == {title!r}")
        for req in ("name", "image", "creator", "dateCreated"):
            check(bool(va.get(req)), f"{path}: VA.{req} present")
        check(va.get("creator", {}).get("name") == "BasicGlitch",
              f"{path}: VA.creator is Person BasicGlitch")
        check(va.get("url", "").endswith(path), f"{path}: VA.url is canonical")
        img_url = va.get("image", "")
        check(img_url.startswith("https://basicglitch.art/"), f"{path}: VA.image absolute")
        # no invented values: dateCreated must equal gallery.json date
        import json as _json
        with open("assets/data/gallery.json", encoding="utf-8") as f:
            g = _json.load(f)
        src = next((it for it in g if it["title"] == title), None)
        if src is None:
            check(False, f"{path}: title {title!r} not found in gallery.json")
            ctx.close()
            continue
        check(va.get("dateCreated") == src["date"], f"{path}: dateCreated matches gallery.json")

        crumb = next((n for n in nodes if n and n.get("@type") == "BreadcrumbList"), {})
        items = crumb.get("itemListElement", [])
        check(len(items) == 3 and all(i.get("name") and i.get("item")
                                      for i in items), f"{path}: breadcrumb 3 items complete")

        links = page.locator(".series-crosslinks a.series-card-link")
        check(links.count() == 3, f"{path}: 3 sibling links (found {links.count()})")
        head_txt = page.locator(".series-crosslinks-title").inner_text()
        if series:
            check(series.split()[0].upper() in head_txt,
                  f"{path}: crosslink label mentions series ({head_txt!r})")
        else:
            check("RECENT" in head_txt, f"{path}: recent-work fallback label ({head_txt!r})")
        hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
        check(all(h and h.startswith("../art/") and h.endswith(".html") for h in hrefs),
              f"{path}: crosslink hrefs are art pages")
        # lazy thumbnails + real alt
        for i in range(links.count()):
            img = links.nth(i).locator("img")
            check(img.get_attribute("loading") == "lazy", f"{path}: crosslink img lazy")
            check(bool((img.get_attribute("alt") or "").strip()), f"{path}: crosslink img alt")

        # crosslink navigation + keyboard access
        first_href = hrefs[0]
        links.nth(0).click()
        page.wait_for_timeout(400)
        check(page.url.endswith(first_href.replace("../", "")),
              f"{path}: clicking crosslink navigates to {first_href}")
        page.go_back()
        page.wait_for_timeout(300)
        page.evaluate("() => document.querySelector('.series-card-link').focus()")
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        check(page.url.endswith(first_href.replace("../", "")),
              f"{path}: Enter on focused crosslink navigates")
        check(not errors, f"{path}: no console/HTTP errors ({errors[:3]})")
        ovf = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ovf <= 1, f"{path}: no horizontal overflow ({ovf}px)")
        ctx.close()


def run_hand(browser):
    # index: WebSite + Person
    html = open("index.html", encoding="utf-8").read()
    nodes = load_jsonld(html)
    types = [n.get("@type") for n in nodes if n]
    check("WebSite" in types and "Person" in types, f"index: WebSite+Person ({types})")
    ws = next(n for n in nodes if n and n.get("@type") == "WebSite")
    check(ws.get("url") == "https://basicglitch.art/" and ws.get("name") == "BasicGlitch",
          "index: WebSite url/name")

    # gallery: ImageGallery with representative items
    html = open("gallery.html", encoding="utf-8").read()
    nodes = load_jsonld(html)
    ig = next((n for n in nodes if n and n.get("@type") == "ImageGallery"), None)
    check(ig is not None, "gallery: ImageGallery present")
    if ig:
        check(len(ig.get("image", [])) >= 10, "gallery: ImageGallery >=10 images")
        check(all(u.startswith("https://basicglitch.art/") for u in ig.get("image", [])),
              "gallery: ImageGallery absolute URLs")

    # portfolio: CollectionPage
    html = open("portfolio.html", encoding="utf-8").read()
    nodes = load_jsonld(html)
    check(any(n and n.get("@type") == "CollectionPage" for n in nodes),
          "portfolio: CollectionPage present")

    # about: Person completed
    html = open("about.html", encoding="utf-8").read()
    nodes = load_jsonld(html)
    p = next((n for n in nodes if n and n.get("@type") == "Person"), None)
    check(p is not None, "about: Person present")
    if p:
        for k in ("name", "url", "image", "jobTitle", "description"):
            check(bool(p.get(k)), f"about: Person.{k}")

    # live behavior: gallery lightbox mouse + keyboard, no errors anywhere
    ctx, page, errors = new_page(browser)
    page.goto(f"{BASE}/gallery.html", wait_until="domcontentloaded")
    page.wait_for_timeout(1200)
    link = page.locator(".gallery-card a").first
    link.click()
    page.wait_for_timeout(500)
    check("hidden" not in (page.locator("#lightbox").get_attribute("class") or ""),
          "gallery: mouse click opens lightbox")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.evaluate("() => document.querySelector('.gallery-card a').focus()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    check("hidden" not in (page.locator("#lightbox").get_attribute("class") or ""),
          "gallery: keyboard Enter opens lightbox")
    check(not errors, f"gallery: no console/HTTP errors ({errors[:3]})")
    ctx.close()

    for p in HAND_PAGES:
        ctx, page, errors = new_page(browser)
        page.goto(f"{BASE}/{p}", wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        check(not errors, f"{p}: no console/HTTP errors ({errors[:3]})")
        ovf = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ovf <= 1, f"{p}: no horizontal overflow ({ovf}px)")
        nodes = load_jsonld(page.content())
        check(all(n is not None for n in nodes), f"{p}: JSON-LD parses")
        if p != "download-wallpapers.html":
            check(page.locator('link[rel="canonical"]').count() == 1, f"{p}: canonical present")
        ctx.close()

    # mobile spot check of the new crosslinks
    ctx, page, errors = new_page(browser, {"width": 390, "height": 844})
    page.goto(f"{BASE}/art/broboticus-the-original.html", wait_until="domcontentloaded")
    page.wait_for_timeout(400)
    ovf = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(ovf <= 1, "mobile art page: no overflow")
    ctx.close()


def main():
    group = sys.argv[1] if len(sys.argv) > 1 else "all"
    try:
        srv = start_server()
    finally:
        pass
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            if group in ("art", "all"):
                run_art(browser)
            if group in ("hand", "all"):
                run_hand(browser)
            browser.close()
    finally:
        if srv:
            srv.shutdown()
    print(f"\nGROUP {group}: {len(FAILS)} failures")
    for f in FAILS:
        print("  FAIL:", f)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
