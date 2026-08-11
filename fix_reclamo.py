import os

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'
css_path = os.path.join(base, 'assets', 'css', 'new.css')

new_css = """
/* --- Libro de Reclamaciones Form --- */
.reclamo-header {
  text-align: center;
  margin-bottom: 40px;
}
.reclamo-header i {
  font-size: 3rem;
  color: var(--a);
  margin-bottom: 15px;
}
.reclamo-header h1 {
  font-family: 'Syne', sans-serif;
  color: #fff;
  font-size: 2.5rem;
  margin-bottom: 15px;
}
.reclamo-header h1 span {
  color: var(--a);
}
.reclamo-header p {
  color: rgba(255,255,255,0.7);
  font-size: 1.1rem;
}

.reclamo-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
}
.reclamo-box.glow {
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}
.reclamo-box h3 {
  color: #fff;
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  margin-bottom: 25px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 15px;
  margin-top: 0;
}

.reclamo-form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
@media (max-width: 768px) {
  .reclamo-form-row {
    grid-template-columns: 1fr;
  }
}

.reclamo-input-group label {
  display: block;
  color: rgba(255,255,255,0.8);
  margin-bottom: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: left;
}
.reclamo-input-group input,
.reclamo-input-group select,
.reclamo-input-group textarea {
  width: 100%;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 12px 15px;
  color: #fff;
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}
.reclamo-input-group input:focus,
.reclamo-input-group select:focus,
.reclamo-input-group textarea:focus {
  outline: none;
  border-color: var(--a);
  background: rgba(255,255,255,0.08);
}
/* Ensure dropdown options are readable on dark background */
.reclamo-input-group select option {
  background: #0f1513; 
  color: #fff;
}
.reclamo-input-group input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1);
}

.reclamo-submit {
  background: var(--a);
  color: #fff;
  border: none;
  border-radius: 30px;
  padding: 15px 40px;
  font-family: 'Outfit', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.reclamo-submit:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
}
"""

with open(css_path, 'r', encoding='utf-8') as f:
    content = f.read()

if ".reclamo-box" not in content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(new_css)
    print("Added reclamo CSS to new.css")
else:
    print("Reclamo CSS already exists.")
