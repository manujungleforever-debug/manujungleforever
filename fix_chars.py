import os
ROOT = 'www.hiddenjunglecusco.com'

def fix_file(fpath):
    with open(fpath, 'rb') as f:
        content = f.read()
    
    # Check if the replacement character is present
    replacement_char = b'\xef\xbf\xbd'
    if replacement_char in content:
        # Replace with en-dash (hyphen-like)
        new_content = content.replace(replacement_char, b'\xe2\x80\x93')
        
        # Write back
        with open(fpath, 'wb') as f:
            f.write(new_content)
        return True
    return False

fixed = 0
for dirpath, dirs, files in os.walk(ROOT):
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(dirpath, fname)
            if fix_file(fpath):
                fixed += 1

print(f"Fixed {fixed} files.")
