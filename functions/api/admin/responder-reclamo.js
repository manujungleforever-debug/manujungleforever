import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';

// ─── Utilidades ──────────────────────────────────────────────────────────────
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Content-Type': 'application/json;charset=UTF-8',
};

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
const error = (msg, status = 400) => json({ ok: false, error: msg }, status);

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

export async function onRequestPut(context) {
  const { request, env } = context;
  try {
    const data = await request.json().catch(() => null);
    if (!data) return error('JSON inválido');

    const { id, detalle_respuesta } = data;
    if (!id || !detalle_respuesta) return error('Faltan datos requeridos');

    // 1. Obtener la lista de reclamos de GitHub
    const repo = 'manujungleforever-debug/manujungleforever';
    const branch = 'main';
    const filePath = 'www.manujungleforever.com/data/reclamos.json';
    const url = `https://api.github.com/repos/${repo}/contents/${filePath}?ref=${branch}`;
    const headers = {
      'User-Agent': 'Cloudflare-Worker',
      'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json'
    };

    const getRes = await fetch(url, { headers });
    if (!getRes.ok) return error('Error al obtener reclamos de GitHub', 500);
    const dataGet = await getRes.json();
    const fileSha = dataGet.sha;
    const reclamos = JSON.parse(atob(dataGet.content));

    // 2. Encontrar el reclamo a responder
    const index = reclamos.findIndex(r => String(r.id) === String(id));
    if (index === -1) return error('Reclamo no encontrado', 404);

    const reclamo = reclamos[index];
    if (reclamo.estado === 'Atendido') return error('Este reclamo ya fue atendido', 409);

    // 3. Generar la fecha de respuesta
    const fechaRespuesta = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    // 4. Enviar Correo de Respuesta
    const msgHtml = `
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
    }

    // 5. Actualizar el estado en GitHub
    reclamo.estado = 'Atendido';
    reclamo.detalle_respuesta = detalle_respuesta;
    reclamo.fecha_respuesta = fechaRespuesta;
    reclamos[index] = reclamo;

    const contentB64 = btoa(unescape(encodeURIComponent(JSON.stringify(reclamos, null, 2))));
    const bodyPut = {
      message: `Respuesta a reclamo: ${reclamo.codigo_reclamo}`,
      content: contentB64,
      sha: fileSha,
      branch: branch
    };
    
    const putRes = await fetch(`https://api.github.com/repos/${repo}/contents/${filePath}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(bodyPut)
    });
    
    if (!putRes.ok) return error('Error al actualizar reclamo en GitHub', 500);

    return json({ ok: true, message: 'Reclamo atendido y correo enviado satisfactoriamente' });
  } catch (e) {
    console.error('Error responder reclamo:', e);
    return error('Error procesando la solicitud', 500);
  }
}
