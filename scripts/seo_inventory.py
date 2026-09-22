"""SEO inventory for basicglitch.art.

Usage: python3 scripts/seo_inventory.py [--json OUT.json]

Measures per page: title (length), meta description (length), canonical,
OG tag count, Twitter tag count, JSON-LD block count + @types, image alt
coverage. Also builds the internal inlink graph across all site HTML.

Machine-generated pages (art/) are reported but never edited by hand.
"""
import glob
import json
import re
import sys
from collections import defaultdict

BASE = "https://basicglitch.art"

SLUG_FALLBACKS = {
    # hand-authored pages whose file stems differ from their slugs
    "broboticus-the-original": "broboticus.html",
    "pumpkin-and-honey-puppy-and-the-diner-robbery": "pup-fiction.html",
    "basicglitch-neon-1440p-optimized": "download-wallpapers.html",
    "the-screambot": "art/the-screambot.html",
}

EXCLUDE_HREFS = ("mailto:", "tel:", "http", "#", "javascript:")


def href_to_page(href, page_dir=""):
    """Map a relative/absolute href to a canonical site page key."""
    if not href:
        return None
    href = href.split("#")[0].split("?")[0].strip()
    if not href or href.startswith(EXCLUDE_HREFS):
        return None
    if href.startswith("/"):
        href = href[1:]
        # root-relative to root
        base = ""
    else:
        base = page_dir
    # resolve .. with simple normalization
    parts = []
    for seg in (base + href).split("/"):
        if seg == "..":
            if parts:
                parts.pop()
        elif seg and seg != ".":
            parts.append(seg)
    path = "/".join(parts)
    if not path:
        return "/"
    stem = path.removesuffix(".html")
    if path in ("index.html", "/"):
        return "/"
    if path.endswith(".html"):
        return path
    if stem in SLUG_FALLBACKS:
        return SLUG_FALLBACKS[stem]
    # art pages keep their art/ path; other extensionless treated as missing
    return None


def parse_page(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    head = html.split("</head>", 1)[0]
    title_m = re.search(r"<title>(.*?)</title>", head, re.S)
    title = title_m.group(1).strip() if title_m else ""
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', head)
    desc = desc_m.group(1).strip() if desc_m else ""
    canonical = bool(re.search(r'rel="canonical"', head))
    og = len(re.findall(r'property=["\']og:', head))
    tw = len(re.findall(r'(?:name|property)=["\']twitter:', head))
    ld_blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ld_types = []
    ld_valid = 0
    for b in ld_blocks:
        try:
            data = json.loads(b)
            ld_valid += 1
            nodes = data if isinstance(data, list) else [data]
            for n in nodes:
                if isinstance(n, dict):
                    t = n.get("@type", "?")
                    ld_types.append(t if isinstance(t, str) else ",".join(t))
        except Exception:
            ld_types.append("INVALID")
    # alt coverage for <img> tags
    imgs = re.findall(r"<img\b[^>]*>", html)
    imgs_alt = [i for i in imgs if re.search(r'\balt="[^"]+"', i)]
    return {
        "title": title,
        "title_len": len(title),
        "desc_len": len(desc),
        "canonical": canonical,
        "og": og,
        "twitter": tw,
        "jsonld_count": len(ld_blocks),
        "jsonld_valid": ld_valid,
        "jsonld_types": sorted(ld_types),
        "imgs": len(imgs),
        "imgs_with_alt": len(imgs_alt),
    }


def build_graph():
    pages = sorted(glob.glob("*.html")) + sorted(glob.glob("art/*.html"))
    pages = [p for p in pages if p != "404.html"]
    inlinks = defaultdict(set)
    outlinks = {}
    for p in pages:
        page_dir = (p.rsplit("/", 1)[0] + "/") if "/" in p else ""
        with open(p, encoding="utf-8") as f:
            html = f.read()
        targets = set()
        for href in re.findall(r'<a\b[^>]*href="([^"]*)"', html):
            t = href_to_page(href, page_dir)
            if t and t != p and t != "/":
                targets.add(t)
        outlinks[p] = sorted(targets)
        for t in targets:
            inlinks[t].add(p)
    return pages, inlinks, outlinks


def main():
    dump = "--json" in sys.argv
    out_path = sys.argv[sys.argv.index("--json") + 1] if dump else None

    pages, inlinks, outlinks = build_graph()
    rows = []
    for p in pages:
        info = parse_page(p)
        info["page"] = p
        info["inlinks"] = len(inlinks.get(p, ()))
        info["outlinks"] = len(outlinks.get(p, ()))
        rows.append(info)

    art_rows = [r for r in rows if r["page"].startswith("art/")]
    core_rows = [r for r in rows if not r["page"].startswith("art/")]

    def summarize(label, subset):
        if not subset:
            return
        print(f"\n=== {label} ({len(subset)} pages) ===")
        for r in subset:
            flag = ""
            if not r["canonical"] and r["page"] != "404.html":
                flag += " !canonical"
            if not r["desc_len"]:
                flag += " !desc"
            if r["og"] < 4:
                flag += " !og"
            if r["twitter"] < 4 and r["page"] != "404.html":
                flag += " !tw"
            if not r["jsonld_count"]:
                flag += " !ld"
            if r["imgs"] and r["imgs_with_alt"] < r["imgs"]:
                flag += f' alt {r["imgs_with_alt"]}/{r["imgs"]}'
            print(f'{r["page"]:44s} T{r["title_len"]:3d} D{r["desc_len"]:3d} '
                  f'in{r["inlinks"]:2d} out{r["outlinks"]:2d} ld{r["jsonld_count"]}'
                  f'{",".join(r["jsonld_types"]) if r["jsonld_types"] else ""}{flag}')

    summarize("CORE + HAND-AUTHORED", core_rows)
    summarize("ART (generator output)", art_rows)

    ins = sorted(((len(v), k) for k, v in inlinks.items()))
    print("\n=== INLINK DISTRIBUTION ===")
    for n, p in ins:
        print(f"{n:3d}  {p}")
    if art_rows:
        avg = sum(r["inlinks"] for r in art_rows) / len(art_rows)
        print(f"\nArt pages mean inlinks: {avg:.2f}")

    if dump:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"pages": rows,
                       "inlinks": {k: sorted(v) for k, v in inlinks.items()},
                       "outlinks": outlinks}, f, indent=1)
        print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
