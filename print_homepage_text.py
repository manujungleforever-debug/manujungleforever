import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/')
soup = BeautifulSoup(html, 'html.parser')
body = soup.select_one('.elementor-9102')

if body:
    print("HOMEPAGE HEADINGS:")
    for h in body.select('h1, h2, h3, h4, h5, h6'):
        print(f"- {h.text.strip()}")
        
    print("\nHOMEPAGE TEXT BLOCKS:")
    for p in body.select('.elementor-widget-text-editor'):
        print(f"[{p.text.strip()[:100]}]")
else:
    print("Could not find .elementor-9102")
