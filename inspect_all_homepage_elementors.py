import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/')
soup = BeautifulSoup(html, 'html.parser')

print("All .elementor elements on the homepage:")
for el in soup.select('.elementor'):
    print(f"Class: {el.get('class')}, ID: {el.get('data-elementor-id')}")
    text = el.text.strip()
    print(f"  Text length: {len(text)}")
    print(f"  Has 'unique': {'unique' in text.lower()}")
    if 'unique' in text.lower():
        print(f"  Snippet: {text[:200]}...")
