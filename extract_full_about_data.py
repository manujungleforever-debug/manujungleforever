import bs4

soup = bs4.BeautifulSoup(open('scratch_about_structure.html', 'r', encoding='utf-8').read(), 'html.parser')

sections = []
current_section = None

# We can parse the document by scanning all the widget containers in elementor.
# Elementor divides content into sections, columns, and widgets.
# Let's iterate over elementor-section elements

all_sections = soup.select('.elementor-section')
print(f"Total elementor sections: {len(all_sections)}")

# We can also just pull out each widget text-editor and image to see their order
with open('scratch_extracted_clean_elements.txt', 'w', encoding='utf-8') as f:
    for idx, sec in enumerate(all_sections):
        # We only care about sections inside elementor-31
        # Let's see if this is a top-level section
        if 'elementor-top-section' in sec.get('class', []):
            f.write(f"\n\n=== SECTION {idx} ===\n")
            
            # Find all headings in this section
            headings = [h.text.strip() for h in sec.find_all(['h1', 'h2', 'h3', 'h4'])]
            f.write(f"HEADINGS: {headings}\n")
            
            # Find all text editors
            editors = sec.select('.elementor-widget-text-editor .elementor-widget-container')
            for ed in editors:
                f.write(f"--- TEXT EDITOR ---\n{ed.decode_contents().strip()}\n")
                
            # Find all images
            imgs = sec.select('.elementor-widget-image img')
            for img in imgs:
                f.write(f"--- IMAGE ---\nSRC: {img.get('src')}\nALT: {img.get('alt')}\n")

print("Clean elements saved.")
