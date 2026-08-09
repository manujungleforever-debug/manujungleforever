file_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\contact\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove Modal JS block that references bk-modal (which no longer exists on contact page)
old_js = """// Modal
  function openModal(){document.getElementById('bk-modal').classList.add('o');document.body.style.overflow='hidden';}
  function closeModal(){document.getElementById('bk-modal').classList.remove('o');document.body.style.overflow='';}
  document.getElementById('bk-modal').addEventListener('click',function(e){if(e.target===this)closeModal();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
  
  // Booking form AJAX
  document.getElementById('bk-form').addEventListener('submit',async function(e){
    e.preventDefault();
    const btn=this.querySelector('[type=submit]'),msg=document.getElementById('bk-msg');
    btn.disabled=true;btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Sending...';"""

new_js = """// Booking form - contact page uses its own inline form
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){}});
  
  // Contact form AJAX placeholder (handled by submitContact function)"""

if old_js in content:
    content = content.replace(old_js, new_js)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Removed bk-modal JS references.")
else:
    # Try partial match
    import re
    # Just remove the bk-form event listener block
    content = re.sub(
        r'// Modal\n  function openModal\(\).*?finally\{btn\.disabled=false;btn\.innerHTML=\'<i class="fas fa-paper-plane"><\/i> Send Enquiry\';\}\s*\}\);\s*',
        '// Contact page uses inline contact-form, no modal needed\n  ',
        content, flags=re.DOTALL
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Applied regex cleanup.")
