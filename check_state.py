c = open(r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\guided-tours\index.html', encoding='utf-8').read()
print("Filter JS present:", 'Tour Category Filter' in c)
idx = c.find('rel="icon"')
print("Favicon line:", c[idx:idx+100])

c2 = open(r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\index.html', encoding='utf-8').read()
idx2 = c2.find('rel="icon"')
print("Root Favicon:", c2[idx2:idx2+100])

c3 = open(r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css', encoding='utf-8').read()
print("WA Wrap in CSS:", 'wa-wrap' in c3)
print("Translate fix in CSS:", 'goog-text-highlight' in c3)
print("Contact grid in CSS:", 'contact-grid' in c3)
