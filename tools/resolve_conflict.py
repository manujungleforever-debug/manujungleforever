import re

fp = 'www.manujungleforever.com/index.html'
with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

conflict_pattern = re.compile(r'<<<<<<< HEAD.*?=======\s*(.*?)\s*>>>>>>> [a-f0-9]+ .*?\n', re.DOTALL)

def repl(m):
    return m.group(1) + '\n'

new_text = conflict_pattern.sub(repl, text)

# Fix mojibake
new_text = new_text.replace('Cusco, Peru  Manu', 'Cusco, Peru · Manu')
new_text = new_text.replace('Cusco ?\" guided', 'Cusco — guided')
new_text = new_text.replace('Cusco ?" guided', 'Cusco — guided')
new_text = new_text.replace('Local. \nWild. Authentic.', 'Local. Wild. Authentic.')

with open(fp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_text)
