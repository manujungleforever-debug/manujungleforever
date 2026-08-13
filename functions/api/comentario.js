// ─── Blog Comment Handler ─────────────────────────────────────────────────────
// Cloudflare Pages Function: /api/comentario
// Receives form data from the blog comment form and sends email via Resend.
// Uses +tag addressing so Zoho Mail filters can route to "COMENTARIOS" folder.

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Content-Type': 'application/json;charset=UTF-8',
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });

const error = (msg, status = 400) =>
  json({ ok: false, error: msg }, status);

// ─── Send email via Resend ────────────────────────────────────────────────────
async function sendEmail(env, to, subject, html, replyTo = '') {
  const body = {
    from: 'Manu Jungle Forever <discover@manujungleforever.com>',
    to: [to],
    subject,
    html,
  };
  if (replyTo) body.reply_to = replyTo;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const txt = await res.text();
    console.error('Resend error:', txt);
    throw new Error(`Resend failed: ${res.status}`);
  }
  return res.json();
}

// ─── Company notification email (high-contrast) ───────────────
function buildEmailHtml({ name, email, comment, pageUrl }) {
  const row = (label, value) => `
    <tr>
      <td style="padding:12px 16px;background:#f4f4f4;border:1px solid #e0e0e0;font-weight:700;font-size:13px;color:#333;width:36%;white-space:nowrap;vertical-align:top;">${label}</td>
      <td style="padding:12px 16px;border:1px solid #e0e0e0;font-size:14px;color:#222;white-space:pre-wrap;">${value}</td>
    </tr>`;

  return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0f0f0;font-family:Arial,Helvetica,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f0f0;padding:32px 16px;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.10);max-width:620px;width:100%;">

        <!-- HEADER -->
        <tr>
          <td style="background:linear-gradient(135deg,#003b5c 0%,#00598b 100%);padding:36px 40px;text-align:center;">
            <div style="font-size:36px;margin-bottom:12px;">💬</div>
            <h1 style="margin:0;color:#f0e4c6;font-size:24px;font-weight:800;letter-spacing:1px;text-transform:uppercase;">
              NUEVO COMENTARIO EN EL BLOG
            </h1>
          </td>
        </tr>

        <!-- BODY -->
        <tr>
          <td style="padding:36px 40px;">
            <p style="margin:0 0 20px;font-size:15px;color:#444;">
              Alguien ha dejado un comentario en tu blog. Revísalo antes de publicarlo.
            </p>

            <!-- DATA TABLE -->
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-radius:8px;overflow:hidden;">
              ${row('👤 Nombre', name)}
              ${row('📧 Email', `<a href="mailto:${email}" style="color:#00598b;font-weight:600;">${email}</a>`)}
              ${pageUrl ? row('🔗 Página Origen', `<a href="${pageUrl}" style="color:#00598b;">${pageUrl}</a>`) : ''}
              ${row('📝 Comentario', comment)}
            </table>

            <!-- QUICK REPLY BUTTON -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;text-align:center;">
              <tr>
                <td align="center">
                  <a href="mailto:${email}?subject=Gracias por tu comentario en nuestro blog&body=Hola ${encodeURIComponent(name)},%0A%0AGracias por tu comentario..."
                     style="display:inline-block;background:#003b5c;color:#f0e4c6;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:700;font-size:14px;letter-spacing:0.5px;">
                    ✉️ Responder al Autor
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

// ─── Route handlers ───────────────────────────────────────────────────────────
export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const contentType = request.headers.get('content-type') || '';
    let fields = {};

    if (contentType.includes('application/json')) {
      fields = await request.json();
    } else {
      const fd = await request.formData();
      fd.forEach((v, k) => { fields[k] = v; });
    }

    const name    = (fields.name || '').trim();
    const email   = (fields.email || '').trim().toLowerCase();
    const comment = (fields.comment || '').trim();
    // Use referer header to know which blog post this came from
    const referer = request.headers.get('Referer') || '';

    if (!name || !email || !comment) {
      return error('Faltan campos obligatorios: nombre, email y comentario.');
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return error('Formato de email inválido.');
    }

    const payload = { name, email, comment, pageUrl: referer };

    // Tag +comentarios para filtro en Zoho Mail -> carpeta "COMENTARIOS"
    const companyEmail = 'discover+comentarios@manujungleforever.com';
    const subject = `[COMENTARIO BLOG] ${name}`;

    if (env.RESEND_API_KEY) {
      await sendEmail(env, companyEmail, subject, buildEmailHtml(payload), email);
    } else {
      console.warn('RESEND_API_KEY not set. Comment data:', JSON.stringify(payload));
      return error('Error de servidor. Por favor intenta de nuevo más tarde.', 500);
    }

    return json({ ok: true, success: 'true', message: '¡Comentario enviado!' });

  } catch (e) {
    console.error('Comment handler error:', e);
    return error('Error procesando la solicitud.', 500);
  }
}
