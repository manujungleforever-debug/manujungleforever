import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')

for key in ['https://www.hiddenjunglecusco.com/', 'https://www.hiddenjunglecusco.com/home/']:
    try:
        html = z.read(key)
        soup = BeautifulSoup(html, 'html.parser')
        main_el = soup.select_one('.elementor')
        print(f"Key: {key}")
        print(f"  Size: {len(html)}")
        print(f"  Title: {soup.find('title')}")
        print(f"  Has elementor: {main_el is not None}")
        if main_el:
            print(f"  Elementor class: {main_el.get('class')}")
            print(f"  Text length: {len(main_el.text)}")
            # Search for unique
            print(f"  Has 'unique': {'unique' in main_el.text.lower()}")
    except KeyError:
        print(f"Key {key} not found")
