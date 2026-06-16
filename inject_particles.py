import os

head_injection = """
<!-- HERO & PARTICLES FIX -->
<style>
.hero { position: relative; width: 100%; min-height: 80vh; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.hv { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; }
.hv video { width: 100%; height: 100%; object-fit: cover; object-position: center center; pointer-events: none; transform: scale(1.02); }
.ho { position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(3,8,5,0.3) 0%, rgba(3,8,5,0.85) 100%); z-index: 1; pointer-events: none; }
.hb { position: relative; z-index: 2; text-align: center; }
</style>
"""

body_injection = """
<!-- TSPARTICLES -->
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
            color: { value: ["#c9a84c", "#39ff6a", "#ffffff"] },
            shape: { type: "circle" },
            opacity: { value: 0.7, random: true, animation: { enable: true, speed: 0.5, minimumValue: 0.1, sync: false } },
            size: { value: 3, random: true, animation: { enable: true, speed: 1, minimumValue: 0.5, sync: false } },
            move: { enable: true, speed: 0.6, direction: "top", random: true, straight: false, outModes: { default: "out" } }
        },
        detectRetina: true
    });
});
</script>
"""

def inject(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        modified = False
        
        # Inject head
        if "<!-- HERO & PARTICLES FIX -->" not in content and "</head>" in content:
            content = content.replace("</head>", head_injection + "\n</head>")
            modified = True
            
        # Inject body
        if "<!-- TSPARTICLES -->" not in content and "</body>" in content:
            content = content.replace("</body>", body_injection + "\n</body>")
            modified = True
            
        if modified:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except:
        pass
    return False

count = 0
for root, dirs, files in os.walk('www.hiddenjunglecusco.com'):
    if '.git' in root or 'admin' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            if inject(os.path.join(root, f)):
                count += 1

print(f"Injected into {count} files")
