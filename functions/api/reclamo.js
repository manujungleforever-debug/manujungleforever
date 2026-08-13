import { PDFDocument, rgb, StandardFonts } from './pdf-lib.js';

// ─── Utilidades ──────────────────────────────────────────────────────────────
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json;charset=UTF-8',
};

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
const error = (msg, status = 400) => json({ ok: false, error: msg }, status);

async function generateReclamoPDF(data) {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([595.28, 841.89]); // A4
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const bold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
  const { width, height } = page.getSize();
  const marginX = 40;
  let y = height - 40;
  const W = width - 2 * marginX; // 515.28

  const drawBorder = (x, yPos, w, h) => page.drawRectangle({ x, y: yPos - h, width: w, height: h, borderColor: rgb(0,0,0), borderWidth: 0.5 });
  const drawBg = (x, yPos, w, h) => page.drawRectangle({ x, y: yPos - h, width: w, height: h, color: rgb(0.85, 0.85, 0.85), borderColor: rgb(0,0,0), borderWidth: 0.5 });
  const dText = (text, x, yPos, size, f = font) => page.drawText(text || '', { x, y: yPos, size, font: f, color: rgb(0,0,0) });

  // -- Top Header Row --
  const h1 = 20;
  drawBg(marginX, y, W * 0.65, h1);
  drawBorder(marginX + W * 0.65, y, W * 0.35, h1);
  dText('LIBRO DE RECLAMACIONES', marginX + 100, y - 14, 12, bold);
  dText('HOJA DE RECLAMACIÓN', marginX + W * 0.65 + 20, y - 14, 11, bold);
  y -= h1;

  // -- Fecha / Numero --
  const h2 = 20;
  drawBorder(marginX, y, 60, h2);
  drawBorder(marginX + 60, y, W * 0.65 - 60, h2);
  drawBorder(marginX + W * 0.65, y, W * 0.35, h2);
  dText('FECHA:', marginX + 5, y - 14, 9, bold);
  dText(data.fecha ? data.fecha.split(',')[0] : '', marginX + 65, y - 14, 9, font);
  dText('N°', marginX + W * 0.65 + 5, y - 14, 10, bold);
  dText(data.codigo_reclamo || '', marginX + W * 0.65 + 40, y - 14, 10, font);
  y -= h2;

  // -- Proveedor --
  const h3 = 40;
  drawBorder(marginX, y, W, h3);
  dText('PROVEEDOR:', marginX + 5, y - 12, 8, bold);
  dText('LLAQUI CHUSI JORDY LEONIDAS (MANU JUNGLE FOREVER)', marginX + 75, y - 12, 8, font);
  dText('RUC:', marginX + 5, y - 24, 8, bold);
  dText('10712309283', marginX + 75, y - 24, 8, font);
  dText('DOMICILIO:', marginX + 5, y - 36, 8, bold);
  dText('Cusco, Perú', marginX + 75, y - 36, 7, font);
  y -= h3;

  // -- 1. Identificacion --
  const h4 = 16;
  drawBg(marginX, y, W, h4);
  dText('1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE', marginX + 5, y - 12, 9, bold);
  y -= h4;

  const rowHeight = 22;
  const labelW = 100;
  
  // Nombre
  drawBorder(marginX, y, labelW, rowHeight);
  drawBorder(marginX + labelW, y, W - labelW, rowHeight);
  dText('NOMBRE:', marginX + 5, y - 14, 8, bold);
  dText(data.nombres || '', marginX + labelW + 5, y - 14, 8, font);
  y -= rowHeight;

  // DNI
  drawBorder(marginX, y, labelW, rowHeight);
  drawBorder(marginX + labelW, y, W - labelW, rowHeight);
  dText('DNI / CE:', marginX + 5, y - 14, 8, bold);
  dText(data.documento || '', marginX + labelW + 5, y - 14, 8, font);
  y -= rowHeight;

  // Domicilio
  drawBorder(marginX, y, labelW, rowHeight);
  drawBorder(marginX + labelW, y, W - labelW, rowHeight);
  dText('DOMICILIO:', marginX + 5, y - 14, 8, bold);
  dText(data.domicilio || '', marginX + labelW + 5, y - 14, 8, font);
  y -= rowHeight;

  // Telefono / Email
  const telW = 200;
  drawBorder(marginX, y, labelW, rowHeight);
  drawBorder(marginX + labelW, y, telW - labelW, rowHeight);
  drawBorder(marginX + telW, y, 60, rowHeight);
  drawBorder(marginX + telW + 60, y, W - telW - 60, rowHeight);
  dText('TELÉFONO', marginX + 5, y - 14, 8, bold);
  dText(data.telefono || '', marginX + labelW + 5, y - 14, 8, font);
  dText('E-MAIL:', marginX + telW + 5, y - 14, 8, bold);
  dText(data.correo || '', marginX + telW + 65, y - 14, 8, font);
  y -= rowHeight;

  // Apoderado
  drawBorder(marginX, y, 350, rowHeight);
  drawBorder(marginX + 350, y, W - 350, rowHeight);
  dText('SI ES MENOR DE EDAD, NOMBRE DEL PADRE, MADRE O APODERADO:', marginX + 5, y - 14, 8, bold);
  dText(data.apoderado || '', marginX + 355, y - 14, 8, font);
  y -= rowHeight;

  // -- 2. Identificacion del Bien --
  drawBg(marginX, y, W, h4);
  dText('2. IDENTIFICACIÓN DEL BIEN CONTRATADO', marginX + 5, y - 12, 9, bold);
  y -= h4;

  const bCol1 = 100;
  const bCol2 = 40;
  const bCol3 = 130;
  const bCol4 = W - (bCol1 + bCol2 + bCol3);
  const isProd = (data.bien_tipo || '').toUpperCase() === 'PRODUCTO' ? 'X' : '';
  const isServ = (data.bien_tipo || '').toUpperCase() !== 'PRODUCTO' ? 'X' : '';

  // Row 1: Producto
  drawBorder(marginX, y, bCol1, rowHeight);
  drawBorder(marginX + bCol1, y, bCol2, rowHeight);
  drawBorder(marginX + bCol1 + bCol2, y, bCol3, rowHeight);
  drawBorder(marginX + bCol1 + bCol2 + bCol3, y, bCol4, rowHeight);
  dText('PRODUCTO', marginX + 5, y - 14, 8, bold);
  dText(isProd, marginX + bCol1 + 15, y - 14, 9, bold);
  dText('MONTO RECLAMADO:', marginX + bCol1 + bCol2 + 5, y - 14, 8, bold);
  dText(data.bien_monto ? `S/ ${data.bien_monto}` : '', marginX + bCol1 + bCol2 + bCol3 + 5, y - 14, 8, font);
  y -= rowHeight;

  // Row 2: Servicio
  drawBorder(marginX, y, bCol1, rowHeight);
  drawBorder(marginX + bCol1, y, bCol2, rowHeight);
  drawBorder(marginX + bCol1 + bCol2, y, bCol3, rowHeight);
  drawBorder(marginX + bCol1 + bCol2 + bCol3, y, bCol4, rowHeight);
  dText('SERVICIO', marginX + 5, y - 14, 8, bold);
  dText(isServ, marginX + bCol1 + 15, y - 14, 9, bold);
  dText('DESCRIPCIÓN:', marginX + bCol1 + bCol2 + 5, y - 14, 8, bold);
  
  // Truncate description if too long for this single line
  let desc = data.bien_descripcion || '';
  if (desc.length > 50) desc = desc.substring(0, 47) + '...';
  dText(desc, marginX + bCol1 + bCol2 + bCol3 + 5, y - 14, 8, font);
  y -= rowHeight;

  // -- 3. Detalle --
  const detTitleW = W * 0.55;
  drawBg(marginX, y, detTitleW, h4);
  drawBorder(marginX + detTitleW, y, 70, h4);
  drawBorder(marginX + detTitleW + 70, y, 40, h4);
  drawBorder(marginX + detTitleW + 110, y, 70, h4);
  drawBorder(marginX + detTitleW + 180, y, W - (detTitleW + 180), h4);
  dText('3. DETALLE DE LA RECLAMACIÓN Y PEDIDO DEL CONSUMIDOR', marginX + 5, y - 12, 8, bold);
  
  const isRec = (data.tipo || '').toUpperCase() === 'RECLAMO' ? 'X' : '';
  const isQue = (data.tipo || '').toUpperCase() === 'QUEJA' ? 'X' : '';
  dText('RECLAMO\xB9', marginX + detTitleW + 10, y - 12, 8, bold);
  dText(isRec, marginX + detTitleW + 85, y - 12, 9, bold);
  dText('QUEJA\xB2', marginX + detTitleW + 125, y - 12, 8, bold);
  dText(isQue, marginX + detTitleW + 195, y - 12, 9, bold);
  y -= h4;

  // Custom multi-line text wrapper
  const wrapText = (text, maxWidth, f, fontSize) => {
    if (!text) return [];
    const words = text.replace(/\n/g, ' \n ').split(' ');
    let lines = [];
    let currentLine = '';
    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      if (word === '\n') {
        lines.push(currentLine);
        currentLine = '';
        continue;
      }
      const testLine = currentLine.length === 0 ? word : currentLine + " " + word;
      const widthStr = f.widthOfTextAtSize(testLine, fontSize);
      if (widthStr < maxWidth) {
        currentLine = testLine;
      } else {
        lines.push(currentLine);
        currentLine = word;
      }
    }
    if (currentLine.length > 0) lines.push(currentLine);
    return lines;
  };

  // Detalle box
  const detH = 150;
  drawBorder(marginX, y, W, detH);
  dText('DETALLE:', marginX + 5, y - 14, 8, bold);
  
  if (data.detalle) {
    const lines = wrapText(data.detalle, W - 20, font, 9);
    let lY = y - 30;
    for (const l of lines) {
      if (lY > y - detH + 10) {
        dText(l, marginX + 10, lY, 9, font);
        lY -= 12;
      }
    }
  }
  y -= detH;

  // Pedido Box
  const pedH = 100;
  drawBorder(marginX, y, W * 0.7, pedH);
  drawBorder(marginX + W * 0.7, y, W * 0.3, pedH - 25);
  drawBorder(marginX + W * 0.7, y - pedH + 25, W * 0.3, 25);
  
  dText('PEDIDO:', marginX + 5, y - 14, 8, bold);
  if (data.pedido) {
    const lines = wrapText(data.pedido, W * 0.7 - 20, font, 9);
    let lY = y - 30;
    for (const l of lines) {
      if (lY > y - pedH + 10) {
        dText(l, marginX + 10, lY, 9, font);
        lY -= 12;
      }
    }
  }
  dText('FIRMA DEL CONSUMIDOR', marginX + W * 0.7 + 10, y - pedH + 8, 8, bold);
  y -= pedH;

  // -- 4. Observaciones --
  drawBg(marginX, y, W, h4);
  dText('4. OBSERVACIONES Y ACCIONES ADOPTADAS POR EL PROVEEDOR', marginX + 5, y - 12, 8, bold);
  y -= h4;

  const obsH = 70;
  drawBorder(marginX, y, W * 0.45, obsH);
  drawBorder(marginX + W * 0.45, y, W * 0.25, obsH);
  drawBorder(marginX + W * 0.7, y, W * 0.3, obsH - 20);
  drawBorder(marginX + W * 0.7, y - obsH + 20, W * 0.3, 20);
  dText('FECHA DE COMUNICACIÓN DE LA RESPUESTA:', marginX + 5, y - 14, 7, bold);
  dText('FIRMA DEL PROVEEDOR', marginX + W * 0.7 + 15, y - obsH + 6, 8, bold);
  y -= obsH;

  // -- Footer notes --
  const fh = 20;
  drawBorder(marginX, y, W * 0.5, fh);
  drawBorder(marginX + W * 0.5, y, W * 0.5, fh);
  dText('\xB9 RECLAMO: Disconformidad relacionada a los productos o servicios.', marginX + 5, y - 8, 6, font);
  dText('\xB2 QUEJA: Disconformidad no relacionada a los productos o servicios; o,', marginX + W * 0.5 + 5, y - 8, 6, font);
  dText('  malestar o descontento respecto a la atención al público.', marginX + W * 0.5 + 5, y - 15, 6, font);
  y -= fh;

  drawBg(marginX, y, W, 15);
  dText('HOJA DE RECLAMACIÓN VIRTUAL', marginX + W - 180, y - 10, 9, bold);
  y -= 15;

  dText('*La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.', marginX, y - 10, 6, font);
  dText('* El proveedor debe dar respuesta al reclamo o queja en un plazo no mayor a quince (15) días hábiles, el cual es improrrogable.', marginX, y - 18, 6, font);

  return await pdfDoc.save();
}
async function sendEmail(env, to, subject, text, html, attachments = [], cc = '') {
  const body = {
    from: "Manu Jungle Forever <discover@manujungleforever.com>",
    to: [to],
    subject: subject,
    html: html,
    text: text
  };
  if (cc) body.cc = [cc];
  if (attachments && attachments.length > 0) body.attachments = attachments;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    console.error("Error enviando email via Resend:", await res.text());
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const data = await request.formData().catch(() => null);
    if (!data) return error('Formato invalido');

    const nombres          = data.get('nombres') || '';
    const documento        = data.get('documento') || '';
    const domicilio        = data.get('domicilio') || '';
    const telefono         = data.get('telefono') || '';
    const correo           = data.get('correo') || '';
    const apoderado        = data.get('apoderado') || '';
    const bien_tipo        = data.get('bien_tipo') || '';
    const bien_monto       = data.get('bien_monto') || '';
    const bien_descripcion = data.get('bien_descripcion') || '';
    const tipo             = data.get('tipo') || 'Reclamo';
    const detalle          = data.get('detalle') || '';
    const pedido           = data.get('pedido') || '';

    if (!nombres || !documento || !domicilio || !telefono || !correo || !detalle || !pedido) {
      return error('Faltan campos obligatorios');
    }

    // 1. Leer GitHub PRIMERO para obtener ultimo correlativo del anio
    const repo     = 'manujungleforever-debug/manujungleforever';
    const branch   = 'main';
    const filePath = 'www.manujungleforever.com/data/reclamos.json';
    const ghUrl    = `https://api.github.com/repos/${repo}/contents/${filePath}?ref=${branch}`;
    const ghHeaders = {
      'User-Agent'   : 'Cloudflare-Worker',
      'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
      'Accept'       : 'application/vnd.github.v3+json'
    };

    let fileSha  = null;
    let reclamos = [];

    if (env.GITHUB_TOKEN) {
      try {
        const getRes = await fetch(ghUrl, { headers: ghHeaders });
        if (getRes.ok) {
          const dataGet = await getRes.json();
          fileSha  = dataGet.sha;
          reclamos = JSON.parse(atob(dataGet.content.replace(/\n/g, '')));
        }
      } catch (ghErr) {
        console.warn('No se pudo leer reclamos.json:', ghErr);
      }
    }

    // 2. Correlativo secuencial YYYY-NNNNNN exigido por INDECOPI
    // Se reinicia automaticamente cada 1 de enero.
    const anio   = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Lima' })).getFullYear();
    const prefix = `${anio}-`;

    let maxNum = 0;
    for (const rec of reclamos) {
      if (rec.codigo_reclamo && rec.codigo_reclamo.startsWith(prefix)) {
        const num = parseInt(rec.codigo_reclamo.slice(prefix.length), 10);
        if (!isNaN(num) && num > maxNum) maxNum = num;
        break; // array ordenado desc; el primero que coincide es el mas reciente del anio
      }
    }
    const codigo_reclamo = `${prefix}${String(maxNum + 1).padStart(6, '0')}`;
    const fecha = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    const dataObj = {
      codigo_reclamo, fecha,
      nombres, documento, domicilio, telefono, correo, apoderado,
      bien_tipo, bien_monto, bien_descripcion,
      tipo, detalle, pedido
    };

    // 3. Generar PDF
    let pdfBytes;
    try {
      pdfBytes = await generateReclamoPDF(dataObj);
    } catch (e) {
      console.error('Error generando PDF:', e);
      return error('Error interno al generar el documento', 500);
    }

    const pdfBase64   = btoa(String.fromCharCode(...new Uint8Array(pdfBytes)));
    const attachments = [{ filename: `${codigo_reclamo}.pdf`, content: pdfBase64 }];

    // 4. Enviar correos
    // Tag +reclamaciones para filtro Zoho Mail -> carpeta "LIBRO DE RECLAMACIONES"
    const toEmail = 'discover+reclamaciones@manujungleforever.com';

    const msgEmpresa = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;">
        <h2 style="color:#2d8a56;text-align:center;border-bottom:2px solid #2d8a56;padding-bottom:10px;margin-bottom:10px;">NUEVO ${tipo.toUpperCase()} - LIBRO DE RECLAMACIONES</h2>
        <p><strong>N&deg;:</strong> ${codigo_reclamo}</p>
        <p><strong>Fecha:</strong> ${fecha}</p>
        <p><strong>Cliente:</strong> ${nombres} (DNI/CE: ${documento})</p>
        <p><strong>Contacto:</strong> ${correo} | ${telefono}</p>
        <div style="background:#f9f9f9;padding:15px;border-left:4px solid #2d8a56;margin-top:20px;">
          <h3 style="margin-top:0;color:#2d8a56;">Detalle de la ${tipo}:</h3>
          <p style="white-space:pre-wrap;">${detalle}</p>
          <h3 style="margin-top:15px;color:#2d8a56;">Pedido del Cliente:</h3>
          <p style="white-space:pre-wrap;">${pedido}</p>
        </div>
        <p style="text-align:center;margin-top:20px;font-size:12px;color:#777;">El documento PDF oficial se encuentra adjunto.</p>
      </div>`;

    const msgClienteHtml = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;">
        <h2 style="color:#2d8a56;text-align:center;border-bottom:2px solid #2d8a56;padding-bottom:10px;margin-bottom:10px;">CARGO DE RECEPCION: HOJA DE RECLAMACION - N&deg; ${codigo_reclamo}</h2>
        <p>Estimado(a) <strong>${nombres}</strong>,</p>
        <p>Le informamos que hemos recibido satisfactoriamente su <strong>${tipo.toLowerCase()}</strong> a traves de nuestro Libro de Reclamaciones Virtual.</p>
        <div style="background:#f9f9f9;padding:15px;border:1px solid #eee;margin:20px 0;text-align:center;">
          <p style="margin:0;font-size:14px;color:#555;">Fecha de registro:</p>
          <h3 style="margin:5px 0 0 0;color:#2d8a56;">${fecha}</h3>
        </div>
        <p>Adjuntamos el documento PDF oficial que sirve como <strong>Cargo de Recepcion</strong> de su reclamo/queja.</p>
        <div style="background:#fff3cd;border-left:4px solid #ffeeba;padding:15px;margin-top:20px;">
          <p style="margin-bottom:0;color:#856404;font-size:13px;">La formulacion del reclamo no impide acudir a otras vias de solucion de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.<br><br><b>MANU JUNGLE FOREVER</b> cuenta con un plazo maximo de <b>quince (15) dias habiles</b> improrrogables para atender su solicitud y emitir una respuesta formal.</p>
        </div>
        <p style="margin-top:20px;text-align:center;font-size:12px;color:#777;">Atentamente,<br><strong>Manu Jungle Forever</strong></p>
      </div>`;

    if (env.RESEND_API_KEY) {
      await sendEmail(env, toEmail, `[${tipo.toUpperCase()}] ${codigo_reclamo}`, msgEmpresa, msgEmpresa, attachments, toEmail);
      await sendEmail(env, correo, `Cargo de Recepcion - Hoja de Reclamacion N&deg; ${codigo_reclamo}`, 'Adjunto su cargo.', msgClienteHtml, attachments, toEmail);
    } else {
      console.warn('RESEND_API_KEY no configurada.');
    }

    // 5. Guardar en GitHub (reutiliza los datos ya leidos, sin segunda llamada a la API)
    if (env.GITHUB_TOKEN) {
      try {
        reclamos.unshift({ ...dataObj, id: Date.now(), estado: 'Pendiente' });
        const contentB64 = btoa(unescape(encodeURIComponent(JSON.stringify(reclamos, null, 2))));
        const putBody = { message: `Nuevo reclamo: ${codigo_reclamo}`, content: contentB64, branch };
        if (fileSha) putBody.sha = fileSha;
        await fetch(`https://api.github.com/repos/${repo}/contents/${filePath}`, {
          method: 'PUT', headers: ghHeaders, body: JSON.stringify(putBody)
        });
      } catch (err) {
        console.error('Error guardando en GitHub:', err);
      }
    }

    return json({ ok: true, success: true, codigo_reclamo, message: 'Reclamo registrado correctamente' });
  } catch (e) {
    console.error('Error general reclamo:', e);
    return error('Error procesando la solicitud', 500);
  }
}