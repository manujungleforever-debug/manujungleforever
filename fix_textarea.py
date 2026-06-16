import os

path = 'www.hiddenjunglecusco.com/admin/index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_style = 'style="min-height:320px;font-family:monospace;font-size:.83rem;line-height:1.6;border:none;border-radius:0;background:rgba(255,255,255,.03);padding:12px"'
new_style = 'style="width:100%; box-sizing:border-box; resize:vertical; min-height:320px; font-family:monospace; font-size:.83rem; line-height:1.6; border:none; border-radius:0; background:rgba(255,255,255,.03); padding:12px"'

if old_style in content:
    content = content.replace(old_style, new_style)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed textarea width!")
else:
    print("Could not find the exact old style string.")
