import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
libro_html_path = os.path.join(base_dir, 'libro-de-reclamaciones', 'index.html')
css_path = os.path.join(base_dir, 'assets', 'css', 'new.css')

new_form_html = """
<div class="reclamo-wrapper">
  <div class="reclamo-box">
    <h3 class="reclamo-subtitle">Hoja de Reclamación Virtual</h3>
    <p class="reclamo-desc">La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.</p>
  </div>

  <form id="formReclamo" class="reclamo-form-container" novalidate>
    <!-- Honeypot anti-spam -->
    <div style="display:none;">
        <label>Si eres humano, deja este campo en blanco</label>
        <input type="text" name="website_url" value="">
    </div>
    
    <!-- 1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE -->
    <div class="reclamo-section">
        <h4>1. Identificación del Consumidor</h4>
        <div class="reclamo-grid">
            <div class="reclamo-group">
                <label>Nombres y Apellidos *</label>
                <input type="text" name="nombres" required>
            </div>
            <div class="reclamo-group">
                <label>DNI / CE / RUC *</label>
                <input type="text" name="documento" required>
            </div>
            <div class="reclamo-group full-width">
                <label>Domicilio *</label>
                <input type="text" name="domicilio" required>
            </div>
            <div class="reclamo-group">
                <label>Teléfono / Celular *</label>
                <input type="tel" name="telefono" required>
            </div>
            <div class="reclamo-group">
                <label>Correo Electrónico *</label>
                <input type="email" name="correo" required>
            </div>
            <div class="reclamo-group full-width">
                <label>Padre o Madre (Solo en caso de menores de edad)</label>
                <input type="text" name="apoderado" placeholder="Nombres y apellidos del apoderado">
            </div>
        </div>
    </div>

    <!-- 2. IDENTIFICACIÓN DEL BIEN CONTRATADO -->
    <div class="reclamo-section">
        <h4>2. Identificación del Bien Contratado</h4>
        <div class="reclamo-grid">
            <div class="reclamo-group">
                <label>Tipo de Bien *</label>
                <div class="reclamo-radio-group">
                    <label class="reclamo-radio">
                        <input type="radio" name="bien_tipo" value="Producto" required>
                        <span>Producto</span>
                    </label>
                    <label class="reclamo-radio">
                        <input type="radio" name="bien_tipo" value="Servicio" required>
                        <span>Servicio</span>
                    </label>
                </div>
            </div>
            <div class="reclamo-group">
                <label>Monto Reclamado (Opcional)</label>
                <input type="number" step="0.01" name="bien_monto" placeholder="0.00">
            </div>
            <div class="reclamo-group full-width">
                <label>Descripción del Producto/Servicio *</label>
                <textarea name="bien_descripcion" rows="3" required placeholder="Ej. Tour de 3 días..."></textarea>
            </div>
        </div>
    </div>
    
    <!-- 3. DETALLE DE LA RECLAMACIÓN Y PEDIDO -->
    <div class="reclamo-section">
        <h4>3. Detalle de la Reclamación y Pedido</h4>
        <div class="reclamo-group full-width">
            <label>Tipo de Reclamación *</label>
            <div class="reclamo-cards">
                <label class="reclamo-card">
                    <input type="radio" name="tipo" value="Reclamo" required>
                    <div class="reclamo-card-content">
                        <span class="reclamo-card-title">Reclamo</span>
                        <span class="reclamo-card-desc">Disconformidad relacionada a los productos o servicios.</span>
                    </div>
                </label>
                <label class="reclamo-card">
                    <input type="radio" name="tipo" value="Queja" required>
                    <div class="reclamo-card-content">
                        <span class="reclamo-card-title">Queja</span>
                        <span class="reclamo-card-desc">Disconformidad no relacionada a los productos o servicios; o, malestar o descontento respecto a la atención al público.</span>
                    </div>
                </label>
            </div>
        </div>
        
        <div class="reclamo-group full-width">
            <label>Detalle de lo ocurrido *</label>
            <textarea name="detalle" rows="4" required placeholder="Describa los hechos..."></textarea>
        </div>
        <div class="reclamo-group full-width">
            <label>Pedido (Lo que usted solicita) *</label>
            <textarea name="pedido" rows="3" required placeholder="Indique qué solicita como solución..."></textarea>
        </div>
    </div>

    <!-- DECLARACIÓN JURADA -->
    <div class="reclamo-section">
        <label class="reclamo-checkbox">
            <input type="checkbox" id="declaracion" required>
            <span>
                Declaro que el contenido de mi reclamación es verdadero y acepto las <a href="../privacy-policy/index.html" target="_blank">Políticas de Privacidad</a> para el tratamiento de mis datos personales en la gestión de mi reclamo/queja.
            </span>
        </label>
    </div>

    <!-- CAPTCHA Matemático -->
    <div class="reclamo-section captcha-section">
        <label><i class="fa-solid fa-shield-halved"></i> Verificación de Seguridad *</label>
        <div class="captcha-container">
            <div id="captcha-box"></div>
            <input type="number" id="captcha-input" required placeholder="Resultado matemático">
        </div>
    </div>
    
    <button type="submit" class="reclamo-btn-submit">
        Enviar Libro de Reclamaciones
    </button>
  </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
    // Captcha
    const captchaBox = document.getElementById('captcha-box');
    const captchaInput = document.getElementById('captcha-input');
    let expectedCaptcha = 0;
    function generateCaptcha() {
        const n1 = Math.floor(Math.random() * 10) + 1;
        const n2 = Math.floor(Math.random() * 10) + 1;
        expectedCaptcha = n1 + n2;
        if(captchaBox) captchaBox.innerText = `${n1} + ${n2} =`;
        if(captchaInput) captchaInput.value = '';
    }
    if (captchaBox) generateCaptcha();

    // Formularios Submit (Por ahora validamos y mostramos alerta hasta tener la API)
    const form = document.getElementById('formReclamo');
    if(form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            if (parseInt(captchaInput.value) !== expectedCaptcha) {
                captchaInput.style.borderColor = 'red';
                captchaInput.value = '';
                captchaInput.placeholder = '¡Incorrecto!';
                setTimeout(() => {
                    captchaInput.style.borderColor = '';
                    captchaInput.placeholder = 'Resultado matemático';
                }, 2000);
                generateCaptcha();
                return;
            }
            alert("El formulario está listo para integrarse con la API de Resend.");
            // Aquí irá la lógica de fetch
        });
    }
});
</script>
"""

