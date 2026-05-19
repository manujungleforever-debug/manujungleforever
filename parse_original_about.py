import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/about-2/')
soup = BeautifulSoup(html, 'html.parser')

main_content = soup.select_one('.elementor-31')
if not main_content:
    print("Could not find elementor-31!")
    main_content = soup.select_one('article')

with open('scratch_about_structure.html', 'w', encoding='utf-8') as f:
    f.write(main_content.prettify() if main_content else soup.body.prettify())

print("Saved structures to scratch_about_structure.html")
