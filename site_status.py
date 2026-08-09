import os

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

print("=== ESTADO ACTUAL DEL SITIO ===\n")

checks = {
    "index.html": r"index.html",
    "about-2/index.html": r"about-2\index.html",
    "contact/index.html": r"contact\index.html",
    "guided-tours/index.html": r"guided-tours\index.html",
    "book-now/index.html": r"book-now\index.html",
}

for name, rel in checks.items():
    path = os.path.join(base_dir, rel)
    if not os.path.exists(path):
        print(f"  MISSING: {name}")
        continue
    c = open(path, encoding='utf-8').read()
    favicon = 'favicon.png' in c and 'favicon2' not in c
    wa_num = '51901525679' in c
    forms = c.count('<form ')
    has_filter_js = 'Tour Category Filter' in c if 'guided-tours' in rel else True
    jordy_first = c.index('Jordy') < c.index('Gloria') if 'about-2' in rel and 'Jordy' in c and 'Gloria' in c else True
    placida = 'Placida' not in c if 'about-2' in rel else True
    
    print(f"[{name}]")
    print(f"  favicon.png: {'OK' if favicon else 'BAD'}")
    print(f"  WA +51901525679: {'OK' if wa_num else 'BAD'}")
    print(f"  Forms count: {forms}")
    if 'guided-tours' in rel:
        print(f"  Filter JS: {'OK' if has_filter_js else 'MISSING'}")
    if 'about-2' in rel:
        print(f"  Jordy before Gloria: {'OK' if jordy_first else 'BAD'}")
        print(f"  Placida removed: {'OK' if placida else 'STILL THERE'}")
    print()
