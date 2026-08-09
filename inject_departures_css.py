import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css'

with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

dep_css = """
/* --- DEPARTURES PAGE LAYOUT --- */
.departures-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dep-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px auto;
}
.dep-intro h2 { margin-bottom: 20px; font-size: 2.2rem; }
.dep-intro p {
  color: rgba(255,255,255,0.7);
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.dep-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 40px;
  margin-bottom: 60px;
}

.dep-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.dep-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.3);
}

.dep-img {
  width: 100%;
  height: 200px;
  background-size: cover;
  background-position: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.5s ease;
}
.dep-card:hover .dep-img {
  transform: scale(1.05);
}

.dep-content {
  padding: 30px;
  position: relative;
  background: rgba(0,0,0,0.4);
  height: 100%;
}

.dep-content h3 {
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  color: #10B981;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 15px;
}

.dep-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.dep-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 0.95rem;
  color: rgba(255,255,255,0.85);
  line-height: 1.5;
}
.dep-list li i {
  color: #10B981;
  margin-top: 4px;
}
.dep-list li strong {
  color: #fff;
  font-weight: 600;
}

.dep-cta {
  text-align: center;
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 20px;
  padding: 40px;
  margin-top: 20px;
}
.dep-cta h4 {
  font-size: 1.4rem;
  margin-bottom: 24px;
  font-family: 'Syne', sans-serif;
}
.dep-cta .btn {
  padding: 16px 32px;
  font-size: 1.1rem;
}
/* --- END DEPARTURES PAGE LAYOUT --- */
"""

if "/* --- DEPARTURES PAGE LAYOUT --- */" not in css:
    css += "\n" + dep_css
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Departures CSS injected.")
else:
    print("Departures CSS already exists.")
