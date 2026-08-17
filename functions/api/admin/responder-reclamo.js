import { PDFDocument, rgb, StandardFonts } from '../pdf-lib.js';

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

async function verifyToken(request, env) {
  const auth = request.headers.get('Authorization') || '';
  const token = auth.replace('Bearer ', '').trim();
  if (!token) return { error: 'No autenticado', status: 401 };
  const secret = env.CMS_SECRET || 'mjf-cms-secret-2026-manujungleforever';
  try {
    const [payload, sig] = token.split('.');
    const expected = await hmac(payload, secret);
    if (sig !== expected) return { error: 'Token inválido', status: 401 };
    const { exp } = JSON.parse(atob(payload));
    if (Date.now() > exp) return { error: 'Sesión expirada', status: 401 };
    return null;
  } catch {
    return { error: 'Token inválido', status: 401 };
  }
}

async function hmac(data, secret) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2,'0')).join('');
}

export async function onRequestPut(context) {
  const { request, env } = context;
  
  // Verify token
  const authErr = await verifyToken(request, env);
  if (authErr) {
    return error(authErr.error, authErr.status);
  }

  try {
    const data = await request.json().catch(() => null);
    if (!data) return error('JSON inválido');

    const { id, detalle_respuesta } = data;
    if (!id || !detalle_respuesta) return error('Faltan datos requeridos');

    // 1. Obtener el reclamo de D1
    const reclamo = await env.DB.prepare(
      "SELECT * FROM reclamos WHERE id = ?"
    ).bind(id).first();

    if (!reclamo) return error('Reclamo no encontrado', 404);
    if (reclamo.estado === 'Atendido') return error('Este reclamo ya fue atendido', 409);

    // 2. Generar la fecha de respuesta
    const fechaRespuesta = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    // 3. Enviar Correo de Respuesta
    const msgHtml = `
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
    }

    // 4. Actualizar el estado en D1
    try {
      await env.DB.prepare(
        "UPDATE reclamos SET estado = 'Atendido', detalle_respuesta = ?, fecha_respuesta = ? WHERE id = ?"
      ).bind(detalle_respuesta, fechaRespuesta, id).run();
    } catch (dbErr) {
      console.error('Error al actualizar en D1:', dbErr);
      return error('Error al guardar la respuesta en la base de datos', 500);
    }

    return json({ ok: true, message: 'Reclamo atendido y correo enviado satisfactoriamente' });
  } catch (e) {
    console.error('Error responder reclamo:', e);
    return error('Error procesando la solicitud', 500);
  }
}
