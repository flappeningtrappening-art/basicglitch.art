# BasicGlitch.art - Project Brain

## 1. Core Vision
A high-saturation, immersive digital portfolio for the artistic persona **BasicGlitch**. The site serves as a gallery for "Cyber-Eclectic Surrealism," "Tech-Noir," and psychedelic character design, blending 90s electronic aesthetics with modern web interactions.

## 2. Technical Stack
- **Frontend:** Vanilla HTML5, CSS3 (Custom Variables, Keyframe Animations), and Modern JavaScript.
- **Interactions:** Custom 3D CSS transforms for commission cards, perspective-based hover effects, and an interactive glitch engine.
- **Visuals:** SVG filters, backdrop-filters for glassmorphism (where applicable), and dual-layered animated neon grids.
- **Infrastructure:** Cloudflare Free Tier (DNS, Caching, Email Routing, Web Analytics).

## 3. Key Features
- **The Neon Grid:** A signature animated background using `linear-gradient` and `background-size` to create a moving 3D floor effect.
- **Interactive Glitch Engine:** A re-activated and enhanced `robot.js` system that features floating, interactive bots (Broboticus/Guitarbot). Clicking these bots triggers audio pulses and site-wide visual grid glitches.
- **Randomized Instagram Feed:** A client-side JavaScript engine that shuffles images from `assets/images/raw` to provide a dynamic "Social Feed" feel on every page load.
- **Cyber-Commission Tiers:** 5-tier service menu (Nano, Binary, Synthweave, Quantum, Singularity) with interactive 3D card flips.

## 4. Recent Updates & Fixes
- **Brand & Persona Unification:**
    - Standardized branding to **BasicGlitch** (one word, no space) across all headers, footers, and metadata.
    - Restricted the use of the name "Justin Lance" to the "About the Artist" bio only, establishing BasicGlitch as the primary artistic persona.
    - Updated the bio to highlight roots in **Newburgh, Indiana**.
- **SEO & Discoverability Overhaul:**
    - Unified all `<title>` tags to a standardized format (e.g., `The Archive | Digital Surrealism & Tech-Noir | BasicGlitch`).
    - Adopted **"Cyber-Eclectic Surrealism"** as the primary descriptive anchor for the site.
    - Removed all instances of "Justin Lance" from meta keywords, descriptions, and JSON-LD schema (except on the About page).
- **Interactive Enhancements:**
    - Integrated the `robot.js` glitch engine into `index.html` and `about.html`.
    - Added floating, pulsing robots that respond to click, touch, and keyboard (`R`, `G`) events.
    - Synced 90s-style electronic audio pulses with visual grid vibrations and hue-shifts.
- **Cleanup & Optimization:**
    - Deleted obsolete `gallery-template.csv`.
    - Removed redundant image sub-directories (`misc`, `products`, `originals`) and duplicate assets.
    - Standardized internal scripts (`backup.sh`, `process_art.py`, `watch_art.sh`) for brand consistency.
- **Corporate Infrastructure:**
    - Department-specific emails: `studio@`, `commissions@`, `licensing@`, `management@`, `press@`.
    - **Contact Page:** Department Directory grid with 5 distinct cards.
    - **Security:** Multiple "decrypting" email links handled via the `.secure-contact-link` class.

## 5. Maintenance Notes
- **Adding New Art to Feed:** Simply drop the new image into `assets/images/raw/` and add the filename to the `rawImages` array in `about.html`.
- **Styling Conventions:** All neon accents should use variables like `--neon` (Cyan), `--neon-mag` (Magenta), or `--neon-pur` (Purple).
- **Email Security:** To add a new secure email link, use the class `secure-contact-link` and attributes `data-user="username"` and `data-domain="basicglitch.art"`.

## 6. Cloudflare Infrastructure
- **Speed Demon Caching:** Edge Cache TTL (1 Month), Browser TTL (1 Day), Serve Stale Content enabled.
- **Ghostly Analytics:** Privacy-first JS beacon injected across all site pages.
    - **Email Routing:** Aliases forwarding to personal inbox: `studio@`, `commissions@`, `licensing@`, `management@`, `press@`.
    - **Discord Integration (Mainframe):** Recommended connecting Formspree to a Discord Webhook (named "BasicGlitch Mainframe") to receive real-time alerts for signups and inquiries, bypassing email spam filters.
