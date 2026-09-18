from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 378, 'height': 846})
    page.add_init_script("localStorage.setItem('mjf_loader_shown', '1');")
    page.goto('http://localhost:8089/manu-reserve-zone-to-blanquillo-macaw-clay-lick-8d-7n/', wait_until='domcontentloaded')
    page.wait_for_timeout(500)
    page.evaluate("const p = document.getElementById('preloader'); if(p) p.style.display='none';")
    
    overflow = page.evaluate("""() => {
        const innerW = window.innerWidth;
        const scrollW = document.documentElement.scrollWidth;
        const bodyW = document.body.scrollWidth;
        const overs = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > innerW + 1) {
                overs.push({
                    tag: el.tagName,
                    cls: el.className,
                    id: el.id,
                    right: Math.round(rect.right),
                    width: Math.round(rect.width),
                    text: (el.textContent || '').trim().slice(0, 30)
                });
            }
        });
        return { innerW, scrollW, bodyW, overs: overs.slice(0, 20) };
    }""")
    print('Overflow metrics:', overflow)
    page.screenshot(path='scratch/tour_378.png')
    browser.close()
