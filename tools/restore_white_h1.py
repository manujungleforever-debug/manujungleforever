import os
import re

root_dir = 'www.manujungleforever.com'
target_style = "color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;"

tag_pattern = re.compile(r'<h1(\s+[^>]*)?>', re.IGNORECASE)
style_attr_pattern = re.compile(r'style=[\"\'\']([^\"\'\']*)[\"\'\']', re.IGNORECASE)

modified_files = []

for root, _, files in os.walk(root_dir):
    if 'admin' in root.split(os.sep):
        continue
        
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                original_content = content
                
                def repl(match):
                    attrs = match.group(1) or ''
                    
                    if 'style=' in attrs:
                        def style_repl(s_match):
                            style_content = s_match.group(1)
                            # Remove any existing color or text-shadow
                            style_content = re.sub(r'color\s*:[^;]+;?', '', style_content, flags=re.IGNORECASE)
                            style_content = re.sub(r'-webkit-text-fill-color\s*:[^;]+;?', '', style_content, flags=re.IGNORECASE)
                            style_content = re.sub(r'text-shadow\s*:[^;]+;?', '', style_content, flags=re.IGNORECASE)
                            
                            new_style = style_content.strip()
                            if new_style and not new_style.endswith(';'):
                                new_style += ';'
                            
                            return f'style="{new_style} {target_style}"'
                        
                        attrs = style_attr_pattern.sub(style_repl, attrs)
                    else:
                        attrs = f' style="{target_style}"{attrs}'
                        
                    return f'<h1{attrs}>'
                        
                new_content = tag_pattern.sub(repl, content)
                
                if new_content != original_content:
                    with open(path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_content)
                    modified_files.append(path)
            except Exception as e:
                print(f'Error on {path}: {e}')

print(f'Restored bright white on H1 across {len(modified_files)} files.')
