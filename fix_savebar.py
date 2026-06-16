import os
import re

path = 'www.hiddenjunglecusco.com/admin/index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add `.save-bar { left: 0; padding: 10px 16px; justify-content: center; }` inside `@media (max-width: 768px) { ... }`
# Let's find `.lcard { padding: 32px 20px; border-radius: 12px; }` which is near the end of the media query and inject it after that.

media_query_fix = """            .lcard { padding: 32px 20px; border-radius: 12px; }
            .save-bar { left: 0; padding: 12px 16px; justify-content: center; width: 100%; box-sizing: border-box; flex-wrap: wrap; }
"""

if '.save-bar { left: 0;' not in content:
    content = content.replace('.lcard { padding: 32px 20px; border-radius: 12px; }', media_query_fix)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed save-bar responsive CSS!")
else:
    print("Already fixed.")
