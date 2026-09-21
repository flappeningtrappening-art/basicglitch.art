"""Quick functional check of lightbox swipe on :8000 (touch events only)."""
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8000"

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.route("**/beacon.min.js*", lambda r: r.fulfill(
        status=200, content_type="application/javascript", body="/* stub */"))
    page.route("**/cdn-cgi/rum*", lambda r: r.fulfill(
        status=200, content_type="application/json",
        headers={"access-control-allow-origin": "*"}, body="{}"))

    # --- gallery: open lightbox with a tap, then swipe ---
    page.goto(f"{BASE}/gallery.html", wait_until="domcontentloaded")
    page.wait_for_timeout(1600)
    card = page.locator(".gallery-card").first
    card.tap()
    page.wait_for_timeout(700)
    hidden = "hidden" in (page.locator("#lightbox").get_attribute("class") or "")
    print("lightbox opened by tap:", not hidden)
    if not hidden:
        title0 = page.locator("#lb-content h3").inner_text()
        # swipe left -> next
        page.locator("#lb-content").tap()
        page.wait_for_timeout(200)
        box = page.locator("#lb-content").bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        page.touchscreen.tap(cx, cy)  # settle
        page.evaluate("""([x, y]) => {
          const c = document.getElementById('lb-content');
          const mk = (t, x2, y2) => new PointerEvent(t, {pointerId: 7, pointerType: 'touch',
            clientX: x2, clientY: y2, bubbles: true, cancelable: true, isPrimary: true});
          c.dispatchEvent(mk('pointerdown', x, y));
          c.dispatchEvent(mk('pointermove', x - 30, y));
          c.dispatchEvent(mk('pointermove', x - 80, y));
          c.dispatchEvent(mk('pointerup', x - 80, y));
        }""", [cx, cy])
        page.wait_for_timeout(600)
        title1 = page.locator("#lb-content h3").inner_text()
        print("swipe left -> next:", title0 != title1, f"({title0!r} -> {title1!r})")
        # vertical-dominant swipe must NOT navigate
        title_before = title1
        page.evaluate("""([x, y]) => {
          const c = document.getElementById('lb-content');
          const mk = (t, x2, y2) => new PointerEvent(t, {pointerId: 8, pointerType: 'touch',
            clientX: x2, clientY: y2, bubbles: true, cancelable: true, isPrimary: true});
          c.dispatchEvent(mk('pointerdown', x, y));
          c.dispatchEvent(mk('pointermove', x + 10, y + 60));
          c.dispatchEvent(mk('pointerup', x + 15, y + 120));
        }""", [cx, cy])
        page.wait_for_timeout(500)
        title2 = page.locator("#lb-content h3").inner_text()
        print("vertical swipe ignored:", title2 == title_before)
        # swipe right -> previous
        page.evaluate("""([x, y]) => {
          const c = document.getElementById('lb-content');
          const mk = (t, x2, y2) => new PointerEvent(t, {pointerId: 9, pointerType: 'touch',
            clientX: x2, clientY: y2, bubbles: true, cancelable: true, isPrimary: true});
          c.dispatchEvent(mk('pointerdown', x, y));
          c.dispatchEvent(mk('pointermove', x + 30, y));
          c.dispatchEvent(mk('pointermove', x + 80, y));
          c.dispatchEvent(mk('pointerup', x + 80, y));
        }""", [cx, cy])
        page.wait_for_timeout(600)
        title3 = page.locator("#lb-content h3").inner_text()
        print("swipe right -> prev:", title3 == title0, f"({title3!r})")
        # close via Escape (app.js path still works)
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        closed = "hidden" in (page.locator("#lightbox").get_attribute("class") or "")
        print("Escape closes:", closed)

    # --- pup-fiction lightbox still opens/closes by tap ---
    page.goto(f"{BASE}/pup-fiction.html", wait_until="domcontentloaded")
    page.wait_for_timeout(900)
    img = page.locator(".card-img").first
    img.tap()
    page.wait_for_timeout(400)
    opened = "hidden" not in (page.locator("#lightbox").get_attribute("class") or "")
    print("pup-fiction lightbox opens by tap:", opened)
    page.locator("#lb-close").tap()
    page.wait_for_timeout(300)
    closed = "hidden" in (page.locator("#lightbox").get_attribute("class") or "")
    print("pup-fiction lightbox closes by tap:", closed)

    # --- collection cards navigate to art pages by design (app.js) — tap check ---
    page.goto(f"{BASE}/collection.html?id=broboticus", wait_until="domcontentloaded")
    page.wait_for_timeout(1600)
    ccard = page.locator(".gallery-card").first
    ccard.tap()
    page.wait_for_timeout(900)
    print("collection card tap navigates to art page:", "/art/" in page.url)
    browser.close()
