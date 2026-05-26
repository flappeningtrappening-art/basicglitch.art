import json
import os
import re

def slugify(text):
    text = text.lower()
    text = text.replace(' — ', '-')
    text = text.replace(' - ', '-')
    text = text.replace(' —', '-')
    text = text.replace('— ', '-')
    text = text.replace('—', '-')
    text = text.replace(' / ', '-')
    text = text.replace(' /', '-')
    text = text.replace('/ ', '-')
    text = text.replace('/', '-')
    text = re.sub(r'[^a-z0-9\-]', '', text.replace(' ', '-'))
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def main():
    with open('assets/data/gallery.json', 'r') as f:
        gallery = json.load(f)

    # Create mapping of slugs to gallery items
    gallery_map = {}
    for item in gallery:
        slug = slugify(item['title'])
        gallery_map[slug] = item
        # Also try without some specific replacements if needed
        # But slugify should be robust enough

    art_dir = 'art'
    updated_files = []

    nav_html = """    <nav class="nav">
      <a class="nav-link" href="../gallery.html"><img src="../assets/icons/gallery.svg" alt="Gallery Icon"> Gallery</a>
      <a class="nav-link" href="../portfolio.html"><img src="../assets/icons/grid.svg" alt="Portfolio Icon"> Portfolio</a>
      <a class="nav-link" href="../broboticus.html"><img src="../assets/icons/about.svg" alt="Broboticus Icon"> Broboticus</a>
      <a class="nav-link" href="../commissions.html"><img src="../assets/icons/commissions.svg" alt="Commissions Icon"> Commissions</a>
      <a class="nav-link" href="../apparel.html"><img src="../assets/icons/physical-products.svg" alt="Apparel Icon"> Apparel</a>
      <a class="nav-link" href="../about.html"><img src="../assets/icons/about.svg" alt="About Icon"> About</a>
      <a class="nav-link" href="../contact.html"><img src="../assets/icons/contact.svg" alt="Contact Icon"> Contact</a>
    </nav>"""

    for filename in os.listdir(art_dir):
        if not filename.endswith('.html'):
            continue
        
        file_path = os.path.join(art_dir, filename)
        slug = filename[:-5] # remove .html
        
        item = gallery_map.get(slug)
        
        # Fallback: try to find by reading the file and getting the title
        if not item:
            with open(file_path, 'r') as f:
                content = f.read()
                title_match = re.search(r'<title>(.*?) \|', content)
                if title_match:
                    found_title = title_match.group(1).replace(' —', ' —') # normalize
                    for it in gallery:
                        if it['title'] == found_title or slugify(it['title']) == slug:
                            item = it
                            break

        if not item:
            # Special case for some files that might have different naming
            if slug == 'broboticus-the-original-march-of-the-robots-2024':
                for it in gallery:
                    if 'March of the Robots, 2024' in it['title']:
                        item = it
                        break
            if slug == 'sangre-de-cristos-night':
                for it in gallery:
                    if it['title'] == 'Sangre De Cristos — Night':
                        item = it
                        break
            if slug == 'sangre-de-cristos-neon':
                for it in gallery:
                    if it['title'] == 'Sangre De Cristos — Neon':
                        item = it
                        break

        if item:
            with open(file_path, 'r') as f:
                content = f.read()

            # RULE 6: Page Title
            new_title = f"{item['title']} | BasicGlitch"
            content = re.sub(r'<title>.*?</title>', f"<title>{new_title}</title>", content)

            # RULE 7: Meta Description
            meta_desc = item['description'][:160]
            content = re.sub(r'<meta name="description" content=".*?"', f'<meta name="description" content="{meta_desc}"', content)
            content = re.sub(r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{meta_desc}"', content)

            # RULE 3: Nav Links
            content = re.sub(r'<nav class="nav">.*?</nav>', nav_html, content, flags=re.DOTALL)

            # RULE 5: Alt Text
            alt_text = item['alt_text']
            content = re.sub(r'<img (.*?)alt=".*?"', f'<img \\1alt="{alt_text}"', content)

            # RULE 1/2: Description Field
            # Populate the forensic-description div
            # Find the div and replace its content
            desc_pattern = re.compile(r'(<div class="forensic-description".*?>).*?(</div>)', re.DOTALL)
            content = desc_pattern.sub(f'\\1\n            {item["description"]}\n        \\2', content)

            # RULE 4: Series/Collection
            categories = " · ".join(item['categories'])
            content = re.sub(r'COLLECTION:.*?</p>', f'COLLECTION: {categories.upper()}</p>', content)

            # Update <h1> title
            content = re.sub(r'<span class="cyber-text" data-text=".*?">(.*?)</span>', 
                             f'<span class="cyber-text" data-text="{item["title"].upper()}">{item["title"].upper()}</span>', 
                             content)

            # Update SEND INQUIRY link
            content = re.sub(r'href="\.\./contact\.html\?subject=Inquiry:.*?"', 
                             f'href="../contact.html?subject=Inquiry: {item["title"]}"', 
                             content)

            with open(file_path, 'w') as f:
                f.write(content)
            
            updated_files.append(filename)
        else:
            print(f"Skipping {filename}: No matching entry in gallery.json")

    print(f"\nTotal files updated: {len(updated_files)}")
    for f in sorted(updated_files):
        print(f)

if __name__ == "__main__":
    main()
