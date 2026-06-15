import os, re

count = 0
for d, _, fs in os.walk('www.hiddenjunglecusco.com'):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(d, f)
            with open(p, 'r', encoding='utf-8') as file:
                c = file.read()
            new_c = re.sub(r'assets/css/new\.css(?:\?v=\d+)?', 'assets/css/new.css?v=2', c)
            if new_c != c:
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(new_c)
                count += 1
print('Updated files:', count)
