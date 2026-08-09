import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css'

with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

contact_css = """
/* --- CONTACT PAGE LAYOUT --- */
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: start;
}

@media(max-width: 900px) {
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

.contact-info-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.2);
  backdrop-filter: blur(10px);
}

.contact-info-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 30px;
}
.contact-info-item:last-child { margin-bottom: 0; }

.ci-icon {
  width: 50px;
  height: 50px;
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.ci-label {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 6px;
  color: #fff;
}

.ci-val, .ci-val a {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.95rem;
  line-height: 1.6;
  text-decoration: none;
  transition: color 0.3s ease;
}
.ci-val a:hover {
  color: #10B981;
}

.form-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 50px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.3);
  backdrop-filter: blur(10px);
}

.form-row {
  margin-bottom: 24px;
}
.form-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

@media(max-width: 600px) {
  .form-2col { grid-template-columns: 1fr; gap: 24px; }
  .form-card { padding: 30px 20px; }
}

.form-row label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-req { color: #10B981; }

.form-row input,
.form-row select,
.form-row textarea {
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px 20px;
  color: #fff;
  font-size: 1rem;
  font-family: 'Outfit', sans-serif;
  transition: all 0.3s ease;
}

.form-row input:focus,
.form-row select:focus,
.form-row textarea:focus {
  outline: none;
  border-color: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
  background: rgba(0, 0, 0, 0.4);
}

.wa-cta-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(37, 211, 102, 0.15), rgba(18, 140, 80, 0.1));
  border: 1px solid rgba(37, 211, 102, 0.2);
  border-radius: 16px;
  padding: 30px 40px;
  margin-top: 60px;
  gap: 20px;
  flex-wrap: wrap;
}

.wa-cta-text h3 {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  margin-bottom: 8px;
}
.wa-cta-text p {
  color: rgba(255,255,255,0.7);
  font-size: 0.95rem;
}

.btn-wa {
  background: #25D366;
  color: #fff;
  padding: 14px 28px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(37,211,102,0.3);
  white-space: nowrap;
}
.btn-wa:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(37,211,102,0.4);
  background: #28E16D;
}
/* --- END CONTACT PAGE LAYOUT --- */
"""

if "/* --- CONTACT PAGE LAYOUT --- */" not in css:
    css += "\n" + contact_css
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Contact CSS injected.")
else:
    print("Contact CSS already exists.")
