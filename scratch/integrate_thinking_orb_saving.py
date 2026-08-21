import glob, os, re

admin_dirs = ['admin', 'www.manujungleforever.com/admin']

for d in admin_dirs:
    for fpath in glob.glob(os.path.join(d, 'gestionar-*.html')) + glob.glob(os.path.join(d, 'index.html')) + glob.glob(os.path.join(d, 'panel.html')):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()

        # 1. Update btn-save click listener to show Thinking Orb overlay
        old_save_pattern = re.compile(
            r"document\.getElementById\('btn-save'\)\.addEventListener\('click',\s*async\s*\(\)\s*=>\s*\{[\s\S]*?\}\);",
            re.DOTALL
        )
        
        new_save_code = """document.getElementById('btn-save').addEventListener('click', async () => {
  if (!saveFnRef) return;
  const btn = document.getElementById('btn-save');
  const ss = document.getElementById('save-status');
  btn.disabled = true;
  if (window.showThinkingOverlay) window.showThinkingOverlay('Guardando cambios....');
  try {
    await saveFnRef();
    if (window.hideThinkingOverlay) window.hideThinkingOverlay();
    ss.textContent = 'Guardado correctamente';
    ss.className = 'save-status ok';
    btn.innerHTML = '<i class="ph ph-check-circle"></i> Guardado ✓';
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = '<i class="ph ph-floppy-disk"></i> Guardar cambios';
    }, 1500);
  } catch(e) {
    if (window.hideThinkingOverlay) window.hideThinkingOverlay();
    ss.textContent = 'Error: ' + e.message;
    ss.className = 'save-status err';
    btn.disabled = false;
    btn.innerHTML = '<i class="ph ph-floppy-disk"></i> Guardar cambios';
  }
});"""
        if old_save_pattern.search(c):
            c = old_save_pattern.sub(lambda m: new_save_code, c)

        # 2. In gestionar-tours.html: fix and optimize tour saving
        if 'gestionar-tours.html' in fpath:
            # Cleanly define sync in editTour
            opt_menu_sync = """async function syncGuidedToursMenuInPages(tours, pageList = MENU_PAGES_TO_SYNC) {
  const promises = pageList.map(async (pagePath) => {
    try {
      const pageData = await ghGet(pagePath);
      let content = pageData.content;
      const isSub = pagePath.split('/').length > 2;
      const { desktopHtml, mobileHtml } = buildGuidedToursMenu(tours, isSub);
      
      let modified = false;
      const dmRegex = /<ul class="dm">[\\s\\S]*?<\\/ul>/;
      const mddRegex = /<ul class="md" id="mdd">[\\s\\S]*?<\\/ul>/;
      
      if (dmRegex.test(content)) {
        content = content.replace(dmRegex, `<ul class="dm">${desktopHtml}\\n      </ul>`);
        modified = true;
      }
      if (mddRegex.test(content)) {
        content = content.replace(mddRegex, `<ul class="md" id="mdd">${mobileHtml}\\n      </ul>`);
        modified = true;
      }
      
      if (modified) {
        await ghPut(pagePath, content, pageData.sha, `update guided tours menu in ${pagePath.split('/').pop()}`);
      }
    } catch(e) {
      console.warn(`Could not sync menu in ${pagePath}:`, e);
    }
  });
  await Promise.allSettled(promises);
}"""
            c = re.sub(r"async function syncGuidedToursMenuInPages[\s\S]*?^\}", lambda m: opt_menu_sync, c, flags=re.MULTILINE)

            # Ensure editTour has clean save bar handler
            edit_tour_save = """    const res = await ghPut(cFile, JSON.stringify(cData, null, 2), cSha, `update tour: ${updated.nombre}`);
    cSha = res.sha;

    // Publish static HTML for this tour
    const slug = updated.slug;
    if (updated.estado === 'activo') {
      await publishTourPage(slug, updated);
    } else {
      await unpublishTourPage(slug);
    }

    // Synchronize departures linked to this tour in departures.json
    try {
      const depData = await ghGet('www.manujungleforever.com/data/departures.json');
      if (depData && depData.content) {
        const dJson = JSON.parse(depData.content);
        let depModified = false;
        (dJson.salidas || []).forEach(sal => {
          if (sal.tour_id === updated.id || sal.tour_id === updated.slug) {
            sal.tour_nombre = updated.nombre;
            sal.moneda = 'USD';
            sal.precio = updated.precio_desde;
            depModified = true;
          }
        });
        if (depModified) {
          await ghPut('www.manujungleforever.com/data/departures.json', JSON.stringify(dJson, null, 2), depData.sha, `sync departures price with tour: ${updated.nombre}`);
        }
      }
    } catch(err) {
      console.warn('Could not sync departures with tour price:', err);
    }"""
            
            # Replace the save logic in editTour
            c = re.sub(
                r"const res\s*=\s*await ghPut\(cFile,\s*JSON\.stringify\(cData,\s*null,\s*2\),\s*cSha,\s*`update tour: \$\{updated\.nombre\}`\);[\s\S]*?await syncGuidedToursMenuInPages\(cData\.tours,\s*MENU_PAGES_TO_SYNC\);",
                lambda m: edit_tour_save,
                c
            )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated Thinking Orb saving integration in {fpath}")

print("All admin files updated successfully.")
