import glob, json, os, re

# 1. Update data/global.json
global_path = 'www.manujungleforever.com/data/global.json'
if os.path.exists(global_path):
    with open(global_path, 'r', encoding='utf-8') as f:
        gdata = json.load(f)

    gdata['address'] = "Manu Jungle Forever 17800, Nuevo Eden, Peru"
    gdata['address_maps_url'] = "https://maps.google.com/?q=Nuevo+Eden,+Madre+de+Dios,+Peru"
    
    clean_social = {
        "facebook": "https://www.facebook.com/manujungleforever",
        "instagram": "https://www.instagram.com/manujungleforever/",
        "tripadvisor": "#",
        "airbnb": "#",
        "whatsapp": "https://wa.me/51901525679",
        "tiktok": "#",
        "youtube": "https://www.youtube.com/@manujungleforever"
    }
    gdata['social'] = clean_social
    gdata['redes_sociales'] = {
        "facebook": clean_social["facebook"],
        "instagram": clean_social["instagram"],
        "tripadvisor": clean_social["tripadvisor"],
        "airbnb": clean_social["airbnb"],
        "whatsapp": clean_social["whatsapp"],
        "tiktok": clean_social["tiktok"]
    }

    with open(global_path, 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=2, ensure_ascii=False)
    print("Purged global.json")

# 2. Update data/contact.json
contact_path = 'www.manujungleforever.com/data/contact.json'
if os.path.exists(contact_path):
    with open(contact_path, 'r', encoding='utf-8') as f:
        cdata = json.load(f)

    cdata['contacto_principal'] = {
        "email": "discover@manujungleforever.com",
        "telefono_1": "+51 931 022 183",
        "telefono_2": "+51 901 525 679",
        "whatsapp": "51901525679",
        "whatsapp_texto": "Hello! I would like to learn more about your jungle trips"
    }
    cdata['direccion'] = {
        "nombre": "Manu Jungle Forever",
        "calle": "17800",
        "localidad": "Nuevo Eden",
        "pais": "Peru",
        "maps_url": "https://maps.google.com/?q=Nuevo+Eden,+Madre+de+Dios,+Peru",
        "maps_embed": "https://www.google.com/maps?q=Nuevo+Eden,+Madre+de+Dios,+Peru&output=embed"
    }

    with open(contact_path, 'w', encoding='utf-8') as f:
        json.dump(cdata, f, indent=2, ensure_ascii=False)
    print("Purged contact.json")

# 3. Update config.php
config_path = 'www.manujungleforever.com/config.php'
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        cc = f.read()
    cc = cc.replace('Fitzcarrald 17800, Nuevo Eden, Peru', 'Manu Jungle Forever 17800, Nuevo Eden, Peru')
    cc = cc.replace("define('SOCIAL_TRIPADVISOR', 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905');", "define('SOCIAL_TRIPADVISOR', '#');")
    cc = cc.replace("define('SOCIAL_TIKTOK',      'https://www.tiktok.com/@hidden.jungle.cus');", "define('SOCIAL_TIKTOK',      '#');")
    cc = cc.replace("https://goo.gl/maps/B8NjhLZizA6YKwKD6", "https://maps.google.com/?q=Nuevo+Eden,+Madre+de+Dios,+Peru")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(cc)
    print("Purged config.php")

# 4. Update _headers and functions
headers_path = 'www.manujungleforever.com/_headers'
if os.path.exists(headers_path):
    with open(headers_path, 'r', encoding='utf-8') as f:
        hc = f.read()
    hc = hc.replace('https://hiddenjunglecusco-2jc.pages.dev', 'https://manujungleforever.pages.dev')
    with open(headers_path, 'w', encoding='utf-8') as f:
        f.write(hc)

auth_func = 'functions/api/auth/index.js'
if os.path.exists(auth_func):
    with open(auth_func, 'r', encoding='utf-8') as f:
        af = f.read()
    af = af.replace('https://hiddenjunglecusco-2jc.pages.dev', 'https://manujungleforever.pages.dev')
    af = af.replace('https://www.hiddenjunglecusco.com', 'https://www.manujungleforever.com')
    with open(auth_func, 'w', encoding='utf-8') as f:
        f.write(af)

# 5. Update ALL public HTML files
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if '/admin/' not in f.replace('\\', '/')]

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Address fix
    c = c.replace('Fitzcarrald 17800, Nuevo Eden, Peru', 'Manu Jungle Forever 17800, Nuevo Eden, Peru')
    c = c.replace('Manu Jungle Forever – La Casa Escondida<br>Fitzcarrald 17800, Nuevo Eden, Peru', 'Manu Jungle Forever<br>17800, Nuevo Eden, Peru')

    # Maps links fix
    c = c.replace('https://goo.gl/maps/B8NjhLZizA6YKwKD6', 'https://maps.google.com/?q=Nuevo+Eden,+Madre+de+Dios,+Peru')
    c = c.replace('https://www.google.com/maps/d/embed?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc', 'https://www.google.com/maps?q=Nuevo+Eden,+Madre+de+Dios,+Peru&output=embed')

    # Purge hiddenjungle links
    c = c.replace('https://www.hiddenjunglecusco.com?utm_source=chatgpt.com', 'https://www.manujungleforever.com/')
    c = c.replace('https://www.hiddenjunglecusco.com/', 'https://www.manujungleforever.com/')
    c = c.replace('https://www.hiddenjunglecusco.com', 'https://www.manujungleforever.com')
    c = c.replace('https://www.tiktok.com/@hidden.jungle.cus', '#')
    c = c.replace('https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905', '#')

    # Replace legacy HiddenJungle image names in HTML with clean paths
    c = c.replace('HiddenJungleCusco_Sliders2.jpg', 'placeholder.jpg')
    c = c.replace('wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg', 'assets/img/hero.png')
    c = c.replace('../wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg', '../assets/img/hero.png')
    c = c.replace('amazon-lake-sunset-hidden-jungle-cusco.jpg', 'hero.png')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Purged all hiddenjungle references & fixed address/maps across all {len(html_files)} HTML files.")
