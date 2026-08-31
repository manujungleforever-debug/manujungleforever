import os
import json
import glob
from bs4 import BeautifulSoup
import urllib.parse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www.manujungleforever.com'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def fix_img_path(p):
    if not p: return ''
    if p.startswith('http://') or p.startswith('https://') or p.startswith('data:'): return p
    if p.startswith('/'): return p
    return '/' + p

def clean_mojibake(text):
    if not text: return ''
    replacements = {
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã±': 'ñ', 'Ã': 'Á', 'Ã‰': 'É', 'Ã': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú', 'Ã‘': 'Ñ',
        'Â¿': '¿', 'Â¡': '¡', 'Â': '', 'â€“': '–', 'â€”': '—',
        'â€˜': '‘', 'â€™': '’', 'â€œ': '“', 'â€': '”', 'â€¢': '•'
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def build_site():
    print(f"Starting SSG Build in {ROOT_DIR}...")
    
    # Load data
    g_data = load_json('global.json')
    c_data = load_json('contact.json')
    
    # Global fallbacks
    soc = g_data.get('social', {})
    cp = c_data.get('contacto_principal', {})
    dir_info = c_data.get('direccion', {})
    
    phone1 = cp.get('telefono_1') or g_data.get('phone_primary') or '+51 901 525 679'
    email = cp.get('email') or g_data.get('email') or 'discover@manujungleforever.com'
    wa_num = (cp.get('whatsapp') or g_data.get('whatsapp_number') or '51901525679')
    wa_num_clean = ''.join(filter(str.isdigit, wa_num))
    wa_txt = urllib.parse.quote(cp.get('whatsapp_texto') or g_data.get('whatsapp_text') or 'Hello! I would like to learn more about your jungle trips')
    wa_link = f"https://api.whatsapp.com/send?phone={wa_num_clean}&text={wa_txt}"
    wa_direct = f"https://wa.me/{wa_num_clean}"
    
    addr_parts = []
    if dir_info.get('nombre'): addr_parts.append(dir_info['nombre'])
    sub_parts = [dir_info.get('calle'), dir_info.get('localidad'), dir_info.get('pais')]
    sub_parts = [p for p in sub_parts if p]
    if sub_parts: addr_parts.append(', '.join(sub_parts))
    address_text = ', '.join(addr_parts) or g_data.get('address') or 'Manu Jungle Forever 17800, Nuevo Eden, Peru'
    maps_url = dir_info.get('maps_url') or g_data.get('address_maps_url') or 'https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc'

    # Find all HTML files
    html_files = glob.glob(os.path.join(ROOT_DIR, '**', '*.html'), recursive=True)
    
    for filepath in html_files:
        if 'admin' in filepath.replace('\\', '/') or 'api' in filepath.replace('\\', '/'):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # 1. Floating WhatsApp Button
        for el in soup.select('a.wa, #wa-float, a[id="wa-btn"]'):
            el['href'] = wa_link
            modified = True
            
        # 2. Sync all WhatsApp links
        for el in soup.select('a[href*="api.whatsapp.com"], a[href*="wa.me"]'):
            if 'sc' in el.get('class', []) or 'soc-btn' in el.get('class', []):
                el['href'] = wa_direct
            else:
                el['href'] = wa_link
            modified = True
            
        # 3. Footer sync
        footer = soup.select_one('footer.ft')
        if footer:
            addr_a = footer.select_one('address.fc a[href*="maps"]')
            if addr_a:
                addr_a.string = address_text
                addr_a['href'] = maps_url
                modified = True
                
            phone_a = footer.select_one('address.fc a[href^="tel:"]')
            if phone_a:
                phone_a.string = phone1
                phone_a['href'] = f"tel:{''.join([c for c in phone1 if c.isdigit() or c == '+'])}"
                modified = True
                
            email_a = footer.select_one('address.fc a[href^="mailto:"]')
            if email_a:
                email_a.string = email
                email_a['href'] = f"mailto:{email}"
                modified = True
                
            # Social links
            so = footer.select_one('.so')
            if so:
                def update_social(label, url):
                    nonlocal modified
                    a = so.select_one(f'a[aria-label="{label}"]')
                    if a and url:
                        a['href'] = url
                        modified = True
                        
                update_social("Facebook", soc.get('facebook'))
                update_social("Instagram", soc.get('instagram'))
                update_social("TripAdvisor", soc.get('tripadvisor'))
                update_social("Airbnb", soc.get('airbnb'))
                update_social("WhatsApp", wa_direct)
                update_social("TikTok", soc.get('tiktok'))

        # 4. Page specific hero updates
        # Assuming we don't know which page is which, we skip dynamic titles unless it's index or contact
        # For index.html:
        if filepath.endswith('index.html') and 'contact' not in filepath and 'about' not in filepath:
            h_data = load_json('home.json')
            if h_data.get('hero'):
                ht = soup.select_one('.hb .ht')
                if ht and h_data['hero'].get('location_tag'):
                    icon = soup.new_tag('i')
                    icon['class'] = ['fas', 'fa-map-marker-alt']
                    ht.clear()
                    ht.append(icon)
                    ht.append(f" {clean_mojibake(h_data['hero']['location_tag'])}")
                    modified = True
                
                h1 = soup.select_one('.hb .h1')
                if h1:
                    t = clean_mojibake(h_data['hero'].get('title', ''))
                    e = clean_mojibake(h_data['hero'].get('title_emphasis', ''))
                    if t.strip().lower() == 'what will' and 'you' not in e.lower():
                        t = 'What Will You'
                    html_content = f"{t}<br><em>{e}</em>" if e else t
                    h1_soup = BeautifulSoup(html_content, 'html.parser')
                    h1.clear()
                    for child in h1_soup.children:
                        h1.append(child)
                    modified = True
                    
                hs = soup.select_one('.hb .hs')
                if hs and h_data['hero'].get('subtitle'):
                    hs.string = clean_mojibake(h_data['hero']['subtitle'])
                    modified = True

            if h_data.get('guided_tours'):
                th = h_data['guided_tours']
                if th.get('title'):
                    ey = soup.select_one('#tours .tr-intro .ey')
                    if ey: ey.string = clean_mojibake(th['title']); modified = True
                if th.get('subtitle'):
                    t = soup.select_one('#tours .tr-intro .h2')
                    if t: t.string = clean_mojibake(th['subtitle']); modified = True
                if th.get('description'):
                    d = soup.select_one('#tours .tr-intro .ld')
                    if d: d.string = clean_mojibake(th['description']); modified = True

                cats = th.get('categories', [])
                if cats:
                    # XL Card
                    xl = soup.select_one('#tours .tc-xl')
                    if xl and len(cats) > 0:
                        c0 = cats[0]
                        if c0.get('imagen'):
                            img = xl.select_one('img')
                            if img:
                                img['src'] = fix_img_path(c0['imagen'])
                                img['alt'] = clean_mojibake(c0.get('imagen_alt') or c0.get('titulo', ''))
                        tbg = xl.select_one('.tbg')
                        if tbg:
                            avail = c0.get('disponible', True)
                            tbg['class'] = ['tbg', 'ton' if avail else 'tof']
                            tbg_soup = BeautifulSoup(f"<i class='fas fa-{'circle' if avail else 'pause-circle'}' style='font-size:.5rem'></i> {clean_mojibake(c0.get('badge_texto') or ('Available Now' if avail else 'Temporarily Unavailable'))}", 'html.parser')
                            tbg.clear()
                            for child in tbg_soup.children: tbg.append(child)
                        tt = xl.select_one('.tt')
                        if tt and c0.get('titulo'): tt.string = clean_mojibake(c0['titulo'])
                        tm = xl.select_one('.tm')
                        if tm:
                            tm_soup = BeautifulSoup(f"<span><i class='far fa-calendar-alt'></i> {clean_mojibake(c0.get('duracion', ''))}</span><span><i class='fas fa-users'></i> {clean_mojibake(c0.get('pasajeros', ''))}</span><span><i class='fas fa-ship'></i> {clean_mojibake(c0.get('transporte', ''))}</span>", 'html.parser')
                            tm.clear()
                            for child in tm_soup.children: tm.append(child)
                        tp = xl.select_one('.tp')
                        if tp and c0.get('descripcion'): tp.string = clean_mojibake(c0['descripcion'])
                        tbtn = xl.select_one('.tbtn')
                        if tbtn:
                            if c0.get('boton_texto'):
                                btn_soup = BeautifulSoup(f"{clean_mojibake(c0['boton_texto'])} <i class='fas fa-arrow-right'></i>", 'html.parser')
                                tbtn.clear()
                                for child in btn_soup.children: tbtn.append(child)
                            if c0.get('enlace'): tbtn['href'] = c0['enlace']
                        modified = True

                    # MD Cards
                    md_cards = soup.select('#tours .tr-right-col .tc-md')
                    for i, md in enumerate(md_cards):
                        if i + 1 < len(cats):
                            cat = cats[i + 1]
                            if cat.get('imagen'):
                                img = md.select_one('img')
                                if img:
                                    img['src'] = fix_img_path(cat['imagen'])
                                    img['alt'] = clean_mojibake(cat.get('imagen_alt') or cat.get('titulo', ''))
                            tbg = md.select_one('.tbg')
                            if tbg:
                                avail = cat.get('disponible', True)
                                tbg['class'] = ['tbg', 'ton' if avail else 'tof']
                                tbg_soup = BeautifulSoup(f"<i class='fas fa-{'circle' if avail else 'pause-circle'}' style='font-size:.5rem'></i> {clean_mojibake(cat.get('badge_texto') or ('Available Now' if avail else 'Temporarily Unavailable'))}", 'html.parser')
                                tbg.clear()
                                for child in tbg_soup.children: tbg.append(child)
                            tt = md.select_one('.tt')
                            if tt and cat.get('titulo'): tt.string = clean_mojibake(cat['titulo'])
                            tm = md.select_one('.tm')
                            if tm:
                                is_truck = '4x4' in cat.get('transporte', '').lower() or '4' in cat.get('transporte', '')
                                tm_soup = BeautifulSoup(f"<span><i class='far fa-calendar-alt'></i> {clean_mojibake(cat.get('duracion', ''))}</span><span><i class='fas fa-users'></i> {clean_mojibake(cat.get('pasajeros', ''))}</span><span><i class='fas fa-{'truck' if is_truck else 'hiking'}'></i> {clean_mojibake(cat.get('transporte', ''))}</span>", 'html.parser')
                                tm.clear()
                                for child in tm_soup.children: tm.append(child)
                            tbtn = md.select_one('.tbtn')
                            if tbtn:
                                if cat.get('boton_texto'):
                                    btn_soup = BeautifulSoup(f"{clean_mojibake(cat['boton_texto'])} <i class='fas fa-arrow-right'></i>", 'html.parser')
                                    tbtn.clear()
                                    for child in btn_soup.children: tbtn.append(child)
                                if cat.get('enlace'): tbtn['href'] = cat['enlace']
                            modified = True

                    # SM Cards
                    sm_cards = soup.select('#tours .tr-row .tc-sm')
                    if len(sm_cards) > 0 and len(cats) > 1:
                        c1 = cats[1]
                        h3 = sm_cards[0].select_one('h3')
                        p = sm_cards[0].select_one('p')
                        if h3 and c1.get('titulo'): h3.string = clean_mojibake(c1['titulo'] + ' · Details')
                        if p and c1.get('descripcion'): p.string = clean_mojibake(c1['descripcion'])
                        modified = True
                    if len(sm_cards) > 1 and len(cats) > 2:
                        c2 = cats[2]
                        h3 = sm_cards[1].select_one('h3')
                        p = sm_cards[1].select_one('p')
                        if h3 and c2.get('titulo'): h3.string = clean_mojibake(c2['titulo'] + ' · Details')
                        if p and c2.get('descripcion'): p.string = clean_mojibake(c2['descripcion'])
                        modified = True

            if h_data.get('about'):
                ab = h_data['about']
                if ab.get('eyebrow'):
                    ey = soup.select_one('#about .ey')
                    if ey: ey.string = clean_mojibake(ab['eyebrow']); modified = True
                if ab.get('title'):
                    t = soup.select_one('#about .h2')
                    if t: t.string = clean_mojibake(ab['title']); modified = True
                if ab.get('paragraphs'):
                    spt = soup.select_one('#about .spt')
                    if spt:
                        # Clear old paragraphs except the button
                        btn = spt.select_one('a.btn')
                        btn_html = str(btn) if btn else ''
                        p_html = ''.join([f"<p class='ld'>{clean_mojibake(p)}</p>" for p in ab['paragraphs']])
                        spt_soup = BeautifulSoup(p_html + btn_html, 'html.parser')
                        spt.clear()
                        for c in spt_soup.children: spt.append(c)
                        modified = True
                if ab.get('image_alt'):
                    img = soup.select_one('#about .spi img')
                    if img: img['alt'] = clean_mojibake(ab['image_alt']); img['title'] = clean_mojibake(ab['image_alt']); modified = True
                if ab.get('image_caption'):
                    cap = soup.select_one('#about .spi .caption-text')
                    if cap: cap.string = clean_mojibake(ab['image_caption']); modified = True
                    
            if h_data.get('unique_section'):
                uq = h_data['unique_section']
                if uq.get('title') or uq.get('eyebrow'):
                    t = soup.select_one('#unique-content .spt h2')
                    if t: t.string = clean_mojibake(uq.get('title') or uq.get('eyebrow')); modified = True
                if uq.get('text'):
                    p = soup.select_one('#unique-content .spt p')
                    if p: p.string = clean_mojibake(uq['text']); modified = True
                if uq.get('image_alt'):
                    img = soup.select_one('#unique-content .spi img')
                    if img: img['alt'] = clean_mojibake(uq['image_alt']); img['title'] = clean_mojibake(uq['image_alt']); modified = True
                if uq.get('image_caption'):
                    cap = soup.select_one('#unique-content .spi .caption-text')
                    if cap: cap.string = clean_mojibake(uq['image_caption']); modified = True

            if h_data.get('wildlife_encounters'):
                wl = h_data['wildlife_encounters']
                if wl.get('eyebrow'):
                    ey = soup.select_one('#wildlife .ey')
                    if ey: ey.string = clean_mojibake(wl['eyebrow']); modified = True
                if wl.get('title'):
                    t = soup.select_one('#wildlife .h2')
                    if t: t.string = clean_mojibake(wl['title']); modified = True
                if wl.get('text'):
                    p = soup.select_one('#wildlife .lead')
                    if p: p.string = clean_mojibake(wl['text']); modified = True
                    
            if h_data.get('call_to_action'):
                cta = h_data['call_to_action']
                if cta.get('eyebrow'):
                    ey = soup.select_one('#plan-trip .ey')
                    if ey: ey.string = clean_mojibake(cta['eyebrow']); modified = True
                if cta.get('title'):
                    t = soup.select_one('#plan-trip .h2')
                    if t: t.string = clean_mojibake(cta['title']); modified = True
                if cta.get('text'):
                    p = soup.select_one('#plan-trip p.ld')
                    if p: p.string = clean_mojibake(cta['text']); modified = True
                    
            if h_data.get('pillars'):
                pil = h_data['pillars']
                if pil.get('eyebrow'):
                    ey = soup.select_one('#why-us .ey')
                    if ey: ey.string = clean_mojibake(pil['eyebrow']); modified = True
                if pil.get('title'):
                    t = soup.select_one('#why-us .h2')
                    if t: t.string = clean_mojibake(pil['title']); modified = True
                if pil.get('pillars') and isinstance(pil['pillars'], list):
                    pg = soup.select_one('#why-us .pg')
                    if pg:
                        html = ""
                        for p in pil['pillars']:
                            html += f'''<div class="pl r v">
                              <div class="pi"><i class="{p.get('icon', 'fas fa-leaf')}"></i></div>
                              <h3>{clean_mojibake(p.get('title', ''))}</h3>
                              <p>{clean_mojibake(p.get('text', ''))}</p>
                            </div>'''
                        pg_soup = BeautifulSoup(html, 'html.parser')
                        pg.clear()
                        for c in pg_soup.children: pg.append(c)
                        modified = True
        
        # Contact page specific
        if filepath.endswith('contact\\index.html') or filepath.endswith('contact/index.html'):
            if c_data.get('titulo_pagina'):
                h1 = soup.select_one('.in-hero .h1')
                if h1: h1.string = clean_mojibake(c_data['titulo_pagina'])
                modified = True
            if c_data.get('subtitulo_pagina'):
                hs = soup.select_one('.in-hero .hs')
                if hs: hs.string = clean_mojibake(c_data['subtitulo_pagina'])
                modified = True
            if c_data.get('hero_image') and 'placeholder.jpg' not in c_data['hero_image']:
                hero = soup.select_one('.in-hero')
                if hero: hero['style'] = f"background-image: url('{fix_img_path(c_data['hero_image'])}')"
                modified = True
                
            dyn_phones = soup.find(id='dyn-contact-phones')
            if dyn_phones:
                p_parts = []
                if phone1:
                    clean_p1 = ''.join([c for c in phone1 if c.isdigit() or c == '+'])
                    p_parts.append(f'<a href="tel:{clean_p1}">{phone1}</a>')
                
                phone2 = cp.get('telefono_2') or g_data.get('phone_secondary')
                wa_display = phone2 if phone2 else (f"+{wa_num_clean}" if wa_num_clean else "")
                if wa_display:
                    p_parts.append(f'<a href="{wa_link}" target="_blank" rel="noopener">{wa_display}</a>')
                
                p_html = ' <span class="sep" style="opacity:0.5; margin:0 6px;">/</span> '.join(p_parts)
                dyn_phones_soup = BeautifulSoup(p_html, 'html.parser')
                dyn_phones.clear()
                for child in dyn_phones_soup.children: dyn_phones.append(child)
                modified = True
                
            dyn_email = soup.find(id='dyn-contact-email')
            if dyn_email:
                dyn_email['href'] = f"mailto:{email}"
                dyn_email.string = email
                modified = True
                
            dyn_loc = soup.find(id='dyn-contact-location')
            if dyn_loc:
                if maps_url: dyn_loc['href'] = maps_url
                loc_html = ', '.join(addr_parts) if addr_parts else address_text
                dyn_loc.string = loc_html
                modified = True
                
            map_iframe = soup.select_one('.map-container iframe')
            if map_iframe and dir_info.get('maps_embed'):
                map_iframe['src'] = dir_info['maps_embed']
                modified = True
                
            hor = c_data.get('horario', {})
            dyn_hours = soup.find(id='dyn-contact-hours')
            if dyn_hours and (hor.get('dias') or hor.get('horas') or hor.get('nota')):
                h_parts = []
                if hor.get('dias') or hor.get('horas'):
                    h_parts.append(f"<strong>{hor.get('dias') or 'Monday – Sunday'}</strong>: {hor.get('horas') or '8:00 AM – 8:00 PM (Peru Time)'}")
                if hor.get('nota'):
                    h_parts.append(f'<span style="font-size:0.82rem;color:rgba(255,255,255,0.6)">{hor.get("nota")}</span>')
                hours_soup = BeautifulSoup('<br>'.join(h_parts), 'html.parser')
                dyn_hours.clear()
                for child in hours_soup.children: dyn_hours.append(child)
                modified = True

            # Contact social row
            sr = soup.select_one('.social-row')
            if sr:
                def update_social_c(label, url):
                    a = sr.select_one(f'a[aria-label="{label}"]')
                    if a and url: a['href'] = url
                update_social_c("Facebook", soc.get('facebook'))
                update_social_c("Instagram", soc.get('instagram'))
                update_social_c("TripAdvisor", soc.get('tripadvisor'))
                update_social_c("Airbnb", soc.get('airbnb'))
                update_social_c("WhatsApp", wa_link)
                update_social_c("TikTok", soc.get('tiktok'))
                modified = True
                
        # Write changes back
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {os.path.relpath(filepath, ROOT_DIR)}")
            
    print("Build complete.")

if __name__ == '__main__':
    build_site()
