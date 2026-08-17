import re

filepath = 'g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com/admin/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of login-screen
# The login-screen div starts around line 604
# We will match from start of file up to `<!-- APP -->`
parts = content.split('<!-- APP -->')

if len(parts) > 1:
    clean_html = parts[0].strip() + '''

<script>
const API = '/api/cms';
let token = sessionStorage.getItem('cms_token');

// Redirect to panel if already logged in
if (token) {
    window.location.href = 'panel.html';
}

document.getElementById('inp-p').addEventListener('keydown', e => { if(e.key==='Enter') doLogin(); });
document.getElementById('btn-login').addEventListener('click', doLogin);

async function doLogin() {
    const u = document.getElementById('inp-u').value.trim();
    const p = document.getElementById('inp-p').value;
    const btn = document.getElementById('btn-login');
    const err = document.getElementById('login-err');
    btn.disabled=true; btn.textContent='Entrando...'; err.style.display='none';

    try {
      const r = await fetch(`${API}/login`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:u,pass:p})});
      const d = await r.json();
      if (!r.ok) throw new Error(d.error||'Credenciales incorrectas');
      
      sessionStorage.setItem('cms_token',d.token);
      sessionStorage.setItem('cms_user',u);
      
      // Check if there was a redirect param
      const params = new URLSearchParams(window.location.search);
      if (params.get('redirect')) {
          window.location.href = params.get('redirect');
      } else {
          window.location.href = 'panel.html';
      }
    } catch(e) {
      err.textContent = 'Credenciales incorrectas'; 
      err.style.display='block';
      btn.disabled=false; btn.textContent='Iniciar Sesión';
    }
}
</script>

<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
    const div = document.createElement("div");
    div.id = "tsparticles";
    div.style.position = "fixed"; div.style.inset = "0"; div.style.pointerEvents = "none"; div.style.zIndex = "998";
    document.body.appendChild(div);
    tsParticles.load("tsparticles", {
        fpsLimit: 60,
        particles: {
            number: { value: 35, density: { enable: true, area: 800 } },
            color: { value: ["#c9a84c", "#4aa18e", "#ffffff"] },
            shape: { type: "circle" },
            opacity: { value: 0.7, random: true, animation: { enable: true, speed: 0.5, minimumValue: 0.1, sync: false } },
            size: { value: 3, random: true, animation: { enable: true, speed: 1, minimumValue: 0.5, sync: false } },
            move: { enable: true, speed: 0.6, direction: "top", random: true, straight: false, outModes: { default: "out" } }
        },
        detectRetina: true
    });
});
</script>
</body>
</html>
'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    print("Fixed index.html!")
else:
    print("Could not find <!-- APP --> marker")
