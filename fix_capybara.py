# -*- coding: utf-8 -*-
# Fix: replace llama emoji with beaver emoji in Capybaras card

path = 'www.hiddenjunglecusco.com/index.html'

llama   = '\U0001F999'   # 🦙 llama (wrong)
beaver  = '\U0001F9AB'   # 🦫 beaver (closest to capybara - large semi-aquatic rodent)

content = open(path, 'r', encoding='utf-8').read()

target = llama + '</div><p>Capybaras</p>'
replacement = beaver + '</div><p>Capybaras</p>'

count = content.count(target)
print(f'Occurrences to replace: {count}')

if count == 1:
    new_content = content.replace(target, replacement)
    open(path, 'w', encoding='utf-8').write(new_content)
    print('SUCCESS: Capybaras icon updated from llama to beaver emoji')
else:
    # Try variant without closing div
    target2 = llama + '\u003c/div\u003e\u003cp\u003eCapybaras\u003c/p\u003e'
    count2 = content.count(target2)
    print(f'Variant count: {count2}')
    print('ERROR: unexpected count, manual check needed')
    # show context
    idx = content.find(llama)
    if idx != -1:
        print('Context:', repr(content[idx:idx+50]))
