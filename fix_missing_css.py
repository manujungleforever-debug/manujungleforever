import os

base_dir = 'www.hiddenjunglecusco.com'

blog_folders = [
    'discovering-the-mysteries-of-the-peruvian-amazon',
    'amazon-rainforest-tour-to-manu-national-park-from-cusco',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026',
    'climate-change-manu-national-park-peru',
    'how-tourism-helps-the-manu-national-park',
    'everything-you-need-to-know-before-visiting-machu-picchu',
    'peru-travel-tips',
    'packing-list-for-your-trip-to-the-peruvian-amazon',
    'five-reasons-to-visit-manu-national-park',
    'ten-days-in-peru'
]

css_block = """
  /* Related posts */
  .related-posts { max-width: 820px; margin: 0 auto; padding: 0 24px 80px; }
  .related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 24px; }
  .related-card { background: var(--f); border: 1px solid rgba(255,255,255,.06); border-radius: 16px; overflow: hidden; text-decoration: none; transition: transform .3s, border-color .3s; display: block; }
  .related-card:hover { transform: translateY(-4px); border-color: rgba(201,168,76,.3); }
  .related-card img { width: 100%; height: 150px; object-fit: cover; }
  .related-card-body { padding: 16px 18px 20px; }
  .related-card-body h3 { font-family: 'Montserrat', sans-serif; font-size: .9rem; font-weight: 800; color: var(--w); line-height: 1.35; transition: color .3s; }
  .related-card:hover .related-card-body h3 { color: var(--a); }
  @media(max-width:768px) { .related-grid { grid-template-columns: 1fr 1fr; } }
  @media(max-width:480px) { .related-grid { grid-template-columns: 1fr; } }
"""

def fix_css(lang_prefix):
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '.related-grid {' not in content:
            # Inject right before </style>
            content = content.replace('</style>', css_block + '\n</style>', 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    print(f"Injected CSS into {updated} files in '{lang_prefix}'")

fix_css('')
fix_css('es')
