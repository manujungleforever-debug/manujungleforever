import glob, re

def update_pdf_export(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update drawBadge max width and dimensions
    old_draw_badge = """    function drawBadge(doc, text, x, y, bgColor, textColor) {
      const pad = 1.2;
      doc.setFontSize(6.0);
      const tw = doc.getTextWidth(text);
      const bw = Math.min(tw + pad * 2 + 0.6, 21);
      const bh = 3.6;
      doc.setFillColor(...bgColor);
      doc.roundedRect(x, y - bh + 0.8, bw, bh, 0.8, 0.8, 'F');
      doc.setTextColor(...textColor);
      doc.setFont(undefined, 'bold');
      doc.text(text, x + pad + 0.3, y - 0.4, { maxWidth: bw - 1 });
      return bw + 1;
    }"""

    new_draw_badge = """    function drawBadge(doc, text, x, y, bgColor, textColor, maxBadgeW = 39) {
      const pad = 1.5;
      doc.setFontSize(6.2);
      const tw = doc.getTextWidth(text);
      const bw = Math.min(tw + pad * 2 + 0.8, maxBadgeW);
      const bh = 4.2;
      doc.setFillColor(...bgColor);
      doc.roundedRect(x, y - bh + 1.0, bw, bh, 1.0, 1.0, 'F');
      doc.setTextColor(...textColor);
      doc.setFont(undefined, 'bold');
      doc.text(text, x + pad + 0.4, y - 0.2, { maxWidth: bw - 1.2 });
      return bw + 1;
    }"""

    if old_draw_badge in content:
        content = content.replace(old_draw_badge, new_draw_badge)

    # 2. Update columnStyles: Increase column 5 (Dieta / Salud) from 23 to 42
    old_col_styles = """      columnStyles: {
        0: { cellWidth: 7, halign: 'center', fontStyle: 'bold', textColor: [13, 148, 136] },
        1: { cellWidth: 14, minCellHeight: 12, halign: 'center' },
        2: { cellWidth: 42, fontStyle: 'bold' },
        3: { cellWidth: 34 },
        4: { cellWidth: 24, halign: 'center' },
        5: { cellWidth: 23 },
        6: { cellWidth: 38 }
      },"""

    new_col_styles = """      columnStyles: {
        0: { cellWidth: 7, halign: 'center', fontStyle: 'bold', textColor: [13, 148, 136] },
        1: { cellWidth: 14, minCellHeight: 13, halign: 'center' },
        2: { cellWidth: 36, fontStyle: 'bold' },
        3: { cellWidth: 26 },
        4: { cellWidth: 20, halign: 'center' },
        5: { cellWidth: 42, minCellHeight: 13 },
        6: { cellWidth: 37 }
      },"""

    if old_col_styles in content:
        content = content.replace(old_col_styles, new_col_styles)

    # 3. Also adjust vertical positioning in didDrawCell for col 5
    old_badges_pos = """            if (hasDieta && hasMedica) {
              drawBadge(doc, dieta, curX, curY - 1.2, [251, 191, 36], [120, 53, 15]);
              drawBadge(doc, medica, curX, curY + 3.4, [204, 241, 236], [15, 118, 110]);
            } else if (hasDieta) {
              drawBadge(doc, dieta, curX, curY + 1.2, [251, 191, 36], [120, 53, 15]);
            } else {
              drawBadge(doc, medica, curX, curY + 1.2, [204, 241, 236], [15, 118, 110]);
            }"""

    new_badges_pos = """            if (hasDieta && hasMedica) {
              drawBadge(doc, dieta, curX, curY - 1.6, [251, 191, 36], [120, 53, 15], 39);
              drawBadge(doc, medica, curX, curY + 3.8, [204, 241, 236], [15, 118, 110], 39);
            } else if (hasDieta) {
              drawBadge(doc, dieta, curX, curY + 1.2, [251, 191, 36], [120, 53, 15], 39);
            } else {
              drawBadge(doc, medica, curX, curY + 1.2, [204, 241, 236], [15, 118, 110], 39);
            }"""

    if old_badges_pos in content:
        content = content.replace(old_badges_pos, new_badges_pos)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated PDF table column widths in {file_path}")

for p in ['admin/gestionar-salidas.html', 'www.manujungleforever.com/admin/gestionar-salidas.html']:
    update_pdf_export(p)
