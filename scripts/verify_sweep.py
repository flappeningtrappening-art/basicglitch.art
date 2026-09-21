"""Phase 5 verification sweep for basicglitch.art (chunked, fast waits).

Usage: python3 verify_sweep.py core|art1|art2|interactions
Writes verification_screenshots/results_<chunk>.json
"""
import json
import re
import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8000"
OUT = "verification_screenshots"

CORE = [
    "index.html", "gallery.html", "portfolio.html", "broboticus.html",
    "pup-fiction.html", "collection.html", "commissions.html", "apparel.html",
    "about.html", "contact.html", "download-wallpapers.html", "terms.html",
]
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}


def art_pages():
    with open("sitemap.xml") as f:
        sm = f.read()
    return re.findall(r"<loc>https://basicglitch\.art/(art/[^<]+)</loc>", sm)


def sweep_page(browser, url, label, viewport, fails):
    ctx = browser.new_context(viewport=viewport)
    page = ctx.new_page()
    # Stub the Cloudflare Web Analytics beacon so it behaves as it does in
    # production (on the real domain). Against localhost it would otherwise
    # always log CORS errors — test-environment noise, not site bugs.
    page.route("**/beacon.min.js*", lambda r: r.fulfill(
        status=200, content_type="application/javascript", body="/* beacon stub */"))
    page.route("**/cdn-cgi/rum*", lambda r: r.fulfill(
        status=200, content_type="application/json",
        headers={"access-control-allow-origin": "*"}, body="{}"))
    console_errors = []
    bad = []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("response", lambda r: bad.append((r.status, r.url))
            if r.status >= 400 else None)
    entry = {"label": label, "url": url, "console_errors": [], "bad_responses": [], "overflow": None}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(650)
        entry["overflow"] = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        real_errs = console_errors
        real_bad = [(s, u) for s, u in bad if "localhost:8000" in u]
        entry["console_errors"] = real_errs
        entry["bad_responses"] = [{"status": s, "url": u} for s, u in real_bad]
        entry["beacon_noise_ignored"] = len(console_errors) - len(real_errs)
        for ce in real_errs:
            fails.append(f"{label}: console: {ce[:160]}")
        for s, u in real_bad:
            fails.append(f"{label}: HTTP {s}: {u}")
        if entry["overflow"] > 1:
            fails.append(f"{label}: horizontal overflow {entry['overflow']}px")
        status = "OK" if not (real_errs or real_bad or entry["overflow"] > 1) else "FAIL"
        print(f"  [{status}] {label} err={len(real_errs)} bad={len(real_bad)} ovf={entry['overflow']}")
    except Exception as e:
        entry["error"] = str(e)[:300]
        fails.append(f"{label}: nav failure: {str(e)[:200]}")
        print(f"  [FAIL] {label}: {str(e)[:120]}")
    finally:
        ctx.close()
    return entry


def run_core(browser, fails):
    entries = []
    for p in CORE:
        for vp, tag in ((DESKTOP, ""), (MOBILE, " [mobile]")):
            entries.append(sweep_page(browser, f"{BASE}/{p}", p + tag, vp, fails))
    return entries


def run_art(browser, fails, lo, hi):
    pages = art_pages()
    entries = []
    for p in pages[lo:hi]:
        for vp, tag in ((DESKTOP, ""), (MOBILE, " [mobile]")):
            entries.append(sweep_page(browser, f"{BASE}/{p}", p + tag, vp, fails))
    return entries


