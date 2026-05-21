from bs4 import BeautifulSoup
import json

with open(r'C:\Users\evera\.gemini\antigravity-ide\brain\ce1bc295-01f6-41a1-8e0a-c23dd2cd24e3\.system_generated\steps\543\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
main_el = soup.find('div', class_='elementor-31')

sections = main_el.find_all('section', recursive=False)
for idx, sec in enumerate(sections):
    print(f"--- SECTION {idx} (ID: {sec.get('data-id')}) ---")
    
    # Let's inspect sub-sections or columns
    columns = sec.find_all('div', class_='elementor-column', recursive=False)
    # If no immediate columns, check nested ones or just print widgets
    widgets = sec.find_all('div', class_=lambda c: c and 'elementor-widget' in c)
    for w in widgets:
        w_classes = w.get('class', [])
        w_type = [c.replace('elementor-widget-', '') for c in w_classes if c.startswith('elementor-widget-')]
        w_type = w_type[0].split('--')[0] if w_type else 'unknown'
        
        print(f"  Widget Type: {w_type}")
        if w_type == 'heading':
            print("    Heading:", w.text.strip())
        elif w_type == 'text-editor':
            print("    Text Editor (first 100 chars):", w.text.strip()[:150])
        elif w_type == 'image':
            img = w.find('img')
            if img:
                print("    Image:", img.get('src'))
        elif w_type == 'gallery':
            imgs = [i.get('src') for i in w.find_all('img')]
            print("    Gallery Images:", len(imgs))
