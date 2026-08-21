import json, os, urllib.parse, re

# Simple Markdown to HTML converter for descriptions
def md_to_html(md):
    if not md:
        return ''
    # Headers
    md = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', md)
    md = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', md)
    md = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', md)
    # Bold & Italic
    md = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.*?)\*', r'<em>\1</em>', md)
    # Lists
    lines = md.split('\n')
    in_list = False
    new_lines = []
    for l in lines:
        if l.strip().startswith('- ') or l.strip().startswith('* '):
            if not in_list:
                new_lines.append('<ul style="margin: 16px 0; padding-left: 20px;">')
                in_list = True
            new_lines.append(f'<li style="margin-bottom: 8px;">{l.strip()[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            if l.strip():
                new_lines.append(f'<p style="margin-bottom: 16px; line-height: 1.8;">{l}</p>')
    if in_list:
        new_lines.append('</ul>')
    return '\n'.join(new_lines)

tours_path = 'www.manujungleforever.com/data/tours.json'
template_path = 'www.manujungleforever.com/data/tour-template.html'

with open(tours_path, 'r', encoding='utf-8') as f:
    tours_data = json.load(f)

with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

CAT_MAP = {
    'wildlife': {'label': 'WILDLIFE QUEST', 'icon': 'fas fa-binoculars'},
    'roadtrip': {'label': 'RAINFOREST ROAD TRIP', 'icon': 'fas fa-route'},
    'expedition': {'label': 'AMAZON EXPEDITION', 'icon': 'fas fa-campground'},
    'cultural': {'label': 'CULTURAL EXPEDITION', 'icon': 'fas fa-landmark'},
    'birdwatching': {'label': 'BIRDWATCHING QUEST', 'icon': 'fas fa-dove'},
    'machu wasi': {'label': 'MACHU WASI ADVENTURE', 'icon': 'fas fa-tree'},
    'photography': {'label': 'WILDLIFE PHOTOGRAPHY', 'icon': 'fas fa-camera'}
}

# Build guided tours menu
active_tours = [t for t in tours_data.get('tours', []) if t.get('estado') == 'activo']
order = ['wildlife', 'roadtrip', 'expedition', 'cultural', 'birdwatching', 'machu wasi', 'photography']
groups = {}
for t in active_tours:
    c = (t.get('categoria') or 'wildlife').lower().strip()
    if c not in groups:
        groups[c] = []
    groups[c].append(t)

all_cats = [c for c in order if c in groups] + [c for c in groups if c not in order]

desktop_html = ''
mobile_html = ''
for cat in all_cats:
    info = CAT_MAP.get(cat, {'label': cat.upper(), 'icon': 'fas fa-compass'})
    items = groups.get(cat, [])
    if not items:
        continue
    desktop_html += f'\n        <span class="dh"><i class="{info["icon"]}"></i> {info["label"]}</span>'
    mobile_html += f'\n        <span class="dh" style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="{info["icon"]}"></i> {info["label"]}</span>'
    for it in items:
        slug = it.get('slug') or it.get('id')
        url = f'../{slug}/index.html'
        desktop_html += f'\n        <li><a href="{url}">{it.get("nombre")}</a></li>'
        mobile_html += f'\n        <li><a href="{url}">{it.get("nombre")}</a></li>'

for t in active_tours:
    slug = t.get('slug') or t.get('id')
    cat_key = (t.get('categoria') or 'wildlife').lower().strip()
    cat_info = CAT_MAP.get(cat_key, {'label': cat_key.upper(), 'icon': 'fas fa-compass'})
    
    html_body = md_to_html(t.get('descripcion_larga') or t.get('descripcion_corta') or '')
    
    itinerary_html = ''
    itinerario = t.get('itinerario') or []
    if itinerario:
        for i, it in enumerate(itinerario):
            day_num = it.get('dia', i + 1)
            day_title = f'Day {day_num}: {it.get("titulo")}' if it.get('titulo') else f'Day {day_num}'
            desc = (it.get('descripcion') or '').replace('\n', '<br>')
            itinerary_html += f"""
        <div style="background:var(--f); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:24px;">
          <h3 style="color:var(--a, #2dd4bf); font-size:1.25rem; font-weight:700; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
            <i class="far fa-calendar-check" style="font-size:1.1rem;"></i> {day_title}
          </h3>
          <p style="color:rgba(255,255,255,0.85); font-size:1rem; line-height:1.75; margin:0;">
            {desc}
          </p>
        </div>"""
    else:
        itinerary_html = '<p style="color:rgba(255,255,255,0.6); font-style:italic;">Custom day-by-day itinerary tailored upon request.</p>'
        
    hero_img = t.get('imagen_hero') or '../assets/img/hero.png'
    if hero_img.startswith('/'):
        hero_img = '..' + hero_img
    
    dur_str = f"{t.get('duracion_dias', 1)} Days / {t.get('duracion_noches', 0)} Nights"
    cap_str = f"{t.get('capacidad_min', 1)}–{t.get('capacidad_max', 8)} Travelers"
    meta_title = f"{t.get('nombre', 'Tour')} | Manu Jungle Forever"
    
    meta_desc = (t.get('descripcion_corta') or t.get('descripcion_larga') or '').replace('\n', ' ').strip()
    if len(meta_desc) > 155:
        meta_desc = meta_desc[:152] + '...'
        
    public_url = f"https://www.manujungleforever.com/{slug}/"
    og_img_url = hero_img if hero_img.startswith('http') else 'https://www.manujungleforever.com/' + hero_img.replace('../', '').replace('/', '')
    
    page_content = template
    page_content = page_content.replace('{{META_TITLE}}', meta_title)
    page_content = page_content.replace('{{META_DESCRIPTION}}', meta_desc)
    page_content = page_content.replace('{{OG_URL}}', public_url)
    page_content = page_content.replace('{{CANONICAL_URL}}', public_url)
    page_content = page_content.replace('{{TITLE}}', t.get('nombre', ''))
    page_content = page_content.replace('{{TITLE_ENCODED}}', urllib.parse.quote(t.get('nombre', 'Tour')))
    page_content = page_content.replace('{{SLUG}}', slug)
    page_content = page_content.replace('{{EXCERPT}}', meta_desc)
    page_content = page_content.replace('{{CATEGORIA_LABEL}}', cat_info['label'])
    page_content = page_content.replace('{{HERO_IMAGE}}', hero_img)
    page_content = page_content.replace('{{OG_IMAGE}}', og_img_url)
    page_content = page_content.replace('{{DURACION}}', dur_str)
    page_content = page_content.replace('{{PRECIO}}', str(t.get('precio_desde', 0)))
    page_content = page_content.replace('{{CAPACIDAD}}', cap_str)
    page_content = page_content.replace('{{DIFICULTAD}}', t.get('dificultad', 'Easy'))
    page_content = page_content.replace('{{TEMPORADA}}', t.get('temporada', 'All year'))
    page_content = page_content.replace('{{DESCRIPCION_CORTA}}', t.get('descripcion_corta', ''))
    page_content = page_content.replace('{{CONTENT}}', html_body)
    page_content = page_content.replace('{{ITINERARIO_HTML}}', itinerary_html)
    page_content = page_content.replace('{{GUIDED_TOURS_MENU_DESKTOP}}', desktop_html)
    page_content = page_content.replace('{{GUIDED_TOURS_MENU_MOBILE}}', mobile_html)
    
    out_dir = f'www.manujungleforever.com/{slug}'
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'index.html')
    with open(out_file, 'w', encoding='utf-8') as out_f:
        out_f.write(page_content)
    print(f"Generated tour page: {out_file} with price ${t.get('precio_desde')} USD")

print("All active tour pages synced with standardized USD pricing.")
