import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin\panel.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# 1. Replace the CSS for .btn-card-icon
css_old = r'''        .btn-card-icon {
            width: 68px;
            height: 68px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.9rem;
            flex-shrink: 0;
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #030807;
            box-shadow: 0 6px 20px rgba(45,212,191,0.35);
            transition: var(--transition);
        }

        .menu-btn-card:hover .btn-card-icon {
            transform: scale(1.08) rotate(-3deg);
            box-shadow: 0 8px 28px rgba(45,212,191,0.5);
        }

        .menu-btn-card.gold-style .btn-card-icon {
            background: linear-gradient(135deg, #ef4444, #b91c1c);
            color: #fff;
            box-shadow: 0 6px 20px rgba(239,68,68,0.35);
        }

        .menu-btn-card.gold-style:hover .btn-card-icon {
            box-shadow: 0 8px 28px rgba(239,68,68,0.5);
        }'''

css_new = r'''        .btn-card-icon {
            width: 68px;
            height: 68px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.9rem;
            flex-shrink: 0;
            transition: var(--transition);
            position: relative;
        }

        .menu-btn-card:hover .btn-card-icon {
            transform: scale(1.08) rotate(-3deg);
            filter: brightness(1.15);
        }

        .card-icon-tours { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; box-shadow: 0 6px 20px rgba(245,158,11,0.35); }
        .card-icon-blog { background: linear-gradient(135deg, #14b8a6, #0d9488); color: #fff; box-shadow: 0 6px 20px rgba(20,184,166,0.35); }
        .card-icon-testim { background: linear-gradient(135deg, #8b5cf6, #6d28d9); color: #fff; box-shadow: 0 6px 20px rgba(139,92,246,0.35); }
        .card-icon-reclamos { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; box-shadow: 0 6px 20px rgba(239,68,68,0.35); }
        .card-icon-contenido { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; box-shadow: 0 6px 20px rgba(59,130,246,0.35); }
        .card-icon-salidas { background: linear-gradient(135deg, #ec4899, #be185d); color: #fff; box-shadow: 0 6px 20px rgba(236,72,153,0.35); }
        .card-icon-medios { background: linear-gradient(135deg, #10b981, #059669); color: #fff; box-shadow: 0 6px 20px rgba(16,185,129,0.35); }'''

content = content.replace(css_old, css_new)

# 2. Update the HTML for each card
html_old_tours = r'<div class="btn-card-icon"><i class="ph ph-map-trifold"></i></div>'
html_new_tours = r'<div class="btn-card-icon card-icon-tours"><i class="ph ph-map-trifold"></i></div>'
content = content.replace(html_old_tours, html_new_tours)

html_old_blog = r'<div class="btn-card-icon"><i class="ph ph-pencil"></i></div>'
html_new_blog = r'<div class="btn-card-icon card-icon-blog"><i class="ph ph-pencil"></i></div>'
content = content.replace(html_old_blog, html_new_blog)

html_old_testim = r'<div class="btn-card-icon"><i class="ph ph-chat-circle-text"></i></div>'
html_new_testim = r'<div class="btn-card-icon card-icon-testim"><i class="ph ph-chat-circle-text"></i></div>'
content = content.replace(html_old_testim, html_new_testim)

# Fix the reclamos card which has gold-style
reclamos_old = r'''<div class="menu-btn-card gold-style" onclick="window.location.href='gestionar-reclamos.html'">
                    <div class="btn-card-icon"><i class="ph ph-scales"></i></div>'''
reclamos_new = r'''<div class="menu-btn-card" onclick="window.location.href='gestionar-reclamos.html'">
                    <div class="btn-card-icon card-icon-reclamos">
                        <i class="ph ph-scales"></i>
                        <span id="badge-reclamos-menu" style="display:none; position:absolute; top:-6px; right:-6px; background:#ef4444; color:#fff; border-radius:50%; width:24px; height:24px; font-size:12px; font-weight:800; align-items:center; justify-content:center; border:2px solid var(--card-bg); box-shadow:0 0 10px rgba(239,68,68,0.6); z-index:10;"></span>
                    </div>'''
content = content.replace(reclamos_old, reclamos_new)

html_old_contenido = r'<div class="btn-card-icon"><i class="ph ph-file-text"></i></div>'
html_new_contenido = r'<div class="btn-card-icon card-icon-contenido"><i class="ph ph-file-text"></i></div>'
content = content.replace(html_old_contenido, html_new_contenido)

html_old_salidas = r'<div class="btn-card-icon"><i class="ph ph-calendar"></i></div>'
html_new_salidas = r'<div class="btn-card-icon card-icon-salidas"><i class="ph ph-calendar"></i></div>'
content = content.replace(html_old_salidas, html_new_salidas)

html_old_medios = r'<div class="btn-card-icon"><i class="ph ph-image"></i></div>'
html_new_medios = r'<div class="btn-card-icon card-icon-medios"><i class="ph ph-image"></i></div>'
content = content.replace(html_old_medios, html_new_medios)

# 3. Add JS to update the badge
js_old = r'''                document.getElementById('stat-reclamos').textContent = pendingReclamos;
            } catch (e) {'''

js_new = r'''                document.getElementById('stat-reclamos').textContent = pendingReclamos;
                
                const badge = document.getElementById('badge-reclamos-menu');
                if (badge && pendingReclamos > 0) {
                    badge.textContent = pendingReclamos > 9 ? '+9' : pendingReclamos;
                    badge.style.display = 'flex';
                } else if (badge) {
                    badge.style.display = 'none';
                }
            } catch (e) {'''
content = content.replace(js_old, js_new)

# Also remove .menu-btn-card.gold-style CSS if it's there
css_gold_style = r'''        .menu-btn-card.gold-style:hover {
            border-color: var(--accent-gold);
            box-shadow: 0 15px 35px rgba(201, 168, 76, 0.08);
        }'''
content = content.replace(css_gold_style, "")

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)

