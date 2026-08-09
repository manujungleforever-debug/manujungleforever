import os, re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

issues = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                c = f.read()
            forms = c.count('<form ')
            if forms > 1:
                issues.append((path, forms))

print("Pages with multiple forms:")
for path, count in sorted(issues):
    print(f"  {count} forms -> {path.replace(base_dir, '')}")

if not issues:
    print("  None! All pages have at most 1 form.")
