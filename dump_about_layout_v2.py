from bs4 import BeautifulSoup
import re

with open(r'C:\Users\evera\.gemini\antigravity-ide\brain\ce1bc295-01f6-41a1-8e0a-c23dd2cd24e3\.system_generated\steps\543\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
main_el = soup.find('div', class_='elementor-31')

def clean_text(t):
    return t.strip().replace('\xa0', ' ').replace('', '')

def parse_element(el, indent=0):
    ind = "  " * indent
    if not el.name:
        return
        
    classes = el.get('class', [])
    
    # Check if this is a section
    if 'elementor-section' in classes:
        print(f"\n{ind}[SECTION ID: {el.get('data-id')}]")
        for child in el.find_all(True, recursive=False):
            parse_element(child, indent + 1)
            
    # Check if container
    elif 'elementor-container' in classes:
        for child in el.find_all(True, recursive=False):
            parse_element(child, indent)
            
    # Check if column
    elif 'elementor-column' in classes:
        col_width = ""
        for c in classes:
            if c.startswith('elementor-col-'):
                col_width = f" ({c.split('-')[-1]}%)"
        print(f"{ind}[COLUMN ID: {el.get('data-id')}{col_width}]")
        wrap = el.find('div', class_='elementor-widget-wrap')
        if wrap:
            for child in wrap.find_all(True, recursive=False):
                parse_element(child, indent + 1)
                
    # Check if widget
    elif 'elementor-widget' in classes:
        w_type = "unknown"
        for c in classes:
            if c.startswith('elementor-widget-'):
                w_type = c.replace('elementor-widget-', '').split('--')[0]
                break
        print(f"{ind}- [WIDGET: {w_type} (ID: {el.get('data-id')})]")
        
        if w_type == 'heading':
            tag = el.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            t = clean_text(tag.text if tag else el.text)
            print(f"{ind}    Heading: \"{t}\"")
        elif w_type == 'text-editor':
            t = clean_text(el.text)
            print(f"{ind}    Text: \"{t[:200]}...\"")
        elif w_type == 'image':
            img = el.find('img')
            if img:
                print(f"{ind}    Image URL: {img.get('src')}")
                print(f"{ind}    Image Alt: \"{img.get('alt')}\"")
        elif w_type == 'divider':
            print(f"{ind}    (Divider)")
        elif w_type == 'spacer':
            print(f"{ind}    (Spacer)")
            
    # Inner sections
    elif 'elementor-row' in classes or 'elementor-widget-wrap' in classes:
        for child in el.find_all(True, recursive=False):
            parse_element(child, indent)
    else:
        for child in el.find_all(True, recursive=False):
            parse_element(child, indent)

parse_element(main_el)
