import zipfile
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/about-2/')
soup = BeautifulSoup(html, 'html.parser')

for el in soup.find_all(string=True):
    if 'WHAT MAKES US UNIQUE' in el.upper():
        print(el.parent.parent.prettify()[:2000])
