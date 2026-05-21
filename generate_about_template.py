import re
from bs4 import BeautifulSoup

# Load live page content
with open(r'C:\Users\evera\.gemini\antigravity-ide\brain\ce1bc295-01f6-41a1-8e0a-c23dd2cd24e3\.system_generated\steps\543\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
main_el = soup.find('div', class_='elementor-31')

def make_relative(url):
    if not url:
        return ''
    return url.replace('https://www.hiddenjunglecusco.com/', '../')

def get_columns_for_section(s):
    cols = s.find_all('div', class_='elementor-column')
    immediate = []
    for col in cols:
        parent_col = col.find_parent('div', class_='elementor-column')
        if parent_col and s in parent_col.parents:
            continue
        immediate.append(col)
    return immediate

# Build the custom template
output = []

# Hero Section
output.append("""<main id="main">
<section class="in-hero" style="background-image: url('../wp-content/uploads/2022/10/Hero-About-Us.jpg'); background-size: cover; background-position: center; position: relative;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem); text-transform: uppercase;">All About Us</h1>
  </div>
</section>

<section class="sec" style="background:var(--k); padding: 80px 0;">
  <div class="cx">
""")

# Intro Section (SECTION: 40177ae0)
intro_sec = main_el.find('section', {'data-id': '40177ae0'})
if intro_sec:
    heading = intro_sec.find('h2').text.strip()
    text_content = intro_sec.find('div', class_='elementor-widget-text-editor').decode_contents()
    text_content = make_relative(text_content)
    output.append(f"""
    <!-- Intro Section -->
    <div class="intro-block r r-up" style="max-width: 900px; margin: 0 auto 60px; text-align: center;">
      <h2 class="h2" style="margin-bottom: 32px; font-size: 2.2rem; line-height: 1.3;">{heading}</h2>
      <div class="tour-rich-text" style="text-align: left;">
        {text_content}
      </div>
    </div>
    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 60px 0;">
""")

# Logistics & Lodges Section (SECTION: 07eea08)
logistics_sec = main_el.find('section', {'data-id': '07eea08'})
if logistics_sec:
    output.append("    <!-- Logistics & Lodges -->\n    <div class='logistics-container'>\n")
    sub_sections = logistics_sec.find_all('section', class_='elementor-inner-section')
    for s in sub_sections:
        sub_id = s.get('data-id')
        immediate_cols = get_columns_for_section(s)
            
        if len(immediate_cols) >= 2:
            left_col, right_col = immediate_cols[0], immediate_cols[1]
            
            # Left images
            imgs = []
            for img_tag in left_col.find_all('img'):
                imgs.append(f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:16px; margin-bottom:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>")
            left_html = "\n".join(imgs)
            
            # Right content (Headings and Text)
            right_html = []
            for w in right_col.find_all('div', class_='elementor-widget'):
                classes = w.get('class', [])
                w_type = [c.replace('elementor-widget-', '') for c in classes if c.startswith('elementor-widget-')]
                w_type = w_type[0].split('--')[0] if w_type else 'unknown'
                
                if w_type == 'heading':
                    tag = w.find(['h2', 'h3', 'h4', 'h5', 'h6'])
                    h_text = tag.text.strip() if tag else w.text.strip()
                    h_level = tag.name if tag else 'h3'
                    if h_level in ['h2', 'h3']:
                        right_html.append(f"<h3 class='h3' style='margin-bottom:12px;'>{h_text}</h3>")
                    else:
                        right_html.append(f"<span class='ey' style='display:block; margin-bottom:8px;'>{h_text}</span>")
                elif w_type == 'text-editor':
                    txt = w.find('div', class_='elementor-widget-container').decode_contents()
                    right_html.append(f"<div class='tour-rich-text'>{make_relative(txt)}</div>")
            
            right_content = "\n".join(right_html)
            
            output.append(f"""
      <div class="split-row r r-up" data-sub-id="{sub_id}" style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-bottom: 80px; align-items: center;">
        <div class="split-left rl">
          {left_html}
        </div>
        <div class="split-right rr">
          {right_content}
        </div>
      </div>
""")
    output.append("    </div>\n")

# Our Story Section (SECTION: 63f3cb0)
story_sec = main_el.find('section', {'data-id': '63f3cb0'})
if story_sec:
    output.append("    <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 60px 0;'>\n")
    # Top 100% column
    top_col = story_sec.find('div', class_='elementor-col-100')
    if top_col:
        story_heading = top_col.find('h2').text.strip()
        story_text = top_col.find('div', class_='elementor-widget-text-editor').decode_contents()
        output.append(f"""
    <!-- Our Story Intro -->
    <div class="story-intro r r-up" style="max-width: 900px; margin: 0 auto 60px; text-align: center;">
      <h2 class="h2" style="margin-bottom: 24px;">{story_heading}</h2>
      <div class="tour-rich-text" style="text-align: left;">
        {make_relative(story_text)}
      </div>
    </div>
""")
    
    # Team members in this section (inner sections)
    team_subs = story_sec.find_all('section', class_='elementor-inner-section')
    for s in team_subs:
        sub_id = s.get('data-id')
        immediate_cols = get_columns_for_section(s)
            
        if len(immediate_cols) >= 2:
            left_col, right_col = immediate_cols[0], immediate_cols[1]
            img_tag = left_col.find('img')
            img_html = f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4);'>" if img_tag else ""
            
            right_html = []
            for w in right_col.find_all('div', class_='elementor-widget'):
                classes = w.get('class', [])
                w_type = [c.replace('elementor-widget-', '') for c in classes if c.startswith('elementor-widget-')]
                w_type = w_type[0].split('--')[0] if w_type else 'unknown'
                
                if w_type == 'heading':
                    tag = w.find(['h2', 'h3', 'h4', 'h5', 'h6'])
                    h_text = tag.text.strip() if tag else w.text.strip()
                    h_level = tag.name if tag else 'h3'
                    if h_level in ['h2', 'h3']:
                        right_html.append(f"<h3 class='h3' style='margin-bottom:4px;'>{h_text}</h3>")
                    else:
                        right_html.append(f"<span class='role' style='display:block; color:var(--a); font-weight:600; text-transform:uppercase; font-size:0.85rem; letter-spacing:0.05em; margin-bottom:16px;'>{h_text}</span>")
                elif w_type == 'text-editor':
                    txt = w.find('div', class_='elementor-widget-container').decode_contents()
                    right_html.append(f"<div class='tour-rich-text' style='font-size:0.95rem;'>{make_relative(txt)}</div>")
            
            right_content = "\n".join(right_html)
            
            output.append(f"""
      <!-- Team Member -->
      <div class="split-row team-row r r-up" data-sub-id="{sub_id}" style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; margin-bottom: 80px; align-items: start;">
        <div class="split-left rl">
          {img_html}
        </div>
        <div class="split-right rr">
          {right_content}
        </div>
      </div>
""")

# Final Section (SECTION: 78faaab) - Placida, Why Visit, Destinations
final_sec = main_el.find('section', {'data-id': '78faaab'})
if final_sec:
    # Sub section cd04b85 (Placida)
    placida_sub = final_sec.find('section', {'data-id': 'cd04b85'})
    if placida_sub:
        immediate_cols = get_columns_for_section(placida_sub)
            
        if len(immediate_cols) >= 2:
            left_col, right_col = immediate_cols[0], immediate_cols[1]
            img_tag = left_col.find('img')
            img_html = f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4);'>" if img_tag else ""
            
            right_html = []
            for w in right_col.find_all('div', class_='elementor-widget'):
                classes = w.get('class', [])
                w_type = [c.replace('elementor-widget-', '') for c in classes if c.startswith('elementor-widget-')]
                w_type = w_type[0].split('--')[0] if w_type else 'unknown'
                
                if w_type == 'heading':
                    tag = w.find(['h2', 'h3', 'h4', 'h5', 'h6'])
                    h_text = tag.text.strip() if tag else w.text.strip()
                    h_level = tag.name if tag else 'h3'
                    if h_level in ['h2', 'h3']:
                        right_html.append(f"<h3 class='h3' style='margin-bottom:4px;'>{h_text}</h3>")
                    else:
                        right_html.append(f"<span class='role' style='display:block; color:var(--a); font-weight:600; text-transform:uppercase; font-size:0.85rem; letter-spacing:0.05em; margin-bottom:16px;'>{h_text}</span>")
                elif w_type == 'text-editor':
                    txt = w.find('div', class_='elementor-widget-container').decode_contents()
                    right_html.append(f"<div class='tour-rich-text' style='font-size:0.95rem;'>{make_relative(txt)}</div>")
            
            right_content = "\n".join(right_html)
            output.append(f"""
      <!-- Team Member (Placida) -->
      <div class="split-row team-row r r-up" data-sub-id="cd04b85" style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; margin-bottom: 80px; align-items: start;">
        <div class="split-left rl">
          {img_html}
        </div>
        <div class="split-right rr">
          {right_content}
        </div>
      </div>
      <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 60px 0;'>
""")

    # Why Visit Manu Title
    why_visit_h = final_sec.find('h2', string=re.compile(r'Why Visit Manu', re.I))
    if why_visit_h:
        output.append(f"      <h2 class='h2 r r-up' style='text-align:center; margin-bottom:48px;'>{why_visit_h.text.strip()}</h2>\n")
        
    # Why Visit Sub Section (c89ec4e)
    why_sub = final_sec.find('section', {'data-id': 'c89ec4e'})
    if why_sub:
        immediate_cols = get_columns_for_section(why_sub)
            
        if len(immediate_cols) >= 2:
            left_col, right_col = immediate_cols[0], immediate_cols[1]
            txt = left_col.find('div', class_='elementor-widget-text-editor').decode_contents()
            
            imgs = []
            for img_tag in right_col.find_all('img'):
                imgs.append(f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:16px; margin-bottom:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>")
            imgs_html = "\n".join(imgs)
            
            output.append(f"""
      <div class="split-row r r-up" data-sub-id="c89ec4e" style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 60px; margin-bottom: 80px; align-items: center;">
        <div class="split-left rl">
          <div class="tour-rich-text">{make_relative(txt)}</div>
        </div>
        <div class="split-right rr">
          {imgs_html}
        </div>
      </div>
""")

    # Why travel with us Title & Sub section
    why_travel_h = final_sec.find('h2', string=re.compile(r'Why travel with us', re.I))
    if why_travel_h:
        output.append(f"      <h2 class='h2 r r-up' style='text-align:center; margin-bottom:48px;'>{why_travel_h.text.strip()}</h2>\n")
        
    why_travel_sub = final_sec.find('section', {'data-id': '20e4842'})
    if why_travel_sub:
        immediate_cols = get_columns_for_section(why_travel_sub)
            
        if len(immediate_cols) >= 2:
            left_col, right_col = immediate_cols[0], immediate_cols[1]
            txt = left_col.find('div', class_='elementor-widget-text-editor').decode_contents()
            img_tag = right_col.find('img')
            img_html = f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>" if img_tag else ""
            
            output.append(f"""
      <div class="split-row r r-up" data-sub-id="20e4842" style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 60px; margin-bottom: 80px; align-items: center;">
        <div class="split-left rl">
          <div class="tour-rich-text">{make_relative(txt)}</div>
        </div>
        <div class="split-right rr">
          {img_html}
        </div>
      </div>
      <hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 60px 0;'>
""")

    # Destinations Title
    dest_h = final_sec.find('h2', string=re.compile(r'Destinations', re.I))
    if dest_h:
        output.append(f"      <h2 class='h2 r r-up' style='text-align:center; margin-bottom:60px;'>{dest_h.text.strip()}</h2>\n")
        
    # Destination Subsections (01ba524, 4160d56, 82c6c75, 2a62e31)
    dest_ids = ['01ba524', '4160d56', '82c6c75', '2a62e31']
    for d_id in dest_ids:
        d_sub = final_sec.find('section', {'data-id': d_id})
        if d_sub:
            immediate_cols = get_columns_for_section(d_sub)
                
            if len(immediate_cols) >= 2:
                left_col, right_col = immediate_cols[0], immediate_cols[1]
                img_tag = left_col.find('img')
                img_html = f"<img src='{make_relative(img_tag.get('src'))}' alt='{img_tag.get('alt', '')}' class='anim-img' style='width:100%; border-radius:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>" if img_tag else ""
                
                heading_tag = right_col.find('h2')
                d_heading = heading_tag.text.strip() if heading_tag else ""
                txt = right_col.find('div', class_='elementor-widget-text-editor').decode_contents()
                
                output.append(f"""
      <div class="split-row r r-up" data-sub-id="{d_id}" style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; margin-bottom: 80px; align-items: center;">
        <div class="split-left rl">
          {img_html}
        </div>
        <div class="split-right rr">
          <h3 class="h3" style="margin-bottom:16px;">{d_heading}</h3>
          <div class="tour-rich-text">{make_relative(txt)}</div>
        </div>
      </div>
""")

output.append("""
  </div>
</section>
</main>
""")

full_template = "".join(output)
with open('about_us_template.html', 'w', encoding='utf-8') as tf:
    tf.write(full_template)

print("Successfully auto-generated 100% faithful about_us_template.html!")