new_css = """
/* --- Libro de Reclamaciones Wachicargo Style --- */
.reclamo-wrapper {
    max-width: 1000px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 40px;
    border-radius: 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    margin-top: 20px;
}
@media (max-width: 768px) {
    .reclamo-wrapper { padding: 20px; }
}

.reclamo-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 32px;
}
.reclamo-subtitle {
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}
.reclamo-desc {
    color: rgba(255,255,255,0.6);
    font-size: 0.875rem;
    margin: 0;
}

.reclamo-form-container {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.reclamo-section {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 32px;
}
.reclamo-section h4 {
    color: var(--a);
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    margin: 0 0 24px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 16px;
}

.reclamo-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}
@media (max-width: 768px) {
    .reclamo-grid { grid-template-columns: 1fr; }
}

.reclamo-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.reclamo-group.full-width {
    grid-column: 1 / -1;
}
.reclamo-group label {
    color: rgba(255,255,255,0.7);
    font-size: 0.875rem;
}
.reclamo-group input[type="text"],
.reclamo-group input[type="tel"],
.reclamo-group input[type="email"],
.reclamo-group input[type="number"],
.reclamo-group textarea {
    width: 100%;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 12px 16px;
    color: #fff;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-sizing: border-box;
}
.reclamo-group input:focus,
.reclamo-group textarea:focus {
    outline: none;
    border-color: var(--a);
    box-shadow: 0 0 0 1px var(--a);
}

.reclamo-radio-group {
    display: flex;
    gap: 24px;
    margin-top: 8px;
}
.reclamo-radio {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: #fff;
}
.reclamo-radio input[type="radio"] {
    accent-color: var(--a);
    width: 18px;
    height: 18px;
}

.reclamo-cards {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.reclamo-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    cursor: pointer;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.5);
    transition: all 0.3s ease;
}
.reclamo-card:hover {
    border-color: rgba(13, 178, 107, 0.5);
}
.reclamo-card input[type="radio"] {
    margin-top: 4px;
    accent-color: var(--a);
    width: 18px;
    height: 18px;
}
.reclamo-card-title {
    display: block;
    color: #fff;
    font-weight: 700;
    margin-bottom: 4px;
}
.reclamo-card-desc {
    color: rgba(255,255,255,0.6);
    font-size: 0.875rem;
}

.reclamo-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    cursor: pointer;
}
.reclamo-checkbox input[type="checkbox"] {
    margin-top: 4px;
    accent-color: var(--a);
    width: 18px;
    height: 18px;
}
.reclamo-checkbox span {
    color: rgba(255,255,255,0.6);
    font-size: 0.875rem;
    line-height: 1.6;
}
.reclamo-checkbox a {
    color: var(--a);
    text-decoration: none;
}
.reclamo-checkbox a:hover {
    text-decoration: underline;
}

.captcha-section {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
}
@media (max-width: 768px) {
    .captcha-section { flex-direction: column; align-items: flex-start; }
}
.captcha-section label {
    color: rgba(255,255,255,0.6);
    font-size: 0.875rem;
    white-space: nowrap;
}
.captcha-section label i {
    color: var(--a);
    margin-right: 8px;
}
.captcha-container {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
}
#captcha-box {
    background: #020617;
    border: 1px solid rgba(13, 178, 107, 0.3);
    color: var(--a);
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.125rem;
    padding: 12px 16px;
    border-radius: 12px;
    min-width: 120px;
    text-align: center;
    box-shadow: 0 0 10px rgba(13, 178, 107, 0.1);
}
#captcha-input {
    width: 100%;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 12px 16px;
    color: #fff;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    box-sizing: border-box;
}
#captcha-input:focus {
    outline: none;
    border-color: var(--a);
    box-shadow: 0 0 0 1px var(--a);
}

.reclamo-btn-submit {
    width: 100%;
    background: linear-gradient(to right, var(--a), #065f46);
    color: #fff;
    font-weight: 700;
    padding: 16px;
    border-radius: 12px;
    border: none;
    font-size: 1.125rem;
    font-family: 'Outfit', sans-serif;
    cursor: pointer;
    box-shadow: 0 0 15px rgba(13, 178, 107, 0.5);
    transition: all 0.3s ease;
}
.reclamo-btn-submit:hover {
    box-shadow: 0 0 25px rgba(13, 178, 107, 0.8);
    background: linear-gradient(to right, #065f46, var(--a));
}
"""

with open(libro_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace everything from <div class="reclamo-box"> to the end of </form> with our new html
import re
new_content = re.sub(r'<div class="reclamo-box">.*?</div>\s*</div>\s*</section>', new_form_html + '\n    </div>\n  </div>\n</section>', content, flags=re.DOTALL)
# Wait, let's be safer. The old form started with <div class="reclamo-box"> and ended with </form>
# Actually, wait, looking at the previous file structure:
# <div class="reclamo-box">
#   <h3>Hoja de Reclamación Virtual</h3>
# ...
# </form>
new_content = re.sub(r'<div class="reclamo-box">\s*<h3>Hoja de Reclamación.*?</form>', new_form_html, content, flags=re.DOTALL)

with open(libro_html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

with open(css_path, 'a', encoding='utf-8') as f:
    f.write(new_css)

print("Form replaced and CSS added.")
