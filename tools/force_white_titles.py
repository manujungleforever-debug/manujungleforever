import os
import re

root_dir = 'www.manujungleforever.com'

tag_pattern = re.compile(r'<(h1|h2)(\s+[^>]*)?>', re.IGNORECASE)
style_attr_pattern = re.compile(r'style=[\"\'\']([^\"\'\']*)[\"\'\']', re.IGNORECASE)

modified_files = []
target_style = "color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;"

for root, _, files in os.walk(root_dir):
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
                    
                    if 'style=' in attrs:
                        def style_repl(s_match):
                            style_content = s_match.group(1)
                            # Remove old color and text-fill-color
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