def run_interactions(browser, fails):
    entries = []

    # --- 1. index: guardian clickable (topmost element + glitch class) ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(900)
    g = pg.locator("#guardian-guitarbot")
    box = g.bounding_box()
    if box:
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        topmost = pg.evaluate(
            "([x, y]) => { const e = document.elementFromPoint(x, y); return !!e && !!e.closest('#guardian-guitarbot'); }",
            [cx, cy])
        (print("  ok: guardian topmost at center (clickable)") if topmost
         else fails.append("guardian covered at its center — not clickable"))
        g.click()
        pg.wait_for_timeout(120)
        cls = g.get_attribute("class") or ""
        if "guardian-active" in cls:
            print("  ok: guardian click triggers glitch burst")
        else:
            fails.append("guardian click did not trigger guardian-active")
    else:
        fails.append("guardian has no bounding box")
    pg.screenshot(path=f"{OUT}/after/index.png")
    pg.close()

    # --- 2. gallery: lightbox by mouse / keyboard, trap, restore ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/gallery.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(1400)
    cards = pg.locator(".gallery-card")
    if cards.count() == 0:
        fails.append("gallery rendered zero cards")
    else:
        link = cards.nth(0).locator("a").first
        href = link.get_attribute("href")
        if href and href.startswith("art/"):
            print(f"  ok: crawl link href {href}")
        else:
            fails.append(f"crawl link href wrong: {href}")
        link.click()  # plain click on overlay -> lightbox
        pg.wait_for_timeout(500)
        if "hidden" in (pg.locator("#lightbox").get_attribute("class") or ""):
            fails.append("plain click on crawl link did not open lightbox")
        else:
            print("  ok: plain click opens lightbox")
        # keyboard open
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(400)
        if "hidden" not in (pg.locator("#lightbox").get_attribute("class") or ""):
            fails.append("Escape did not close lightbox")
        else:
            print("  ok: Escape closes lightbox")
        pg.evaluate("() => { const a = document.querySelector('.gallery-card a'); if (a) a.focus(); }")
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(500)
        if "hidden" not in (pg.locator("#lightbox").get_attribute("class") or ""):
            print("  ok: Enter on focused crawl link opens lightbox")
        else:
            fails.append("Enter on crawl link did not open lightbox")
        # focus trap: Tab from last focusable wraps to first
        trap = pg.evaluate(
            """() => {
              const lb = document.getElementById('lightbox');
              const f = Array.from(lb.querySelectorAll('button, [href]')).filter(e => e.offsetParent !== null);
              if (!f.length) return 'no-focusables';
              f[f.length-1].focus();
              const first = f[0];
              document.dispatchEvent(new KeyboardEvent('keydown', {key:'Tab', bubbles:true, cancelable:true}));
              return document.activeElement === first ? 'trapped' : 'NOT-TRAPPED';
            }""")
        if trap == "trapped":
            print("  ok: focus trap wraps Tab")
        else:
            fails.append(f"focus trap failed: {trap}")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(400)
        restored = pg.evaluate(
            "() => { const a = document.querySelector('.gallery-card a'); return document.activeElement === a; }")
        if restored:
            print("  ok: focus restored to card link after close")
        else:
            fails.append("focus not restored to triggering card after close")
    pg.screenshot(path=f"{OUT}/after/gallery.png")
    pg.close()

    # --- 3a. collection page cards navigate to art pages (by design in app.js) ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/collection.html?id=broboticus", wait_until="domcontentloaded")
    pg.wait_for_timeout(1400)
    card = pg.locator(".gallery-card").first
    if card.count():
        card.click()
        pg.wait_for_timeout(900)
        if "/art/" in pg.url:
            print("  ok: collection card navigates to art page")
        else:
            fails.append(f"collection card click did not navigate (url={pg.url})")
    else:
        fails.append("collection rendered no cards")
    pg.close()

    # --- 3b. pup-fiction own lightbox opens on the diner-robbery image ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/pup-fiction.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    img = pg.locator(".card-img").first
    if img.count():
        img.click()
        pg.wait_for_timeout(400)
        if "hidden" not in (pg.locator("#lightbox").get_attribute("class") or ""):
            print("  ok: pup-fiction lightbox opens")
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(300)
            if "hidden" in (pg.locator("#lightbox").get_attribute("class") or ""):
                print("  ok: pup-fiction lightbox closes (Escape via app.js)")
            else:
                fails.append("pup-fiction lightbox did not close")
        else:
            fails.append("pup-fiction lightbox did not open on image click")
    else:
        fails.append("pup-fiction has no .card-img")
    pg.close()

    # --- 4. 404 page structure (deep-URL serving is GitHub Pages runtime;
    #         python's http.server cannot reproduce it locally) ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/404.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(500)
    body = pg.locator("body").inner_text()
    if "RETURN_TO_BASE" in body:
        print("  ok: 404 page renders (RETURN_TO_BASE present)")
    else:
        fails.append("404 page content missing")
    href = pg.locator("a.btn").first.get_attribute("href")
    if href == "/":
        print("  ok: 404 home link root-relative '/'")
    else:
        fails.append(f"404 home link is {href}")
    robots = pg.locator("meta[name='robots']").get_attribute("content") or ""
    if "noindex" in robots:
        print("  ok: 404 noindex present")
    else:
        fails.append("404 missing noindex")
    desc = pg.locator("meta[name='description']").get_attribute("content") or ""
    if desc.strip():
        print("  ok: 404 meta description present")
    else:
        fails.append("404 missing meta description")
    # icons referenced from root must resolve from any depth
    icon_status = pg.evaluate(
        "async () => (await fetch('/assets/icons/home.svg')).status")
    if icon_status == 200:
        print("  ok: /assets/icons/home.svg resolves at root")
    else:
        fails.append(f"/assets/icons/home.svg -> {icon_status}")
    pg.screenshot(path=f"{OUT}/after/404.png")
    pg.close()

    # --- 5. art page screenshot ---
    pg = browser.new_context(viewport=DESKTOP).new_page()
    pg.goto(f"{BASE}/art/american-gothbotic.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(900)
    pg.screenshot(path=f"{OUT}/after/art-american-gothbotic.png")
    pg.close()
    print("  ok: screenshots written to after/")
    return entries


def main():
    chunk = sys.argv[1]
    fails = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        if chunk == "core":
            entries = run_core(browser, fails)
        elif chunk == "art1":
            entries = run_art(browser, fails, 0, 28)
        elif chunk == "art2":
            entries = run_art(browser, fails, 28, 56)
        elif chunk == "interactions":
            entries = run_interactions(browser, fails)
        else:
            print("unknown chunk"); sys.exit(2)
        browser.close()
    with open(f"{OUT}/results_{chunk}.json", "w") as f:
        json.dump({"chunk": chunk, "entries": entries, "fails": fails}, f, indent=1)
    print(f"CHUNK {chunk}: {len(fails)} failures")
    for x in fails:
        print("  FAIL:", x)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
