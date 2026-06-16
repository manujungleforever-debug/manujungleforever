import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'www.hiddenjunglecusco.com/admin/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update SECTIONS array
old_sections = """const SECTIONS = [
  { id:'blog',    label:'✍️ Blog',       sub:[] },
  { id:'content', label:'📄 Contenido',  sub:[
    {id:'home',    label:'🏠 Inicio'},
    {id:'contact', label:'📞 Contacto'},
    {id:'global',  label:'⚙️ Datos Globales'},
  ]},"""

new_sections = """const SECTIONS = [
  { id:'blog',    label:'✍️ Blog',       sub:[] },
  { id:'content', label:'📄 Contenido',  sub:[
    {id:'home',    label:'🏠 Inicio'},
    {id:'about',   label:'ℹ️ Sobre Nosotros'},
    {id:'contact', label:'📞 Contacto'},
    {id:'global',  label:'⚙️ Datos Globales'},
  ]},"""
text = text.replace(old_sections, new_sections)

# 2. Update the router to include 'about'
old_route = "const views = {blog:viewBlog,home:viewHome,contact:viewContact,global:viewGlobal,\n      tours:viewTours,departures:viewDeps,testimonials:viewTestims, media:viewMedia};"
new_route = "const views = {blog:viewBlog,home:viewHome,about:viewAbout,contact:viewContact,global:viewGlobal,\n      tours:viewTours,departures:viewDeps,testimonials:viewTestims, media:viewMedia};"
text = text.replace(old_route, new_route)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Admin SECTIONS and Router updated.")
