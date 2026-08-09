import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_js = """window.toggleAccordion = function(btn) {
  const content = btn.nextElementSibling;
  const isActive = btn.classList.contains('active');
  
  document.querySelectorAll('.itinerary-toggle').forEach(function(otherBtn) {
    otherBtn.classList.remove('active');
    if(otherBtn.nextElementSibling) {
       otherBtn.nextElementSibling.style.maxHeight = null;
    }
  });
  
  if (!isActive) {
    btn.classList.add('active');
    if(content) {
       content.style.maxHeight = content.scrollHeight + "px";
    }
  }
};"""

new_js = """window.toggleAccordion = function(btn) {
  const isActive = btn.classList.contains('active');
  
  document.querySelectorAll('.itinerary-toggle').forEach(function(otherBtn) {
    otherBtn.classList.remove('active');
    if(otherBtn.nextElementSibling) {
       otherBtn.nextElementSibling.style.maxHeight = null;
    }
  });
  
  if (!isActive) {
    btn.classList.add('active');
    // CSS max-height transition handles expansion
  }
};"""

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if old_js in content:
            content = content.replace(old_js, new_js)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
