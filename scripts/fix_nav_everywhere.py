import os
import re

def main():
    root_nav = """    <nav class="nav">
      <a class="nav-link" href="gallery.html"><img src="assets/icons/gallery.svg" alt="Gallery Icon"> Gallery</a>
      <a class="nav-link" href="portfolio.html"><img src="assets/icons/grid.svg" alt="Portfolio Icon"> Portfolio</a>
      <a class="nav-link" href="broboticus.html"><img src="assets/icons/about.svg" alt="Broboticus Icon"> Broboticus</a>
      <a class="nav-link" href="commissions.html"><img src="assets/icons/commissions.svg" alt="Commissions Icon"> Commissions</a>
      <a class="nav-link" href="apparel.html"><img src="assets/icons/physical-products.svg" alt="Apparel Icon"> Apparel</a>
      <a class="nav-link" href="about.html"><img src="assets/icons/about.svg" alt="About Icon"> About</a>
      <a class="nav-link" href="contact.html"><img src="assets/icons/contact.svg" alt="Contact Icon"> Contact</a>
    </nav>"""

    art_nav = """    <nav class="nav">
      <a class="nav-link" href="../gallery.html"><img src="../assets/icons/gallery.svg" alt="Gallery Icon"> Gallery</a>
      <a class="nav-link" href="../portfolio.html"><img src="../assets/icons/grid.svg" alt="Portfolio Icon"> Portfolio</a>
      <a class="nav-link" href="../broboticus.html"><img src="../assets/icons/about.svg" alt="Broboticus Icon"> Broboticus</a>
      <a class="nav-link" href="../commissions.html"><img src="../assets/icons/commissions.svg" alt="Commissions Icon"> Commissions</a>
      <a class="nav-link" href="../apparel.html"><img src="../assets/icons/physical-products.svg" alt="Apparel Icon"> Apparel</a>
      <a class="nav-link" href="../about.html"><img src="../assets/icons/about.svg" alt="About Icon"> About</a>
      <a class="nav-link" href="../contact.html"><img src="../assets/icons/contact.svg" alt="Contact Icon"> Contact</a>
    </nav>"""

    # Root files
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            with open(filename, 'r') as f:
                content = f.read()
            
            if '<nav class="nav">' in content:
                new_content = re.sub(r'<nav class="nav">.*?</nav>', root_nav, content, flags=re.DOTALL)
                with open(filename, 'w') as f:
                    f.write(new_content)
                print(f"Updated {filename}")

    # Art files
    art_dir = 'art'
    if os.path.exists(art_dir):
        for filename in os.listdir(art_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(art_dir, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if '<nav class="nav">' in content:
                    new_content = re.sub(r'<nav class="nav">.*?</nav>', art_nav, content, flags=re.DOTALL)
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    main()
