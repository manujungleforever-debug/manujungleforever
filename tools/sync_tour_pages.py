import json, os, urllib.parse, re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www.manujungleforever.com'))
tours_path = os.path.join(ROOT_DIR, 'data', 'tours.json')
template_path = os.path.join(ROOT_DIR, 'data', 'tour-template.html')

def clean_mojibake(text):
    if not text: return ''
    replacements = {
        'Ã¡': 'á', 'Ã©': 'é', 'Ã\xad': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã±': 'ñ', 'Ã': 'Á', 'Ã‰': 'É', 'Ã\xad': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú', 'Ã‘': 'Ñ',
        'Â¿': '¿', 'Â¡': '¡', 'Â': '', 'â€“': '–', 'â€”': '—',
        'â€˜': '‘', 'â€™': '’', 'â€œ': '“', 'â€ ': '”', 'â€¢': '•'
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def md_to_html(md):
    if not md: return ''
    md = clean_mojibake(md)
    md = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', md)
    md = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', md)
    md = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', md)
    md = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.*?)\*', r'<em>\1</em>', md)
    lines = md.split('\n')
    in_list = False
    new_lines = []
    for l in lines:
        stripped = l.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                new_lines.append('<ul style="margin: 16px 0; padding-left: 24px;">')
                in_list = True
            new_lines.append(f'<li style="margin-bottom: 8px; line-height: 1.6;">{stripped[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            if stripped:
                new_lines.append(f'<p style="margin-bottom: 16px; line-height: 1.8;">{stripped}</p>')
    if in_list:
        new_lines.append('</ul>')
    return '\n'.join(new_lines)

CATEGORY_ORDER_MAP = {
    'manu reserve zone': 1,
    'reserve': 1,
    'manu cultural zone': 2,
    'cultural': 2,
    'birding & photography': 3,
    'birding': 3,
    'birdwatching': 3,
    'photo': 3,
    'wildlife': 4,
    'roadtrip': 5,
    'expedition': 6
}

def get_category_rank(cat_name):
    if not cat_name: return 9999
    c = str(cat_name).lower().strip()
    if c in CATEGORY_ORDER_MAP: return CATEGORY_ORDER_MAP[c]
    if 'reserve' in c: return 1
    if 'cultural' in c: return 2
    if 'bird' in c or 'photo' in c: return 3
    if 'wildlife' in c: return 4
    if 'road' in c: return 5
    if 'expedition' in c: return 6
    return 999

def tour_sort_key_py(t):
    cr = get_category_rank(t.get('categoria'))
    try:
        dur = float(t.get('duracion_dias') or 999999)
        if dur <= 0: dur = 999999
    except Exception:
        dur = 999999
    pos = float(t.get('posicion') or 999999)
    name = str(t.get('nombre', '')).lower()
    return (cr, dur, pos, name)

CAT_MAP = {
    'manu reserve zone': {'label': 'MANU RESERVE ZONE', 'icon': 'fas fa-compass'},
    'reserve': {'label': 'MANU RESERVE ZONE', 'icon': 'fas fa-compass'},
    'manu cultural zone': {'label': 'MANU CULTURAL ZONE', 'icon': 'fas fa-compass'},
    'cultural': {'label': 'MANU CULTURAL ZONE', 'icon': 'fas fa-compass'},
    'birding & photography': {'label': 'BIRDING & PHOTOGRAPHY', 'icon': 'fas fa-compass'},
    'birding': {'label': 'BIRDING & PHOTOGRAPHY', 'icon': 'fas fa-compass'},
    'birdwatching': {'label': 'BIRDING & PHOTOGRAPHY', 'icon': 'fas fa-compass'},
    'wildlife': {'label': 'WILDLIFE QUEST', 'icon': 'fas fa-compass'},
    'roadtrip': {'label': 'RAINFOREST ROAD TRIP', 'icon': 'fas fa-compass'},
    'expedition': {'label': 'AMAZON EXPEDITION', 'icon': 'fas fa-compass'},
    'machu wasi': {'label': 'MACHU WASI ADVENTURE', 'icon': 'fas fa-compass'},
    'photography': {'label': 'WILDLIFE PHOTOGRAPHY', 'icon': 'fas fa-compass'}
}

def render_itinerary_accordion(itinerario, tour_title):
    if not itinerario:
        return '<p style="color:var(--earth-text, #4B5563); font-style:italic; padding:16px 0;">Custom day-by-day itinerary tailored upon request.</p>'

    html_parts = []
    for i, it in enumerate(itinerario):
        day_num = it.get('dia', i + 1)
        day_pad = f"{int(day_num):02d}"
        day_title = clean_mojibake(it.get('titulo') or '').strip()
        if not day_title:
            day_title = f"Day {day_num}"
        day_subtitle = clean_mojibake(it.get('subtitulo') or '').strip()
        is_open = (i == 0)

        bloques = it.get('bloques') or []
        body_parts = []

        if bloques:
            for b in bloques:
                b_type = b.get('tipo', 'texto')
                if b_type in ('imagen', 'image'):
                    img_url = b.get('url', '')
                    if img_url.startswith('/') and not img_url.startswith('//'):
                        img_url = '..' + img_url
                    alt_text = clean_mojibake(b.get('alt') or day_title)
                    caption = clean_mojibake(b.get('pie') or '').strip()
                    cap_html = f'<figcaption class="it-caption">{caption}</figcaption>' if caption else ''
                    body_parts.append(f"""
              <figure class="it-figure">
                <div class="it-img-box">
                  <img src="{img_url}" alt="{alt_text}" loading="lazy">
                </div>
                {cap_html}
              </figure>""")
                else:
                    content = clean_mojibake(b.get('contenido') or b.get('texto') or '')
                    if content.strip():
                        body_parts.append(f"""
              <div class="it-text-block">
                {md_to_html(content)}
              </div>""")
        elif it.get('descripcion') and it.get('descripcion').strip():
            desc = clean_mojibake(it.get('descripcion'))
            body_parts.append(f"""
              <div class="it-text-block">
                {md_to_html(desc)}
              </div>""")

        if not body_parts:
            body_parts.append(f'<p style="color:var(--earth-text, #4B5563); font-style:italic; margin:0;">Detailed highlights for this day will be coordinated with your certified guide.</p>')

        body_html = '\n'.join(body_parts)
        subtitle_html = f'<p class="it-day-subtitle">{day_subtitle}</p>' if day_subtitle else ''

        open_cls = 'is-open' if is_open else ''
        expanded_val = 'true' if is_open else 'false'
        hidden_val = 'false' if is_open else 'true'

        html_parts.append(f"""
  <div class="it-day-item {open_cls}" data-day="{day_num}">
    <button type="button" class="it-day-header" aria-expanded="{expanded_val}" aria-controls="it-body-{day_num}" id="it-btn-{day_num}">
      <div class="it-day-header-left">
        <div class="it-day-badge">
          <span class="it-badge-tag">DAY</span>
          <span class="it-badge-num">{day_pad}</span>
        </div>
        <div class="it-day-titles">
          <h3 class="it-day-title">{day_title}</h3>
          {subtitle_html}
        </div>
      </div>
      <div class="it-day-chevron">
        <i class="fas fa-chevron-down"></i>
      </div>
    </button>
    <div class="it-day-body" id="it-body-{day_num}" role="region" aria-labelledby="it-btn-{day_num}" aria-hidden="{hidden_val}">
      <div class="it-content-wrap">
        {body_html}
      </div>
    </div>
  </div>""")

    return '\n'.join(html_parts)

def main():
    with open(tours_path, 'r', encoding='utf-8') as f:
        tours_data = json.load(f)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    active_tours = [t for t in tours_data.get('tours', []) if t.get('estado') not in ('inactivo', 'borrador')]
    active_tours = sorted(active_tours, key=tour_sort_key_py)

    groups = {}
    for t in active_tours:
        cat = (t.get('categoria') or 'wildlife').lower().strip()
        groups.setdefault(cat, []).append(t)

    all_cats = sorted(groups.keys(), key=lambda c: (get_category_rank(c), c))

    desktop_items = []
    mobile_items = []
    for cat in all_cats:
        info = CAT_MAP.get(cat, {'label': cat.upper(), 'icon': 'fas fa-compass'})
        items = sorted(groups[cat], key=lambda t: tour_sort_key_py(t)[1:])
        if not items: continue

        desktop_items.append(f'<span class="dh"><i class="{info["icon"]}"></i> {info["label"]}</span>')
        mobile_items.append(f'<span class="dh" style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="{info["icon"]}"></i> {info["label"]}</span>')

        for t in items:
            slug = t.get('slug') or t.get('id')
            nombre = clean_mojibake(t.get('nombre', ''))
            url = f"../{slug}/index.html"
            desktop_items.append(f'<li><a href="{url}">{nombre}</a></li>')
            mobile_items.append(f'<li><a href="{url}">{nombre}</a></li>')

    desktop_menu_html = '\n'.join(desktop_items)
    mobile_menu_html = '\n'.join(mobile_items)

    generated_count = 0
    for t in active_tours:
        slug = t.get('slug') or t.get('id')
        tour_name = clean_mojibake(t.get('nombre', 'Tour'))
        cat_key = (t.get('categoria') or 'wildlife').lower().strip()
        cat_info = CAT_MAP.get(cat_key, {'label': cat_key.upper(), 'icon': 'fas fa-compass'})

        html_body = md_to_html(t.get('descripcion_larga') or t.get('descripcion_corta') or '')
        itinerary_html = render_itinerary_accordion(t.get('itinerario') or [], tour_name)

        hero_img = t.get('imagen_hero') or '../assets/img/hero.png'
        if hero_img.startswith('/') and not hero_img.startswith('//'):
            hero_img = '..' + hero_img

        dur_str = f"{t.get('duracion_dias', 1)} Days / {t.get('duracion_noches', 0)} Nights"
        cap_str = f"{t.get('capacidad_min', 1)}–{t.get('capacidad_max', 8)} Travelers"
        meta_title = f"{tour_name} | Manu Jungle Forever"

        meta_desc = clean_mojibake(t.get('descripcion_corta') or t.get('descripcion_larga') or '').replace('\n', ' ').strip()
        if len(meta_desc) > 155:
            meta_desc = meta_desc[:152] + '...'

        public_url = f"https://www.manujungleforever.com/{slug}/"
        og_img_url = hero_img if hero_img.startswith('http') else 'https://www.manujungleforever.com/' + hero_img.replace('../', '').replace('/', '')

        page_content = template
        page_content = page_content.replace('{{META_TITLE}}', meta_title)
        page_content = page_content.replace('{{META_DESCRIPTION}}', meta_desc)
        page_content = page_content.replace('{{OG_URL}}', public_url)
        page_content = page_content.replace('{{CANONICAL_URL}}', public_url)
        page_content = page_content.replace('{{TITLE}}', tour_name)
        page_content = page_content.replace('{{TITLE_ENCODED}}', urllib.parse.quote(tour_name))
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
        page_content = page_content.replace('{{DESCRIPCION_CORTA}}', clean_mojibake(t.get('descripcion_corta', '')))
        page_content = page_content.replace('{{CONTENT}}', html_body)
        page_content = page_content.replace('{{ITINERARIO_HTML}}', itinerary_html)
        page_content = page_content.replace('{{GUIDED_TOURS_MENU_DESKTOP}}', desktop_menu_html)
        page_content = page_content.replace('{{GUIDED_TOURS_MENU_MOBILE}}', mobile_menu_html)

        out_dir = os.path.join(ROOT_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, 'index.html')
        with open(out_file, 'w', encoding='utf-8') as out_f:
            out_f.write(page_content)
        generated_count += 1
        print(f"Generated tour page: {slug}/index.html (${t.get('precio_desde', 0)} USD)")

    print(f"\nSuccessfully generated {generated_count} tour detail pages with new accessible accordion, pricing contrast and departures widget.")

if __name__ == '__main__':
    main()
