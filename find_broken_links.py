import os
import re
from pathlib import Path
from urllib.parse import urlparse, unquote

root_dir = Path('g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com').resolve()

broken_links = []

for root, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = Path(root) / file
            try:
                content = filepath.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = filepath.read_text(encoding='latin-1')
            
            # Find href attributes
            links = re.findall(r'href=[\"\'](.*?)[\"\']', content)
            
            for link in links:
                # ignore external links or anchor links or tel/mailto
                if link.startswith(('http', 'https', 'mailto:', 'tel:', '#')):
                    continue
                    
                parsed = urlparse(link)
                path = unquote(parsed.path)
                
                if not path:
                    continue
                    
                # Resolve relative path
                if path.startswith('/'):
                    target = root_dir / path.lstrip('/')
                else:
                    target = (filepath.parent / path).resolve()
                
                # Check if target exists
                if not target.exists():
                    broken_links.append((str(filepath.relative_to(root_dir)), link))

for file, link in set(broken_links):
    print(f'Broken link in {file}: {link}')
