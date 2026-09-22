"""Per-group verification for the SEO sweep (server + Playwright in one process).

Usage: python3 scripts/seo/group_check.py art|hand|series
Exits non-zero on any failure.

The `series` group validates the generated /series/ layer end to end:
  * every non-flagship series has a page, flagships do not, retired
    categories are redirect stubs
  * every portfolio box resolves to an existing page (no gallery.html dumps,
    no links into retired redirect stubs)
  * each series page lists exactly its category's pieces and no others
  * every piece appears on at least one series page or flagship
  * portfolio boxes: series with 3+ pieces show >=3 showcase images, all of
    real member pieces of that box's series
  * crosslinks (flagship <-> Masters Remixed) both work
  * 0 console errors, 0 internal 404s, 0 overflow, desktop + mobile
  * all JSON-LD parses with required properties
  * sitemap contains every series page with an image entry and no retired URLs
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
    ("art/broboticus-the-original.html", "Broboticus: The Original", "BROBOTICUS"),
    ("art/sangre-de-cristos-neon.html", "Sangre De Cristos: Neon", "SANGRE DE CRISTOS"),
    ("art/gaia-of-the-wasteland.html", "Gaia of the Wasteland", "GAIA DIPTYCH"),
    ("art/sidepiece-dimepiece.html", "Sidepiece Dimepiece", "CYBER-ECLECTIC"),
]


def load_series_defs():
    with open("assets/data/series.json", encoding="utf-8") as f:
        return json.load(f)


def is_flagship_def(d):
    return bool(d.get("flagship_page") or d.get("page") or d.get("suppress_page"))


def is_redirect_def(d):
    return bool(d.get("redirect_to"))


def check_no_art_orphans():
    """Indexing-critical: every art page must receive >=1 static <a> inlink
    from somewhere on the site. Pages linked only from JS are invisible to
    discovery crawling."""
    import glob
    import os
    from collections import Counter
    targets = Counter()
    pages = sorted(glob.glob("*.html")) + sorted(glob.glob("art/*.html"))
    for p in pages:
        body = open(p, encoding="utf-8").read().split("</head>", 1)[-1]
        for href in re.findall(r'<a\b[^>]*href="([^"]+)"', body):
            m = re.match(r"(?:\.\./|/)?art/([\w-]+)\.html", href.split("#")[0])
            if m:
                targets["art/" + m.group(1) + ".html"] += 1
    files = sorted("art/" + f for f in os.listdir("art") if f.endswith(".html"))
    orphans = [f for f in files if targets[f] == 0]
    check(not orphans, f"no zero-inlink art pages (found {len(orphans)}: {orphans[:5]})")

HAND_PAGES = ["index.html", "gallery.html", "portfolio.html", "about.html",
              "commissions.html", "apparel.html", "contact.html",
              "download-wallpapers.html", "terms.html", "pup-fiction.html"]


def run_art(browser):
    # literal-traphouse used to be the whole Standalone category; that
    # category is retired into Cyber-Eclectic, so it now links out to its
    # Cyber-Eclectic family instead of the old standalone club.
    print("\n— art/literal-traphouse.html (cyber-eclectic family)")
    ctx, page, errors = new_page(browser)
    page.goto(f"{BASE}/art/literal-traphouse.html", wait_until="domcontentloaded")
    page.wait_for_timeout(400)
    head_txt = page.locator(".series-crosslinks-title").inner_text()
    check("CYBER-ECLECTIC" in head_txt,
          f"traphouse page: cyber-eclectic club label ({head_txt!r})")
    links = page.locator(".series-crosslinks a.series-card-link")
    check(links.count() == 3, f"traphouse page: 3 club links (found {links.count()})")
    ctx.close()

    for path, title, expected_label in ART_SAMPLES:
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
        check(expected_label in head_txt,
              f"{path}: crosslink label mentions family ({head_txt!r})")
        hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
        check(all(h and h.startswith("../art/") and h.endswith(".html") for h in hrefs),
              f"{path}: crosslink hrefs are art pages")
        own = path.split("/")[-1]
        check(own not in hrefs, f"{path}: crosslinks never link to self")
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

    # Pup Fiction flagship: the live scene card must statically link its art
    # page — after the Standalone club retired, that link is the Diner
    # Robbery page's only static inlink (no-orphan gate depends on it).
    pup = open("pup-fiction.html", encoding="utf-8").read()
    check('href="art/pumpkin-and-honey-puppy-and-the-diner-robbery.html"' in pup,
          "pup-fiction: live card links the Diner Robbery art page")

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


SERIES_JSONLD_REQUIRED = ("name", "url", "description", "creator", "image")


def run_series(browser):
    import os
    import posixpath

    defs = load_series_defs()
    redirects = [d for d in defs if is_redirect_def(d)]
    generated = [d for d in defs
                 if not is_flagship_def(d) and not is_redirect_def(d)]
    flagships = [d for d in defs if is_flagship_def(d)]

    with open("assets/data/gallery.json", encoding="utf-8") as f:
        gallery = json.load(f)
    by_title = {it["title"]: it for it in gallery}

    # ── structural: every non-flagship series has a generated page, retired
    # categories have redirect stubs ──
    for d in generated:
        path = f"series/{d['slug']}.html"
        check(os.path.exists(path), f"{d['category']}: page exists ({path})")
    for d in redirects:
        path = f"series/{d['slug']}.html"
        check(os.path.exists(path), f"{d['category']}: redirect stub exists ({path})")
    for d in flagships:
        if d.get("suppress_page"):
            check(not os.path.exists(f"series/{d['slug']}.html"),
                  f"{d['category']}: suppressed page absent")
        else:
            fp = d.get("flagship_page") or d.get("page")
            check(os.path.exists(fp),
                  f"{d['category']}: flagship page exists ({fp})")

    # ── expected membership: every piece carrying the category, no dedupe ──
    expected = {}
    for d in generated:
        members = [it["title"] for it in gallery
                   if d["category"] in it.get("categories", [])]
        expected[d["slug"]] = members

    # ── coverage: every piece appears on >=1 series page or flagship ──
    page_cats = {d["category"] for d in generated} | {d["category"] for d in flagships}
    uncovered = [it["title"] for it in gallery
                 if not (set(it.get("categories", [])) & page_cats)]
    check(not uncovered,
          f"every piece on a series page or flagship ({uncovered[:5] or 'clean'})")
    empty = [slug for slug, m in expected.items() if not m]
    check(not empty, f"no empty series pages ({empty or 'clean'})")

    # ── portfolio boxes resolve ──
    portfolio_html = open("portfolio.html", encoding="utf-8").read()
    box_hrefs = re.findall(
        r'<a href="([^"]+)" class="series-card[^"]*">', portfolio_html)
    redirect_hrefs = {f"series/{d['slug']}.html" for d in redirects}
    for href in box_hrefs:
        check(not href.endswith("gallery.html"),
              f"portfolio box no longer dumps to archive: {href}")
        check(href not in redirect_hrefs,
              f"portfolio box does not point at a retired redirect stub: {href}")
        check(os.path.exists(href), f"portfolio box resolves: {href}")
    check("broboticus.html" in box_hrefs and "pup-fiction.html" in box_hrefs,
          "flagship boxes still point at broboticus.html / pup-fiction.html")

    # ── box image audit: every showcase image belongs to a real member of
    # that box's series, and series with 3+ pieces show >=3 images (4 on
    # featured boxes) ──
    def member_asset_basenames(cats):
        allowed = set()
        for it in gallery:
            if not (set(it.get("categories", [])) & cats):
                continue
            allowed.add(posixpath.basename(it.get("file", "")))
            allowed.add(f"{it.get('id', '')}.jpg")
        return allowed

    box_defs = {}
    for href in box_hrefs:
        cats = set()
        if href.startswith("series/"):
            slug = href.split("/")[-1][:-len(".html")]
            d = next((x for x in generated if x["slug"] == slug), None)
            if d:
                cats = {d["category"]}
        else:
            cats = {x["category"] for x in flagships
                    if (x.get("flagship_page") or x.get("page")) == href}
        box_defs[href] = cats

    for m in re.finditer(
            r'<a href="([^"]+)" class="(series-card[^"]*)">(.*?)</a>',
            portfolio_html, re.S):
        href, cls, inner = m.group(1), m.group(2), m.group(3)
        imgs = re.findall(r'<img src="([^"]+)"', inner)
        cats = box_defs.get(href, set())
        if not cats:
            continue
        members = [it for it in gallery
                   if set(it.get("categories", [])) & cats]
        allowed = member_asset_basenames(cats)
        foreign = [src for src in imgs
                   if posixpath.basename(src) not in allowed]
        check(not foreign,
              f"box {href}: all showcase images are real member pieces ({foreign[:3] or 'clean'})")
        want = min(4, len(members)) if "series-card--featured" in cls \
            else min(3, len(members))
        check(len(imgs) >= want,
              f"box {href}: {len(members)} members -> >= {want} showcase images "
              f"(found {len(imgs)})")

    # ── sitemap coverage ──
    sm = open("sitemap.xml", encoding="utf-8").read()
    for d in generated:
        loc = f"https://basicglitch.art/series/{d['slug']}.html"
        check(loc in sm, f"sitemap contains {loc}")
        block = sm.split(loc, 1)[1].split("</url>", 1)[0] if loc in sm else ""
        check("<image:loc>" in block,
              f"sitemap image entry for {d['slug']}")
    for d in flagships:
        if d.get("suppress_page"):
            continue
        check(f"https://basicglitch.art/series/{d['slug']}.html" not in sm,
              f"sitemap excludes flagship/suppressed slug {d['slug']}")
    for d in redirects:
        check(f"https://basicglitch.art/series/{d['slug']}.html" not in sm,
              f"sitemap excludes retired redirect slug {d['slug']}")

    # ── per-page live checks ──
    member_pages = set()
    for d in generated:
        path = f"series/{d['slug']}.html"
        print(f"\n— {path}")
        ctx, page, errors = new_page(browser)
        page.goto(f"{BASE}/{path}", wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        # desktop + mobile overflow
        ovf = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ovf <= 1, f"{path}: no horizontal overflow desktop ({ovf}px)")
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(250)
        ovf_m = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ovf_m <= 1, f"{path}: no horizontal overflow mobile ({ovf_m}px)")
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(250)

        # unique title + meta description
        title = page.title()
        check(title == f"{d['name']} | BasicGlitch",
              f"{path}: unique title ({title!r})")
        meta_desc = page.locator("meta[name='description']").get_attribute("content") or ""
        check(20 <= len(meta_desc) <= 165, f"{path}: meta description length ({len(meta_desc)})")
        canon = page.locator("link[rel='canonical']").get_attribute("href") or ""
        check(canon == f"https://basicglitch.art/{path}", f"{path}: canonical ({canon})")
        check((page.locator("meta[property='og:image']").get_attribute("content") or "").startswith(
            "https://basicglitch.art/assets/images/"), f"{path}: OG image absolute")

        # JSON-LD: parses + required properties
        nodes = load_jsonld(page.content())
        check(nodes and all(n is not None for n in nodes), f"{path}: all JSON-LD parses")
        cp = next((n for n in nodes if n and n.get("@type") == "CollectionPage"), {})
        for req in SERIES_JSONLD_REQUIRED:
            check(bool(cp.get(req)), f"{path}: CollectionPage.{req} present")
        crumb = next((n for n in nodes if n and n.get("@type") == "BreadcrumbList"), {})
        items = crumb.get("itemListElement", [])
        check([i.get("name") for i in items] == ["BasicGlitch", "Portfolio", d["name"]],
              f"{path}: breadcrumb Home > Portfolio > Series")

        # grid membership: exactly this category's pieces, no others
        cards = page.locator(".gallery-card")
        # text_content() (not inner_text()): style.css uppercases rendered
        # card titles, and membership must compare against source-case titles.
        got_titles = [cards.nth(i).locator("h3").text_content().strip()
                      for i in range(cards.count())]
        check(sorted(got_titles) == sorted(expected[d["slug"]]),
              f"{path}: lists exactly its category's pieces "
              f"(got {len(got_titles)}, want {len(expected[d['slug']])})")
        hrefs = [cards.nth(i).get_attribute("href") for i in range(cards.count())]
        check(all(h and h.startswith("../art/") for h in hrefs),
              f"{path}: all cards link to art pages")
        for i in range(cards.count()):
            img = cards.nth(i).locator("img")
            if img.count():
                check(img.first.get_attribute("loading") == "lazy",
                      f"{path}: card img lazy")
                check(img.first.get_attribute("width") is not None
                      and img.first.get_attribute("height") is not None,
                      f"{path}: card img has dimensions")
                break

        # every card href resolves (no internal 404s from the grid)
        for h in hrefs:
            target = h.replace("../", "")
            member_pages.add(target)
            check(os.path.exists(target), f"{path}: card target exists ({target})")

        check(not errors, f"{path}: no console/HTTP errors ({errors[:3]})")
        ctx.close()

    # ── retired categories: stubs carry meta refresh + canonical to target ──
    for d in redirects:
        target = d["redirect_to"]
        path = f"series/{d['slug']}.html"
        print(f"\n— {path} (redirect stub)")
        stub = open(path, encoding="utf-8").read()
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', stub)
        check(canon is not None
              and canon.group(1) == f"https://basicglitch.art/series/{target}.html",
              f"{path}: canonical points at series/{target}.html "
              f"({canon.group(1) if canon else 'missing'})")
        refresh = re.search(r'http-equiv="refresh" content="([^"]+)"', stub)
        check(refresh is not None
              and f"url=https://basicglitch.art/series/{target}.html" in refresh.group(1),
              f"{path}: meta refresh targets series/{target}.html")
        check(os.path.exists(f"series/{target}.html"),
              f"{path}: redirect target page exists (series/{target}.html)")

    # ── crosslinks both directions ──
    print("\n— crosslinks")
    ctx, page, errors = new_page(browser)
    page.goto(f"{BASE}/broboticus.html", wait_until="domcontentloaded")
    page.wait_for_timeout(400)
    strip = page.locator(".series-xref-strip a")
    check(strip.count() == 1, "broboticus: cross-reference strip present (exactly one)")
    check(strip.first.get_attribute("href") == "series/masters-remixed.html",
          "broboticus: strip links to Masters Remixed series page")
    strip.first.click()
    page.wait_for_timeout(400)
    check(page.url.endswith("series/masters-remixed.html"),
          "broboticus: strip navigates to series page")
    back = page.locator(".series-xref a.series-xref-link")
    check(back.count() >= 1, "masters-remixed: reciprocal note present")
    check(back.first.get_attribute("href") == "../broboticus.html",
          "masters-remixed: note links back to broboticus.html")
    back.first.click()
    page.wait_for_timeout(400)
    check(page.url.endswith("broboticus.html"),
          "masters-remixed: note navigates back to flagship")
    check(not errors, f"crosslinks: no console/HTTP errors ({errors[:3]})")
    ctx.close()

    # ── flagship pages: crosslink strip is the ONLY visible edit; core gates hold ──
    for fp in ("broboticus.html", "pup-fiction.html"):
        ctx, page, errors = new_page(browser)
        page.goto(f"{BASE}/{fp}", wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        ovf = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ovf <= 1, f"{fp}: no overflow ({ovf}px)")
        check(not errors, f"{fp}: no console/HTTP errors ({errors[:3]})")
        ctx.close()

    # ── art-page lightbox gate still green (series cards navigate, not lightbox) ──
    ctx, page, errors = new_page(browser)
    page.goto(f"{BASE}/series/sangre-de-cristos.html", wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    first = page.locator(".gallery-card").first
    first.click()
    page.wait_for_timeout(500)
    check("/art/" in page.url, f"series card navigates to art page ({page.url})")
    ctx.close()

    print(f"\n— membership summary")
    for slug, members in sorted(expected.items()):
        print(f"  {slug}: {len(members)} pieces")


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
                check_no_art_orphans()
            if group in ("hand", "all"):
                run_hand(browser)
            if group in ("series", "all"):
                run_series(browser)
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
