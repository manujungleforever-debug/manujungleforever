from bs4 import BeautifulSoup

with open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
print("MODERN HOME HEADINGS:")
for h in soup.select('h1, h2, h3, h4, h5, h6'):
    print(f"- {h.text.strip()}")
