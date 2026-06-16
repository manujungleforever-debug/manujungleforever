import os
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time

translator = GoogleTranslator(source='en', target='es')
translation_cache = {}

def translate_text(text):
    text = text.strip()
    if not text or text.isnumeric() or len(text) <= 1:
        return text
    if text in translation_cache:
        return translation_cache[text]
    try:
        translated = translator.translate(text)
        translation_cache[text] = translated
        # small sleep to avoid rate limits
        time.sleep(0.05)
        return translated
    except Exception as e:
        return text

def adjust_paths(soup, rel_depth):
    # rel_depth is the number of directories deep the original file was.
    # We add one more '../' because it's now inside /es/
    prefix = '../'
    
    tags_attrs = {'a': 'href', 'img': 'src', 'link': 'href', 'script': 'src', 'form': 'action'}
    for tag_name, attr in tags_attrs.items():
        for tag in soup.find_all(tag_name):
            val = tag.get(attr)
            if val and not val.startswith(('http', 'https', 'mailto:', 'tel:', '#', '/', 'data:')):
                tag[attr] = prefix + val

def translate_all(base_dir):
    for root, dirs, files in os.walk(base_dir):
        # Skip the /es/ directory itself to avoid recursion
        if 'es' in dirs and root == base_dir:
            dirs.remove('es')
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                out_path = os.path.join(base_dir, 'es', rel_path)
                
                # depth = how many folders deep is the original file from base_dir
                # e.g., index.html -> 0
                # blog/index.html -> 1
                depth = len(rel_path.split(os.sep)) - 1
                
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                    
                soup = BeautifulSoup(html, 'html.parser')
                
                text_elements = [text for text in soup.find_all(string=True) if text.parent.name not in ['style', 'script', 'noscript', 'head', 'code']]
                
                count = 0
                for element in text_elements:
                    if element.strip():
                        translated = translate_text(element)
                        if translated and translated != element.strip():
                            element.replace_with(element.replace(element.strip(), translated))
                            count += 1
                            
                adjust_paths(soup, depth)
                
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                    
                print(f"Translated {rel_path} ({count} items)")

if __name__ == "__main__":
    base = 'www.hiddenjunglecusco.com'
    print("Starting translation of all 98 files... This will take a few minutes, but it's free!")
    translate_all(base)
    print("Translation complete!")
