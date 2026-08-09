import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css'

with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

gallery_css = """
/* --- GALLERY & INSTA GRID LAYOUT --- */
.gallery-item {
  display: block;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
.gallery-item img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.gallery-item:hover img {
  transform: scale(1.08);
}

.insta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.insta-card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  display: block;
  box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}
.insta-card img {
  width: 100%;
  height: 450px;
  object-fit: cover;
  display: block;
  transition: transform 0.6s ease;
}
.insta-card:hover img {
  transform: scale(1.05);
}

.play-icon {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(5px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #fff;
  transition: all 0.3s ease;
}
.insta-card:hover .play-icon {
  transform: translate(-50%, -50%) scale(1.2);
  background: rgba(16,185,129,0.9);
}

.insta-hover {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 30px 20px 20px 20px;
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
  color: #fff;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.4s ease;
}
.insta-card:hover .insta-hover {
  opacity: 1;
  transform: translateY(0);
}
.insta-hover i {
  font-size: 1.5rem;
  margin-bottom: 8px;
  color: #E1306C;
}
.insta-hover p {
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
/* --- END GALLERY & INSTA GRID LAYOUT --- */
"""

if "/* --- GALLERY & INSTA GRID LAYOUT --- */" not in css:
    css += "\n" + gallery_css
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Gallery CSS injected.")
else:
    print("Gallery CSS already exists.")
