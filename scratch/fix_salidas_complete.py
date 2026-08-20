import subprocess, re

# Get the pristine version from HEAD~1
cmd = ['git', 'show', 'HEAD~1:www.manujungleforever.com/admin/gestionar-salidas.html']
content = subprocess.check_output(cmd).decode('utf-8')

# Replace the broken LOGO_B64 section with the robust logo loader
old_logo_pattern = r"// Logo hardcoded to bypass ALL loading and CORS issues forever\s+const LOGO_B64\s*=\s*'[^']+';\s+// Preload passenger photos"

new_logo_block = """// Logo institucional de Manu Jungle Forever
    let logoImg = document.querySelector('.logo-wrap img') || document.querySelector('.logo-brand img');
    if (!logoImg || !logoImg.complete || logoImg.naturalWidth === 0) {
      logoImg = await withTimeout(new Promise((resolve) => {
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        img.src = '../assets/img/logo.png';
        img.onload = () => resolve(img);
        img.onerror = () => resolve(null);
      }), 4000).catch(() => null);
    }

    // Preload passenger photos"""

if re.search(old_logo_pattern, content):
    content = re.sub(old_logo_pattern, new_logo_block, content)
    print("Replaced LOGO_B64 definition")
else:
    print("Pattern not found, checking direct replace...")

# Replace addImage call
content = content.replace(
    "doc.addImage('data:image/jpeg;base64,' + LOGO_B64, 'JPEG', 14, 10, 60, 30);",
    """if (logoImg) {
      try {
        doc.addImage(logoImg, 'PNG', 14, 8, 56, 24);
      } catch(e) {
        console.warn('Error adding logo to PDF:', e);
      }
    }"""
)

# Ensure thinking-orb is linked
if 'thinking-orb.css' not in content and '</head>' in content:
    content = content.replace('</head>', '  <link rel="stylesheet" href="css/thinking-orb.css">\n</head>')
if 'thinking-orb.js' not in content and '</body>' in content:
    content = content.replace('</body>', '  <script src="js/thinking-orb.js"></script>\n</body>')

with open('www.manujungleforever.com/admin/gestionar-salidas.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('admin/gestionar-salidas.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated files.")
