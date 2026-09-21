"""Phase 1 mobile audit for basicglitch.art — read-only, quantified findings.

Usage: python3 scripts/audit_mobile.py [core|art|all]
Writes verification_screenshots/audit_mobile.json
"""
import json
import os
import re
import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8000"
OUT = "verification_screenshots"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE = [
    "index.html", "gallery.html", "portfolio.html", "broboticus.html",
    "pup-fiction.html", "collection.html", "commissions.html", "apparel.html",
    "about.html", "contact.html", "download-wallpapers.html", "terms.html",
    "404.html",
]
WIDTHS = [(320, 844), (360, 844), (390, 844), (768, 1024)]


def art_pages():
    with open(os.path.join(ROOT, "sitemap.xml")) as f:
        sm = f.read()
    return re.findall(r"<loc>https://basicglitch\.art/(art/[^<]+)</loc>", sm)


def audit_page(browser, path, fails):
    w0, h0 = WIDTHS[2]
    ctx = browser.new_context(viewport={"width": w0, "height": h0})
    page = ctx.new_page()
    page.route("**/beacon.min.js*", lambda r: r.fulfill(
        status=200, content_type="application/javascript", body="/* stub */"))
    page.route("**/cdn-cgi/rum*", lambda r: r.fulfill(
        status=200, content_type="application/json",
        headers={"access-control-allow-origin": "*"}, body="{}"))
    entry = {"page": path, "viewport_meta": None, "widths": {},
             "tap_targets": [], "inputs_small": [], "hover_only": [],
             "imgs_missing_attrs": 0, "imgs_total": 0}
    try:
        page.goto(f"{BASE}/{path}", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(700)

        entry["viewport_meta"] = page.evaluate(
            "() => document.querySelector('meta[name=viewport]')?.content || null")

        for w, h in WIDTHS:
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(250)
            ovf = page.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            # which element overflows
            culprits = page.evaluate("""() => {
              const vw = document.documentElement.clientWidth;
              const bad = [];
              document.querySelectorAll('body *').forEach(e => {
                const r = e.getBoundingClientRect();
                if (r.right > vw + 2 && r.width > 4) {
                  bad.push(`${e.tagName.toLowerCase()}${e.id ? '#'+e.id : ''}${e.className && typeof e.className === 'string' ? '.'+e.className.split(' ')[0] : ''} right=${Math.round(r.right)}`);
                }
              });
              return bad.slice(0, 6);
            }""")
            entry["widths"][str(w)] = {"overflow": ovf, "culprits": culprits}
            if ovf > 1:
                fails.append(f"{path} @{w}px: overflow {ovf}px {culprits[:3]}")

        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(250)

        # tap targets: interactive elements + effective hit area.
        # Skips elements that are not actually tappable at their center
        # (e.g. 3D-carousel cells with pointer-events: none).
        targets = page.evaluate("""() => {
          const out = [];
          const seen = new Set();
          document.querySelectorAll('a, button, input, select, textarea, [onclick], [role=button]').forEach(e => {
            const r = e.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            const cx = r.x + r.width / 2, cy = r.y + r.height / 2;
            const probe = document.elementFromPoint(cx, cy);
            if (!probe || (!probe.contains(e) && !e.contains(probe) && probe !== e)) return;
            const style = getComputedStyle(e);
            // effective hit area: padding box is clickable even for small inline content
            const w = Math.round(r.width), h = Math.round(r.height);
            const label = (e.textContent || e.getAttribute('aria-label') || e.name || e.tagName).trim().slice(0, 30);
            if (w < 44 || h < 44) {
              const key = `${e.tagName}|${label}|${w}x${h}`;
              if (!seen.has(key)) { seen.add(key); out.push({tag: e.tagName, label, w, h}); }
            }
          });
          return out.slice(0, 40);
        }""")
        entry["tap_targets"] = targets

        # input font sizes < 16px
        inputs = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('input, select, textarea').forEach(e => {
            const fs = parseFloat(getComputedStyle(e).fontSize);
            if (fs < 16) out.push({tag: e.tagName, name: e.name || e.id || '', fs});
          });
          return out;
        }""")
        entry["inputs_small"] = inputs
        for i in inputs:
            fails.append(f"{path}: input {i['tag']} {i['name']} font-size {i['fs']}px < 16")

        # hover-only revealed UI (opacity 0 until hover, inline onmouseover reveal)
        hover = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('[onmouseover]').forEach(e => {
            out.push((e.outerHTML || '').slice(0, 80));
          });
          return out;
        }""")
        entry["hover_only"] = hover

        # imgs without width/height or without lazy (below fold approximated: all but first)
        imgs = page.evaluate("""() => {
          const out = {total: 0, missing: 0};
          document.querySelectorAll('img').forEach((img, idx) => {
            out.total++;
            if (!img.hasAttribute('width') || !img.hasAttribute('height')) out.missing++;
          });
          return out;
        }""")
        entry["imgs_total"] = imgs["total"]
        entry["imgs_missing_attrs"] = imgs["missing"]

        status = "OK" if not any([
            entry["widths"][str(w)]["overflow"] > 1 for w, _ in WIDTHS]) else "ISSUES"
        ovf_str = ", ".join("%s:%d" % (w, entry["widths"][str(w)]["overflow"]) for w, _ in WIDTHS)
        print(f"  [{status}] {path} viewport={'ok' if entry['viewport_meta'] else 'MISSING'} "
              f"ovf={{{ovf_str}}} "
              f"tap_small={len(targets)} inputs_small={len(inputs)} imgs_no_wh={imgs['missing']}/{imgs['total']}")
    except Exception as e:
        entry["error"] = str(e)[:300]
        fails.append(f"{path}: audit failure: {str(e)[:200]}")
        print(f"  [FAIL] {path}: {str(e)[:120]}")
    finally:
        ctx.close()
    return entry


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else "core"
    pages = CORE if scope in ("core", "all") else []
    if scope in ("art", "all"):
        pages += art_pages()
    fails = []
    entries = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for p in pages:
            entries.append(audit_page(browser, p, fails))
        browser.close()
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/audit_mobile.json", "w") as f:
        json.dump({"scope": scope, "entries": entries, "fails": fails}, f, indent=1)
    print(f"AUDIT {scope}: {len(pages)} pages, {len(fails)} flagged findings")
    for x in fails[:80]:
        print("  -", x)


if __name__ == "__main__":
    main()
