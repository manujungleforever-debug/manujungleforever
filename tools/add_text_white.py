import os
import re

root_dir = 'www.manujungleforever.com'

tag_pattern = re.compile(r'<(h1|h2)(\s+[^>]*)?>', re.IGNORECASE)
class_pattern = re.compile(r'class=[\"\'\']([^\"\'\']*)[\"\'\']', re.IGNORECASE)
style_pattern = re.compile(r'style=[\"\'\']([^\"\'\']*)[\"\'\']', re.IGNORECASE)
color_remove_pattern = re.compile(r'color\s*:[^;]+;?', re.IGNORECASE)

modified_files = []

for root, _, files in os.walk(root_dir):
    # Skip admin folder
    if 'admin' in root.split(os.sep):
        continue
        
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'rb') as f:
                    raw = f.read()
                
                if raw.startswith(b'\xef\xbb\xbf'):
                    raw = raw[3:]
                
                content = raw.decode('utf-8')
                original_content = content
                
                def repl(match):
                    tag_name = match.group(1)
                    attrs = match.group(2) or ''
                    
                    # Ensure text-white class
                    if 'class=' in attrs:
                        def class_repl(c_match):
                            classes = c_match.group(1).split()
                            if 'text-white' not in classes:
                                classes.append('text-white')
                            return 'class="' + ' '.join(classes) + '"'
                        attrs = class_pattern.sub(class_repl, attrs)
                    else:
                        attrs = ' class="text-white"' + attrs
                        
                    # Remove color from inline style
                    if 'style=' in attrs:
                        def style_repl(s_match):
                            style_content = s_match.group(1)
                            new_style = color_remove_pattern.sub('', style_content).strip()
                            if new_style:
                                return 'style="' + new_style + '"'
                            return ''
                        attrs = style_pattern.sub(style_repl, attrs)
                        # Clean up empty style="" just in case
                        attrs = attrs.replace(' style=""', '')
                        
                    return f'<{tag_name}{attrs}>'
                        
                new_content = tag_pattern.sub(repl, content)
                
                if new_content != original_content:
                    with open(path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_content)
                    modified_files.append(path)
            except Exception as e:
                print(f'Error on {path}: {e}')

print(f'Modified {len(modified_files)} files.')
for m in modified_files:
    print(f' - {m}')
