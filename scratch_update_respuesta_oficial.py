import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\functions\api\admin\responder-reclamo.js'
with codecs.open(path, 'r', 'utf-8') as f:
    js = f.read()

old_snippet = '''    const msgHtml = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:650px;margin:0 auto;border:1px solid #ddd;border-radius:8px;overflow:hidden;">
        <div style="background:#2d8a56;padding:20px;text-align:center;">
            <h3 style="color:#fff;margin:8px 0">RESPUESTA OFICIAL A SU ${reclamo.tipo.toUpperCase()}</h3>
            <p style="font-size:13px;color:#e2e8f0;margin:0;">N° ${reclamo.codigo_reclamo} | Respondido el: ${fechaRespuesta}</p>
        </div>
        <div style="padding:30px;">
          <p style="font-size:15px">Estimado(a) <strong>${reclamo.nombres}</strong>,</p>
          <p style="font-size:14px;color:#444">Hemos analizado su ${reclamo.tipo.toLowerCase()} registrado en nuestro Libro de Reclamaciones Virtual y procedemos a darle respuesta formal conforme a la Ley N° 29571.</p>
          
          <table style="width:100%;border-collapse:collapse;margin:20px 0;font-size:13px;background:#f8fafc;">
            <tbody>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;width:40%;border:1px solid #e2e8f0;">Su Reclamo N°:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.codigo_reclamo}</td>
              </tr>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;border:1px solid #e2e8f0;">Tipo:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.tipo}</td>
              </tr>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;border:1px solid #e2e8f0;">Fecha de Registro:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.fecha}</td>
              </tr>
            </tbody>
          </table>

          <div style="background:#f1f5f9;border-left:4px solid #2d8a56;padding:15px;margin-bottom:25px;">
            <h4 style="margin-top:0;color:#2d8a56;margin-bottom:10px;">RESPUESTA DE MANU JUNGLE FOREVER:</h4>
            <p style="margin:0;font-size:14px;white-space:pre-wrap;">${detalle_respuesta}</p>
          </div>

          <p style="font-size:13px;color:#666;">Si tiene alguna duda adicional o no está conforme con esta respuesta, puede responder directamente a este correo o comunicarse con nuestros canales de atención al cliente.</p>
          <p style="font-size:14px;margin-top:30px;">Atentamente,<br><strong style="color:#2d8a56">Servicio al Cliente - Manu Jungle Forever</strong></p>
        </div>
      </div>
    `;

    if (env.RESEND_API_KEY) {
      await sendEmail(env, reclamo.correo, `Respuesta Oficial - Reclamo N° ${reclamo.codigo_reclamo}`, 'Por favor, revise la respuesta en el correo HTML.', msgHtml, [], 'discover@manujungleforever.com');
    }'''

new_snippet = '''    const msgHtml = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;border-radius:8px;background:#ffffff;">
        <div style="text-align:center;margin-bottom:10px;background:#030807;padding:15px;border-top-left-radius:8px;border-top-right-radius:8px;">
          <img src="https://www.manujungleforever.com/assets/img/logo.png" alt="Manu Jungle Forever" style="max-width:180px;">
        </div>
        <div style="padding:20px;">
          <h2 style="color:#10b981;text-align:center;border-bottom:2px solid #10b981;padding-bottom:10px;margin-bottom:15px;margin-top:0;">RESPUESTA OFICIAL A SU ${reclamo.tipo.toUpperCase()}</h2>
          <p style="text-align:center;font-size:13px;color:#777;margin-top:-10px;margin-bottom:20px;">N° ${reclamo.codigo_reclamo} | Respondido el: ${fechaRespuesta}</p>
          <p style="font-size:15px">Estimado(a) <strong>${reclamo.nombres}</strong>,</p>
          <p style="font-size:14px;color:#444">Hemos analizado su ${reclamo.tipo.toLowerCase()} registrado en nuestro Libro de Reclamaciones Virtual y procedemos a darle respuesta formal conforme a la Ley N° 29571.</p>
          
          <table style="width:100%;border-collapse:collapse;margin:20px 0;font-size:13px;background:#f8fafc;">
            <tbody>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;width:40%;border:1px solid #e2e8f0;">Su Reclamo N°:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.codigo_reclamo}</td>
              </tr>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;border:1px solid #e2e8f0;">Tipo:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.tipo}</td>
              </tr>
              <tr>
                <td style="padding:8px 12px;font-weight:bold;border:1px solid #e2e8f0;">Fecha de Registro:</td>
                <td style="padding:8px 12px;border:1px solid #e2e8f0;">${reclamo.fecha}</td>
              </tr>
            </tbody>
          </table>

          <div style="background:#f9f9f9;border-left:4px solid #10b981;padding:15px;margin-bottom:25px;">
            <h4 style="margin-top:0;color:#10b981;margin-bottom:10px;">RESPUESTA DE MANU JUNGLE FOREVER:</h4>
            <p style="margin:0;font-size:14px;white-space:pre-wrap;">${detalle_respuesta}</p>
          </div>

          <p style="font-size:13px;color:#666;">Si tiene alguna duda adicional o no está conforme con esta respuesta, puede responder directamente a este correo o comunicarse con nuestros canales de atención al cliente.</p>
          <p style="font-size:14px;margin-top:30px;">Atentamente,<br><strong style="color:#10b981">Servicio al Cliente - Manu Jungle Forever</strong></p>
        </div>
      </div>
    `;

    if (env.RESEND_API_KEY) {
      await sendEmail(env, reclamo.correo, `[LIBRO DE RECLAMACIONES] Respuesta Oficial - Reclamo N° ${reclamo.codigo_reclamo}`, 'Por favor, revise la respuesta en el correo HTML.', msgHtml, [], 'discover@manujungleforever.com');
    }'''

js = js.replace(old_snippet, new_snippet)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(js)
