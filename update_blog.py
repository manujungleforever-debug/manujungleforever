import os

search_dir = 'www.hiddenjunglecusco.com'

reps = [
    (
        ".blog-grid {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);",
        ".blog-grid {\n    display: grid;\n    grid-template-columns: repeat(2, 1fr);"
    ),
    (
        ".blog-grid { display: grid; grid-template-columns: repeat(3, 1fr);",
        ".blog-grid { display: grid; grid-template-columns: repeat(2, 1fr);"
    ),
    (
        ".article-nav a { flex: 1; padding: 20px 24px; background: var(--f); border: 1px solid rgba(255,255,255,.06); border-radius: 16px; font-size: .88rem; color: rgba(255,255,255,.6); transition: all .3s; text-decoration: none; }",
        ".article-nav a { flex: 1; padding: 20px 24px; background: linear-gradient(145deg, rgba(201,168,76,.08) 0%, rgba(201,168,76,.02) 100%); border: 1px solid rgba(201,168,76,.25); border-radius: 16px; font-size: .88rem; color: rgba(255,255,255,.8); transition: all .3s; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,.2); }"
    ),
    (
        ".article-nav a:hover { border-color: rgba(201,168,76,.35); color: var(--a); transform: translateY(-3px); }",
        ".article-nav a:hover { border-color: rgba(201,168,76,.6); color: var(--w); transform: translateY(-3px); background: linear-gradient(145deg, rgba(201,168,76,.15) 0%, rgba(201,168,76,.05) 100%); box-shadow: 0 8px 24px rgba(201,168,76,.15); }"
    ),
    (
        ".article-nav .nav-label { font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: rgba(255,255,255,.28); margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }",
        ".article-nav .nav-label { font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: rgba(201,168,76,.8); margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }"
    )
]

updated_files = []
for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                new_content = content
                for old, new in reps:
                    new_content = new_content.replace(old, new)
                
                # Handling minified or varying whitespace for blog-grid just in case
                if "grid-template-columns: repeat(3, 1fr)" in new_content and ".blog-grid" in new_content:
                    lines = new_content.split('\n')
                    for i, line in enumerate(lines):
                        if ".blog-grid {" in line or ".blog-grid{" in line:
                            for j in range(i, min(i+5, len(lines))):
                                if "grid-template-columns:" in lines[j]:
                                    lines[j] = lines[j].replace("repeat(3, 1fr)", "repeat(2, 1fr)")
                                    lines[j] = lines[j].replace("repeat(3,1fr)", "repeat(2,1fr)")
                    new_content = '\n'.join(lines)

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    updated_files.append(path)
            except Exception as e:
                pass

print(f'Updated {len(updated_files)} files: {updated_files}')
