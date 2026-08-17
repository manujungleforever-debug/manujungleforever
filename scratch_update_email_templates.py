import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\functions\api\reclamo.js'
with codecs.open(path, 'r', 'utf-8') as f:
    js = f.read()

old_templates = '''    const msgEmpresa = `
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
      </div>`;'''

new_templates = '''    const msgEmpresa = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;background:#ffffff;">
        <div style="text-align:center;margin-bottom:20px;background:#030807;padding:15px;border-radius:6px;">
          <img src="https://www.manujungleforever.com/assets/img/logo.png" alt="Manu Jungle Forever" style="max-width:180px;">
        </div>
        <h2 style="color:#10b981;text-align:center;border-bottom:2px solid #10b981;padding-bottom:10px;margin-bottom:10px;">NUEVO ${tipo.toUpperCase()} - LIBRO DE RECLAMACIONES</h2>
        <p><strong>N&deg;:</strong> ${codigo_reclamo}</p>
        <p><strong>Fecha:</strong> ${fecha}</p>
        <p><strong>Cliente:</strong> ${nombres} (DNI/CE: ${documento})</p>
        <p><strong>Contacto:</strong> ${correo} | ${telefono}</p>
        <div style="background:#f9f9f9;padding:15px;border-left:4px solid #10b981;margin-top:20px;">
          <h3 style="margin-top:0;color:#10b981;">Detalle de la ${tipo}:</h3>
          <p style="white-space:pre-wrap;">${detalle}</p>
          <h3 style="margin-top:15px;color:#10b981;">Pedido del Cliente:</h3>
          <p style="white-space:pre-wrap;">${pedido}</p>
        </div>
        <p style="text-align:center;margin-top:20px;font-size:12px;color:#777;">El documento PDF oficial se encuentra adjunto.</p>
      </div>`;

    const msgClienteHtml = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;background:#ffffff;">
        <div style="text-align:center;margin-bottom:20px;background:#030807;padding:15px;border-radius:6px;">
          <img src="https://www.manujungleforever.com/assets/img/logo.png" alt="Manu Jungle Forever" style="max-width:180px;">
        </div>
        <h2 style="color:#10b981;text-align:center;border-bottom:2px solid #10b981;padding-bottom:10px;margin-bottom:10px;">CARGO DE RECEPCION: HOJA DE RECLAMACION - N&deg; ${codigo_reclamo}</h2>
        <p>Estimado(a) <strong>${nombres}</strong>,</p>
        <p>Le informamos que hemos recibido satisfactoriamente su <strong>${tipo.toLowerCase()}</strong> a traves de nuestro Libro de Reclamaciones Virtual.</p>
        <div style="background:#f9f9f9;padding:15px;border:1px solid #eee;margin:20px 0;text-align:center;">
          <p style="margin:0;font-size:14px;color:#555;">Fecha de registro:</p>
          <h3 style="margin:5px 0 0 0;color:#10b981;">${fecha}</h3>
        </div>
        <p>Adjuntamos el documento PDF oficial que sirve como <strong>Cargo de Recepcion</strong> de su reclamo/queja.</p>
        <div style="background:#fff3cd;border-left:4px solid #ffeeba;padding:15px;margin-top:20px;">
          <p style="margin-bottom:0;color:#856404;font-size:13px;">La formulacion del reclamo no impide acudir a otras vias de solucion de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.<br><br><b>MANU JUNGLE FOREVER</b> cuenta con un plazo maximo de <b>quince (15) dias habiles</b> improrrogables para atender su solicitud y emitir una respuesta formal.</p>
        </div>
        <p style="margin-top:20px;text-align:center;font-size:12px;color:#777;">Atentamente,<br><strong>Manu Jungle Forever</strong></p>
      </div>`;'''

js = js.replace(old_templates, new_templates)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(js)
