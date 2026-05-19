import sys
from bs4 import BeautifulSoup

with open("temp_dl.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("--- H1 ---")
h1 = soup.find('h1')
print(h1.text.strip() if h1 else "No H1")

print("\n--- TEXT EDITORS ---")
editors = soup.select(".elementor-widget-text-editor .elementor-widget-container")
for e in editors:
    print(e.decode_contents().strip()[:100] + "...")

print("\n--- ACCORDIONS ---")
accordions = soup.select(".elementor-accordion-item")
for acc in accordions[:2]:
    title = acc.select_one(".elementor-accordion-title")
    content = acc.select_one(".elementor-tab-content")
    print("Title:", title.text.strip() if title else "")
    print("Content:", content.decode_contents().strip()[:100] + "...")

