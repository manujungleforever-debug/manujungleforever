import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/blog/')
soup = BeautifulSoup(html, 'html.parser')

posts = soup.find_all('article')
print(f"Total articles found in original blog: {len(posts)}")
for p in posts:
    title = p.find(['h2', 'h3'])
    if title:
        print(f" - {title.text.strip()}")
    else:
        print(" - (no title found in article tag)")
