import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
legacy_html = z.read('https://www.hiddenjunglecusco.com/')
legacy_soup = BeautifulSoup(legacy_html, 'html.parser')

print("Searching for 'unique' in legacy homepage...")
matches = []
for el in legacy_soup.find_all(text=True):
    if 'unique' in el.lower():
        matches.append((el.parent.name, el.strip()))

for m in matches[:10]:
    print(m)
