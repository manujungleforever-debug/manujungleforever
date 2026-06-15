import re

target_href = 'index.html'
pattern = rf'<a\s[^>]*href="(?:(?:\.\.\/)+|(?:\.\/)?){re.escape(target_href)}"[^>]*>'

test_strings = [
    '<a href="index.html">',
    '<a href="./index.html">',
    '<a href="../index.html">',
    '<a href="../../index.html">',
    '<a href="guided-tours/index.html">', # SHOULD FAIL
    '<a href="../guided-tours/index.html">', # SHOULD FAIL
]

print(f"Target href: {target_href}")
for s in test_strings:
    match = re.search(pattern, s)
    if match:
        print(f"MATCH: {s}")
    else:
        print(f"FAIL:  {s}")

print("---")
target_href2 = 'about-2/index.html'
pattern2 = rf'<a\s[^>]*href="(?:(?:\.\.\/)+|(?:\.\/)?){re.escape(target_href2)}"[^>]*>'
test_strings2 = [
    '<a href="about-2/index.html">',
    '<a href="../about-2/index.html">',
    '<a href="../../about-2/index.html">',
]
print(f"Target href: {target_href2}")
for s in test_strings2:
    match = re.search(pattern2, s)
    if match:
        print(f"MATCH: {s}")
    else:
        print(f"FAIL:  {s}")