## 7. Previous Session Updates (2026-01-11)
- **Monetization & Lead Gen:**
    - Added **"Broboticus" Commission Tier** ($99) to `commissions.html`.
    - Implemented **Email Signup Forms** (Newsletter & Contact) using **Formspree** (Endpoint: `https://formspree.io/f/mbddjdyg`).
    - Added AJAX form handling in `app.js` to prevent page reloads.
- **Visual Design & FX:**
    - Implemented **SVG Glitch Filters** for hover states (buttons/links) and a subtle **Scroll Glitch** animation.
    - Standardized internal image paths (removed leading slashes) to fix local preview/loading issues.
    - Updated **Portfolio Grid** layout and reordered the "Broboticus" series (Avatar is now 2nd).
- **SEO & Content:**
    - Enriched `gallery.json` with AI-generated descriptions and alt text using **Z.AI GLM-4.6v-flash**.
    - Updated metadata, `sitemap.xml`, and `alt` attributes across the site.
    - Corrected "Pup Fiction" descriptions to clarify it is a parody series.
- **Infrastructure:**
    - Refactored `robot.js` to use `IntersectionObserver`.
    - Added `thumbnail_generator.py` script for Krita.
    - Secured API keys using `.env` and `.gitignore`.

## 8. Recovery Session Updates (2026-02-08)
- **Lead Gen & Value Delivery:**
    - **Instant Bundle:** Created `download-wallpapers.html` featuring 4K+ exclusive assets (`sangre_de_cristo_midnight_v2`, `marilyn_monbroe`, `the_screambot`).
    - **Automated Hand-off:** Updated `app.js` to automatically redirect users to the download portal after Formspree signup (2s delay).
    - **Cache Busting:** Implemented `?v=1.1` script versioning in `index.html` to force deployment updates.
- **Krita Toolkit (Quantum Engineering):**
    - **Auto-Load Solved:** Created `kritapykrita_BasicGlitch_toolkit.desktop` and refactored `__init__.py` to ensure the plugin loads permanently in Krita's "Scripts" menu.
    - **Unified Toolbelt:** Consolidated all 20+ scripts into `BasicGlitch_toolkit/tools/` with a dynamic, self-healing registration engine.
    - **Functional Repairs:** Upgraded complex tools (`Neural Style Transfer Bridge`, `Temporal Undo`, `RGB Glitch`, `CRT Scanlines`) for Krita 5.2/Windows compatibility.
    - **Apparel Expansion:** Upgraded `master_apparel.py` with centered, DPI-aware templates for tapestries, backpacks, duffel bags, tote bags, socks, and beanies.
- **Infrastructure & Pipeline:**
    - **One-Click Sync:** Developed `distribute_toolkit.sh` (Linux) and `Install_System.bat` (Windows) to synchronize the production pipeline across partitions via the shared folder.
    - **Documentation:** Authored a comprehensive `README.md` for the Krita toolkit detailing usage and effects.
        - **System Hardening:** Identified and resolved "silent crash" bugs caused by redundant `__init__.py` files in the root `pykrita` directory.
## 9. Full-Spectrum Automation (2026-02-13)
- **Neural Forge (AI Integration):**
    - Created `forge.html` featuring a terminal-style UI for user-driven image generation.
    - Integrated `visualForgeFlow` into the Genkit Server (Port 3400) using Gemini-Flash.
    - Added `runNeuralForge` to `app.js` for seamless frontend-to-backend communication.
- **V3 Ingestion Engine Upgrade:**
    - **Technical Polish:** Implemented automated WebP conversion in `ingest_art.py`, reducing image size by ~70% for SEO performance.
    - **Market Readiness:** Added automated POD metadata generation. The system now creates `pod_market_master.csv` with optimized titles, tags, and descriptions for bulk uploads.
    - **Deep Lore ARG:** Integrated a hidden Forensic Terminal (`terminal.js`). Gemini now occasionally hides "Forensic Fragments" in the 300-word art analyses to trigger ARG rewards.
- **POD Pipeline:**
    - Developed `pod_signup_assistant.py` to automate tedious account creation data entry.
    - Developed `pod_upload_assistant.py` for "Metadata Injection," allowing rapid listing across Redbubble, TeePublic, and Society6.
- **Navigation:** Unified "Neural Forge" access across all 13 site pages.
    