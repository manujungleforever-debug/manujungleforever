import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/3-day-wildlife-quest-machu-wasi/')
soup = BeautifulSoup(html, 'html.parser')

lists = soup.find_all(class_='elementor-icon-list-items')
for idx, ul in enumerate(lists):
    print(f"--- LIST {idx} ---")
    for li in ul.find_all('li'):
        icon = li.find('i')
        icon_class = icon.get('class') if icon else 'NO ICON'
        print(f"  - [{icon_class}] {li.text.strip().replace(chr(160), ' ')}")
