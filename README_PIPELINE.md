# BASICGLITCH.ART | Automated Production Pipeline
**Status:** FULLY OPERATIONAL (Win and Keep Winning)

This document outlines the zero-labor workflow for moving artwork from **Krita (Windows)** to **Cloudflare (Live Site)**.

---

## 1. Setup (One-Time / Every Session)
To ensure the pipeline is "listening" for your signals, you must have the **Foundry Watcher** running in your Linux terminal.

1. Open your Linux terminal.
2. Navigate to the project root: `cd ~/monetization`
3. Start the watcher:
   ```bash
   ./basic-glitch-art/scripts/watch_foundry.sh
   ```
*Leave this terminal window open while you work.*

---

## 2. Creating New Art (Krita Workflow)
When you finish a piece in Krita on your Windows partition:

1. Go to **Tools -> Scripts -> Scripter**.
2. Load or paste the `foundry_exporter.py` script.
3. Click **Run**.
4. **What happens:**
   - A high-res PNG is saved to the shared drive.
   - A web-optimized version is created.
   - A thumbnail is generated.
   - A message box in Krita will confirm: "Foundry Export Complete!"

---

## 3. Ingesting Existing Art (Bulk Upload)
If you have art in other folders on your computer that you want on the site:

1. Simply **Copy/Paste** the image files (.png, .jpg, or .jpeg) into:
   `C:\sf_minty_windows\foundry_transferaw`
2. **What happens:**
   - Within 30 seconds, the Linux Watcher will "see" the files.
   - It will trigger the Ingestion Engine automatically.

---

## 4. The Automated Engine (Under the Hood)
The moment a file hits the ingestion folder, the following chain reaction occurs:

1. **AI Analysis:** Gemini 2.0/1.5 scans the image and writes a **300-word Forensic Analysis**.
2. **Database Update:** The piece is added to the top of `assets/data/gallery.json`.
3. **SEO Page Generation:** A dedicated HTML page is built at `/art/[title].html`.
4. **Sitemap Update:** `sitemap.xml` is refreshed to tell Google about the new content.
5. **Mainframe Sync:** The code is automatically committed and pushed to GitHub.
6. **Live Deployment:** Cloudflare detects the push and deploys the update.

---

## 5. Verification
To see your work live:
1. Wait approx. 2-3 minutes for the Cloudflare build to finish.
2. Visit `https://basicglitch.art/gallery.html`.
3. Your new piece will be at the top. Click it to see its unique SEO page and 300-word analysis.

---

## Troubleshooting
- **Watcher not detecting:** Ensure the path `/media/sf_minty_windows/foundry_transfer/raw` is accessible in Linux.
- **Quota Errors:** If the 300-word analysis fails due to API limits, the script will insert a placeholder and retry on the next run.
- **Git Push Fails:** Check your internet connection or GitHub PAT status.
