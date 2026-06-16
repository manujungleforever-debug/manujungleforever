import os

path = 'www.hiddenjunglecusco.com/admin/index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

particles_code = """
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

if '<!-- TSPARTICLES -->' not in content:
    content = content.replace('</body>', particles_code + '\n</body>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added particles!")
else:
    print("Particles already present.")
