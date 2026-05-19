import zipfile
import re
from bs4 import BeautifulSoup

z = zipfile.ZipFile('hts-cache/new.zip', 'r')
html = z.read('https://www.hiddenjunglecusco.com/about-2/')
soup = BeautifulSoup(html, 'html.parser')

template = open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8').read()

about_html = re.sub(r'<main id="main">.*?</main>', '''<main id="main">
<section class="in-hero" style="background-image: url('../wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg'); background-size: cover; background-position: center; position: relative;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">About Us</h1>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="tour-rich-text">
''' + soup.find('div', class_='elementor-widget-wrap').decode_contents() + '''
    </div>
  </div>
</section>
</main>''', template, flags=re.DOTALL)

# Fix paths for about-2 since it's 1 level deep
about_html = about_html.replace('href="', 'href="../').replace('src="', 'src="../')
# Fix the absolute paths that might have gotten double ../
about_html = about_html.replace('href="../http', 'href="http')
about_html = about_html.replace('src="../http', 'src="http')
# Fix the nav link
about_html = about_html.replace('href="../about-2/index.html"', 'href="index.html" class="on"')

# Remove any empty or malformed widgets
about_html = re.sub(r'https?://(www\.)?hiddenjunglecusco\.com/wp-content/', '../wp-content/', about_html)
about_html = re.sub(r'https?://(www\.)?hiddenjunglecusco\.com/?', '../', about_html)

open('www.hiddenjunglecusco.com/about-2/index.html', 'w', encoding='utf-8').write(about_html)

print("About-2 restored!")
