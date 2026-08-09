import os, glob, re

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

# Regex to capture the Libro block
libro_regex = re.compile(r'(\s*<!-- Libro de reclamaciones -->\s*<a href=".*?libro-de-reclamaciones/index\.html".*?</a>\s*)', re.DOTALL)

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<footer class="ft">' not in content:
            continue

        # 1. Update .fa style
        old_fa = r".fa { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 800; letter-spacing: 0.05em; line-height: 1.6; color: #ffffff; text-transform: uppercase; margin-bottom: 25px; margin-top: 15px; display: block; }"
        new_fa = r".fa { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 300; letter-spacing: 0; line-height: 1.6; color: rgba(255,255,255,0.7); text-transform: uppercase; margin-bottom: 25px; margin-top: 15px; display: block; }"
        if old_fa in content:
            content = content.replace(old_fa, new_fa)

        # 2. Update Grid
        grid_old = r'grid-template-columns: 1.8fr 1fr 1.2fr 1.5fr;'
        grid_new = r'grid-template-columns: 1.8fr 1fr 1.2fr 1.3fr 1.2fr;'
        content = content.replace(grid_old, grid_new)
        
        # 3. Extract Libro block
        m = libro_regex.search(content)
        if m:
            libro_block = m.group(1)
            # Remove from original place
            content = content.replace(libro_block, '\n')
            
            # Reconstruct the links correctly taking into account nested paths (using the href from Explore Home to determine depth)
            # Find the path prefix by looking at Home link in footer
            depth_match = re.search(r'<li><a href="([^"]*)index\.html"><i class="fas fa-arrow-right"></i> Home</a></li>', content)
            prefix = depth_match.group(1) if depth_match else ''
            
            # The libro block already has correct paths, we just insert the Legal column
            legal_col = f"""
    <!-- COLUMN 5: Legal & Support -->
    <div class="f-col">
      <h3>Legal &amp; Support</h3>
      <ul style="margin-bottom: 20px;">
        <li><a href="{prefix}terms-and-conditions/index.html"><i class="fas fa-arrow-right"></i> Terms &amp; Conditions</a></li>
        <li><a href="{prefix}privacy-policy/index.html"><i class="fas fa-arrow-right"></i> Privacy Policy</a></li>
        <li><a href="{prefix}cookies-policy/index.html"><i class="fas fa-arrow-right"></i> Cookies Policy</a></li>
        <li><a href="{prefix}faq/index.html"><i class="fas fa-arrow-right"></i> FAQ</a></li>
      </ul>
{libro_block.rstrip()}
    </div>
"""
            # Insert before the last two closing divs of the footer
            # They look like:
            #   </div>
            # </div>
            # </footer>
            
            footer_end = r"  </div>\s*</div>\s*</footer>"
            def replacer(match):
                return legal_col + match.group(0)
            
            content = re.sub(footer_end, replacer, content, count=1)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error {fpath}: {e}")
print("Done.")
