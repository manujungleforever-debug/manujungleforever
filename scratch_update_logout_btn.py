import os
import codecs
import glob
import re

admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

new_btn_logout_css = '''
.btn-logout { 
    background: linear-gradient(135deg, #ef4444, #b91c1c); 
    color: #fff; 
    border: none;
    cursor: pointer; 
    font-size: .85rem; 
    font-weight: 700; 
    padding: 8px 16px; 
    border-radius: 10px; 
    transition: .3s; 
    display: flex; 
    align-items: center; 
    gap: 8px; 
    box-shadow: 0 4px 15px rgba(239,68,68,0.35);
}
.btn-logout:hover { 
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(239,68,68,0.5);
    filter: brightness(1.1);
}
'''

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Clean up inline styles for btn-logout in panel.html
    content = re.sub(r'class="btn-logout" style="[^"]+"', 'class="btn-logout"', content)
    
    # Replace existing .btn-logout CSS in subpages
    content = re.sub(r'\.btn-logout\s*\{[^}]+\}', '', content)
    content = re.sub(r'\.btn-logout:hover\s*\{[^}]+\}', '', content)
    
    # Inject new CSS before </style>
    content = content.replace('</style>', new_btn_logout_css + '\n</style>')
        
    if content != original_content:
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Updated btn-logout in {os.path.basename(filepath)}")

