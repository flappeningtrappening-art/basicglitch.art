"""Live production verification at mobile viewport (390x844, touch, Fast 4G).

Usage: python3 scripts/live_verify.py
"""
import sys
from playwright.sync_api import sync_playwright

LIVE = "https://basicglitch.art"
PAGES = ["", "gallery.html", "art/american-gothbotic.html", "404.html",
         "contact.html", "portfolio.html"]

fails = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              is_mobile=True, has_touch=True)
    page = ctx.new_page()
    try:
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.emulateNetworkConditions",
                 {"offline": False, "latency": 150,
                  "downloadThroughput": 200000, "uploadThroughput": 93750})
    except Exception:
        pass

    console_errors, bad = [], []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("response", lambda r: bad.append((r.status, r.url)) if r.status >= 400 else None)

    for p in PAGES:
        url = f"{LIVE}/{p}"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1200)
            ovf = page.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            tap = page.evaluate("""() => {
              const out = [];
              document.querySelectorAll('a, button, input, select, textarea').forEach(e => {
                const r = e.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) return;
                const probe = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
                if (!probe || (!probe.contains(e) && !e.contains(probe) && probe !== e)) return;
                if (r.width < 44 || r.height < 44) out.push(e.tagName);
              });
              return out;
            }""")
            status = "OK" if ovf <= 1 and not tap else "ISSUES"
            print(f"[{status}] /{p} ovf={ovf} tap_small={len(tap)}")
            if ovf > 1:
                fails.append(f"/{p}: overflow {ovf}px")
            if tap:
                fails.append(f"/{p}: {len(tap)} small tap targets: {tap[:4]}")
        except Exception as e:
            fails.append(f"/{p}: {str(e)[:150]}")
            print(f"[FAIL] /{p}: {str(e)[:100]}")

    # swipe on live gallery
    page.goto(f"{LIVE}/gallery.html", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2500)
    cards = page.locator(".gallery-card")
    if cards.count():
        cards.first.tap()
        page.wait_for_timeout(1200)
        lb = page.locator("#lightbox")
        if "hidden" in (lb.get_attribute("class") or ""):
            fails.append("live gallery: tap did not open lightbox")
            print("[FAIL] live gallery lightbox")
        else:
            box = page.locator("#lb-content").bounding_box()
            cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            t0 = page.locator("#lb-content h3").inner_text()
            page.evaluate("""([x, y]) => {
              const c = document.getElementById('lb-content');
              const mk = (t, x2, y2) => new PointerEvent(t, {pointerId: 7, pointerType: 'touch',
                clientX: x2, clientY: y2, bubbles: true, cancelable: true, isPrimary: true});
              c.dispatchEvent(mk('pointerdown', x, y));
              c.dispatchEvent(mk('pointermove', x - 40, y));
              c.dispatchEvent(mk('pointerup', x - 80, y));
            }""", [cx, cy])
            page.wait_for_timeout(900)
            t1 = page.locator("#lb-content h3").inner_text()
            print(f"[{'OK' if t0 != t1 else 'FAIL'}] live gallery swipe next: {t0[:20]!r} -> {t1[:20]!r}")
            if t0 == t1:
                fails.append("live gallery: swipe did not advance")
    else:
        fails.append("live gallery: zero cards")

    real_bad = [(s, u) for s, u in bad if "basicglitch.art" in u or "localhost" not in u]
    if console_errors:
        fails.append(f"console errors: {console_errors[:3]}")
    if real_bad:
        fails.append(f"bad responses: {real_bad[:3]}")
    print(f"console errors: {len(console_errors)}, bad responses: {len(real_bad)}")
    browser.close()

print(f"\nLIVE VERIFY: {len(fails)} failures")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
