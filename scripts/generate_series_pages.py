"""Generate /series/<slug>.html pages from assets/data/series.json + gallery.json.

Usage:
    python3 scripts/generate_series_pages.py           # regenerate all
    python3 scripts/generate_series_pages.py --check   # exit 1 if any page is stale

Source of truth: gallery.json categories -> series.json presentation config.
Output is fully generated; never hand-edit series/*.html.
"""
import sys

from seo.series_lib import generate_all, load_gallery, load_series_config

if __name__ == "__main__":
    check = "--check" in sys.argv
    if check:
        # Dry-run comparison: regenerate into a temp map and diff against disk.
        import io
        import os
        import contextlib
        import tempfile
        from seo import series_lib

        gallery = load_gallery()
        defs = load_series_config()
        stale = []
        orig_dir = series_lib.SERIES_DIR
        with tempfile.TemporaryDirectory() as tmp:
            series_lib.SERIES_DIR = tmp
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    series_lib.generate_all(verbose=False)
                for sd in defs:
                    if series_lib.is_suppressed(sd):
                        continue
                    live = os.path.join(orig_dir, f"{sd['slug']}.html")
                    fresh = os.path.join(tmp, f"{sd['slug']}.html")
                    try:
                        with open(live, encoding="utf-8") as lf:
                            live_text = lf.read()
                    except OSError:
                        stale.append(f"series/{sd['slug']}.html (missing)")
                        continue
                    with open(fresh, encoding="utf-8") as ff:
                        if live_text != ff.read():
                            stale.append(f"series/{sd['slug']}.html")
            finally:
                series_lib.SERIES_DIR = orig_dir
        if stale:
            print("STALE series pages (run: python3 scripts/generate_series_pages.py):")
            for s in stale:
                print("  " + s)
            sys.exit(1)
        print("All series pages up to date.")
        sys.exit(0)

    generate_all()
