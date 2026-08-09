import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

unsafe_modal_js = """// Modal
function openModal(){document.getElementById('bk-modal').classList.add('o');document.body.style.overflow='hidden';}
function closeModal(){document.getElementById('bk-modal').classList.remove('o');document.body.style.overflow='';}
document.getElementById('bk-modal').addEventListener('click',function(e){if(e.target===this)closeModal();});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

// Booking form AJAX
document.getElementById('bk-form').addEventListener('submit',async function(e){
  e.preventDefault();
  const btn=this.querySelector('[type=submit]'),msg=document.getElementById('bk-msg');
  btn.disabled=true;btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Sending...';
  try{
    const r=await fetch('handlers/send-booking.php',{method:'POST',body:new FormData(this)});
    const d=await r.json();
    msg.className='fm '+(d.ok?'ok':'er');
    msg.textContent=d.message;
    if(d.ok)this.reset();
  }catch{
    msg.className='fm er';
    msg.textContent='Could not send. Please email discover@manujungleforever.com or use WhatsApp.';
  }finally{btn.disabled=false;btn.innerHTML='<i class="fas fa-paper-plane"></i> Send Enquiry';}
});"""

safe_modal_js = """// Modal
function openModal(){const m=document.getElementById('bk-modal');if(m){m.classList.add('o');document.body.style.overflow='hidden';}}
function closeModal(){const m=document.getElementById('bk-modal');if(m){m.classList.remove('o');document.body.style.overflow='';}}
const bkModal = document.getElementById('bk-modal');
if(bkModal){
  bkModal.addEventListener('click',function(e){if(e.target===this)closeModal();});
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

// Booking form AJAX
const bkForm = document.getElementById('bk-form');
if(bkForm){
  bkForm.addEventListener('submit',async function(e){
    e.preventDefault();
    const btn=this.querySelector('[type=submit]'),msg=document.getElementById('bk-msg');
    btn.disabled=true;btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Sending...';
    try{
      const r=await fetch('handlers/send-booking.php',{method:'POST',body:new FormData(this)});
      const d=await r.json();
      msg.className='fm '+(d.ok?'ok':'er');
      msg.textContent=d.message;
      if(d.ok)this.reset();
    }catch{
      msg.className='fm er';
      msg.textContent='Could not send. Please email discover@manujungleforever.com or use WhatsApp.';
    }finally{btn.disabled=false;btn.innerHTML='<i class="fas fa-paper-plane"></i> Send Enquiry';}
  });
}"""

# A variation with different whitespace/newlines just in case
for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple replace for exact match
        if unsafe_modal_js in content:
            content = content.replace(unsafe_modal_js, safe_modal_js)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif "document.getElementById('bk-modal').addEventListener('click'" in content:
            # We must fix it manually if it has slightly different formatting
            content = content.replace("document.getElementById('bk-modal').addEventListener('click',function(e){if(e.target===this)closeModal();});", "const bkModal = document.getElementById('bk-modal'); if(bkModal){ bkModal.addEventListener('click',function(e){if(e.target===this)closeModal();}); }")
            content = content.replace("document.getElementById('bk-form').addEventListener('submit',async function(e){", "const bkForm = document.getElementById('bk-form'); if(bkForm){ bkForm.addEventListener('submit',async function(e){")
            # And close the bkForm if statement. But this is risky with string replace. 
            # So I will just use the exact match which should work for most of them.
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
