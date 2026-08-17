// ─── Booking Form Handler ─────────────────────────────────────────────────────
// Cloudflare Pages Function: /api/booking
// Receives form data from the contact/book-now page and sends email via Resend.
// Uses +tag addressing so Gmail filters can route to "SOLICITUDES DE RESERVA" folder.

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

// ─── Company notification email (high-contrast, premium design) ───────────────
function buildEmailHtml({ name, email, phone, tour, travelers, date, contact, notes }) {
  const dateStr = date
    ? new Date(date).toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' })
    : 'No especificada';

  const row = (label, value, highlight = false) => `
    <tr>
      <td style="padding:12px 16px;background:#f4f4f4;border:1px solid #e0e0e0;font-weight:700;font-size:13px;color:#333;width:36%;white-space:nowrap;">${label}</td>
      <td style="padding:12px 16px;border:1px solid #e0e0e0;font-size:14px;color:${highlight ? '#1a7a45' : '#222'};font-weight:${highlight ? '700' : '400'};">${value}</td>
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
          <td style="background:linear-gradient(135deg,#002e24 0%,#004d3a 100%);padding:36px 40px;text-align:center;">
            <div style="margin-bottom:12px;">
              <img src="https://www.manujungleforever.com/assets/img/logo.png" alt="Manu Jungle Forever" style="height:65px;width:auto;">
            </div>
            <h1 style="margin:0;color:#c9a84c;font-size:24px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;">
              NUEVA SOLICITUD DE RESERVA
            </h1>
            <p style="margin:10px 0 0;color:#ffffff;font-size:14px;font-weight:400;opacity:0.9;">
              Manu Jungle Forever · Tour Enquiry
            </p>
            <div style="margin-top:16px;display:inline-block;background:#c9a84c;border-radius:20px;padding:4px 18px;">
              <span style="color:#002e24;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">⚡ Acción Requerida — Responder en 24h</span>
            </div>
          </td>
        </tr>

        <!-- BODY -->
        <tr>
          <td style="padding:36px 40px;">
            <p style="margin:0 0 20px;font-size:15px;color:#444;">
              Se ha recibido una nueva consulta de reserva desde el sitio web. Revisa los detalles a continuación y responde al cliente lo antes posible.
            </p>

            <!-- DATA TABLE -->
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-radius:8px;overflow:hidden;">
              ${row('👤 Nombre', name)}
              ${row('📧 Email', `<a href="mailto:${email}" style="color:#1a7a45;font-weight:600;">${email}</a>`)}
              ${row('📞 Teléfono / WhatsApp', `<a href="https://wa.me/${phone.replace(/\D/g,'')}" style="color:#1a7a45;">${phone}</a>`)}
              ${row('🗺️ Tour Seleccionado', tour, true)}
              ${row('👥 N° de Viajeros', travelers || '—')}
              ${row('📅 Fecha de Salida', dateStr)}
              ${row('💬 Contacto Preferido', contact)}
              ${notes ? row('📝 Notas / Preguntas', `<span style="white-space:pre-wrap;">${notes}</span>`) : ''}
            </table>

            <!-- CTA -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:28px;">
              <tr>
                <td style="background:#e8f5ee;border-left:4px solid #2d8a56;border-radius:0 8px 8px 0;padding:16px 20px;">
                  <p style="margin:0;font-size:13px;font-weight:700;color:#1a7a45;">⚡ Próximo paso</p>
                  <p style="margin:6px 0 0;font-size:13px;color:#333;">
                    Responder a <a href="mailto:${email}" style="color:#1a7a45;font-weight:600;">${email}</a> con precios, disponibilidad y detalles del tour <strong>${tour}</strong>.
                  </p>
                </td>
              </tr>
            </table>

            <!-- QUICK REPLY BUTTON -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;text-align:center;">
              <tr>
                <td align="center">
                  <a href="mailto:${email}?subject=Re: Consulta tour ${encodeURIComponent(tour)}&body=Hola ${encodeURIComponent(name)},%0A%0AGracias por tu interés en..."
                     style="display:inline-block;background:#002e24;color:#c9a84c;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:700;font-size:14px;letter-spacing:0.5px;">
                    ✉️ Responder al Cliente
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- FOOTER -->
        <tr>
          <td style="background:#f4f4f4;padding:18px 40px;text-align:center;border-top:1px solid #e0e0e0;">
            <p style="margin:0;font-size:11px;color:#999;">
              Este mensaje fue generado automáticamente desde
              <a href="https://www.manujungleforever.com" style="color:#2d8a56;">manujungleforever.com</a>
              · Fitzcarrald 17800, Nuevo Eden, Perú
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

// ─── Confirmation email to the client ────────────────────────────────────────
function buildConfirmationHtml({ name, tour, date }) {
  const dateStr = date
    ? new Date(date).toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' })
    : '';

  return `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0f0f0;font-family:Arial,Helvetica,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f0f0;padding:32px 16px;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.10);max-width:620px;width:100%;">

        <!-- HEADER -->
        <tr>
          <td style="background:linear-gradient(135deg,#002e24 0%,#004d3a 100%);padding:36px 40px;text-align:center;">
            <div style="margin-bottom:12px;">
              <img src="https://www.manujungleforever.com/assets/img/logo.png" alt="Manu Jungle Forever" style="height:65px;width:auto;">
            </div>
            <h1 style="margin:0;color:#c9a84c;font-size:22px;font-weight:800;">¡Gracias por tu consulta!</h1>
            <p style="margin:10px 0 0;color:#ffffff;font-size:15px;font-weight:400;opacity:0.9;">
              Hemos recibido tu solicitud correctamente
            </p>
          </td>
        </tr>

        <!-- BODY -->
        <tr>
          <td style="padding:36px 40px;">
            <p style="margin:0 0 16px;font-size:15px;color:#333;">Hola <strong>${name}</strong>,</p>
            <p style="margin:0 0 16px;font-size:15px;color:#555;">
              Hemos recibido tu solicitud para el tour
              <strong style="color:#1a7a45;">${tour}</strong>${dateStr ? ` con fecha de salida el <strong>${dateStr}</strong>` : ''}.
            </p>
            <p style="margin:0 0 28px;font-size:15px;color:#555;">
              Nuestro equipo se pondrá en contacto contigo en las próximas
              <strong>24 horas</strong> con precios, disponibilidad y todos los detalles de tu aventura en el Amazonas peruano.
            </p>

            <!-- SUMMARY BOX -->
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;border-radius:8px;margin-bottom:28px;">
              <tr>
                <td style="padding:20px 24px;">
                  <p style="margin:0 0 6px;font-size:12px;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:1px;">Tour solicitado</p>
                  <p style="margin:0;font-size:17px;font-weight:700;color:#002e24;">${tour}</p>
                  ${dateStr ? `<p style="margin:6px 0 0;font-size:13px;color:#666;">📅 ${dateStr}</p>` : ''}
                </td>
              </tr>
            </table>

            <!-- WHATSAPP CTA -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
              <tr>
                <td style="background:#e8f5ee;border-radius:8px;padding:20px 24px;text-align:center;">
                  <p style="margin:0 0 4px;font-size:14px;color:#333;font-weight:600;">¿Necesitas una respuesta inmediata?</p>
                  <p style="margin:0 0 14px;font-size:13px;color:#666;">Escríbenos directamente por WhatsApp</p>
                  <a href="https://api.whatsapp.com/send?phone=51901525679&text=Hola!%20Consulté%20por%20el%20tour%20${encodeURIComponent(tour)}"
                     style="display:inline-block;background:#25d366;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;font-size:14px;">
                    💬 WhatsApp: +51 901 525 679
                  </a>
                </td>
              </tr>
            </table>

            <p style="font-size:13px;color:#888;margin:0;">
              Atentamente,<br>
              <strong style="color:#333;">Jordy &amp; el equipo de Manu Jungle Forever</strong><br>
              📧 discover@manujungleforever.com &nbsp;·&nbsp; 📞 +51 901 525 679
            </p>
          </td>
        </tr>

        <!-- FOOTER -->
        <tr>
          <td style="background:#f4f4f4;padding:18px 40px;text-align:center;border-top:1px solid #e0e0e0;">
            <p style="margin:0;font-size:11px;color:#999;">
              Manu Jungle Forever · Fitzcarrald 17800, Nuevo Eden, Perú<br>
              <a href="https://www.manujungleforever.com" style="color:#2d8a56;">www.manujungleforever.com</a>
            </p>
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
    // Accept both JSON and FormData
    const contentType = request.headers.get('content-type') || '';
    let fields = {};

    if (contentType.includes('application/json')) {
      fields = await request.json();
    } else {
      const fd = await request.formData();
      fd.forEach((v, k) => { fields[k] = v; });
    }

    const name      = (fields.traveler_name || fields.name || '').trim();
    const email     = (fields.email || '').trim().toLowerCase();
    const phone     = (fields.phone || '').trim();
    const tour      = (fields.tour_type || fields.tour || '').trim();
    const travelers = (fields.num_travelers || fields.travelers || '').trim();
    const date      = (fields.departure_date || fields.date || '').trim();
    const contact   = (fields.contact_pref || fields.contact || 'Email').trim();
    const notes     = (fields.notes || '').trim();

    // Basic validation
    if (!name || !email || !phone || !tour) {
      return error('Faltan campos obligatorios: nombre, email, teléfono y tipo de tour.');
    }

    // Email format check
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return error('Formato de email inválido.');
    }

    const payload = { name, email, phone, tour, travelers, date, contact, notes };

    // Use +reservas tag so Gmail filter routes to "SOLICITUDES DE RESERVA" folder
    const companyEmail = 'discover+reservas@manujungleforever.com';
    const subject = `[RESERVA] ${name} — ${tour}`;

    if (env.RESEND_API_KEY) {
      // Email to company (tagged for folder filtering)
      await sendEmail(env, companyEmail, subject, buildEmailHtml(payload), email);

      // Confirmation email to client
      try {
        await sendEmail(
          env,
          email,
          '✅ Hemos recibido tu consulta — Manu Jungle Forever',
          buildConfirmationHtml(payload),
          'discover@manujungleforever.com'
        );
      } catch (confirmErr) {
        console.warn('Could not send confirmation to client:', confirmErr);
      }
    } else {
      console.warn('RESEND_API_KEY not set. Booking data:', JSON.stringify(payload));
      return error('Configuración de servidor incompleta. Por favor contáctanos por WhatsApp.', 500);
    }

    return json({ ok: true, success: 'true', message: '¡Tu consulta fue enviada! Te responderemos en menos de 24 horas.' });

  } catch (e) {
    console.error('Booking handler error:', e);
    return error('Error procesando la solicitud. Por favor intenta de nuevo.', 500);
  }
}
