import zipfile
from bs4 import BeautifulSoup
import re

def extract_about_us(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        html = z.read('https://www.hiddenjunglecusco.com/about-2/')
        soup = BeautifulSoup(html, 'html.parser')
        
        main_content = soup.find('main') or soup.find(id='content') or soup.body
        
        print("--- ABOUT US ORIGINAL TEXT AND IMAGES ---")
        for el in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img']):
            if el.name == 'img':
                print(f"IMG: {el.get('src', '')}")
            else:
                text = el.get_text(strip=True)
                if text:
                    print(f"{el.name.upper()}: {text}")

if __name__ == '__main__':
    extract_about_us('hts-cache/new.zip')
