// ─── Booking Form Handler ─────────────────────────────────────────────────────
// Cloudflare Pages Function: /api/booking
// Receives form data from the contact/book-now page and sends email via Resend.

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

// ─── Email HTML template ──────────────────────────────────────────────────────
function buildEmailHtml({ name, email, phone, tour, travelers, date, contact, notes }) {
  const dateStr = date ? new Date(date).toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' }) : 'No especificada';
  return `
  <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:620px;margin:0 auto;border:1px solid #ddd;border-radius:10px;overflow:hidden;">
    <div style="background:#002e24;padding:28px 32px;text-align:center;">
      <h1 style="color:#c9a84c;margin:0;font-size:22px;letter-spacing:1px;">🌿 NUEVA SOLICITUD DE RESERVA</h1>
      <p style="color:rgba(255,255,255,0.65);margin:6px 0 0;font-size:13px;">Manu Jungle Forever — Tour Enquiry</p>
    </div>
    <div style="padding:32px;">
      <table style="width:100%;border-collapse:collapse;font-size:14px;">
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;width:38%;">Nombre</td><td style="padding:10px 12px;border:1px solid #eee;">${name}</td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">Email</td><td style="padding:10px 12px;border:1px solid #eee;"><a href="mailto:${email}" style="color:#2d8a56;">${email}</a></td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">Teléfono / WhatsApp</td><td style="padding:10px 12px;border:1px solid #eee;">${phone}</td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">Tour Seleccionado</td><td style="padding:10px 12px;border:1px solid #eee;"><strong style="color:#2d8a56;">${tour}</strong></td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">N° de Viajeros</td><td style="padding:10px 12px;border:1px solid #eee;">${travelers}</td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">Fecha de Salida</td><td style="padding:10px 12px;border:1px solid #eee;">${dateStr}</td></tr>
        <tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;">Contacto Preferido</td><td style="padding:10px 12px;border:1px solid #eee;">${contact}</td></tr>
        ${notes ? `<tr><td style="padding:10px 12px;background:#f7f7f7;border:1px solid #eee;font-weight:bold;vertical-align:top;">Notas / Preguntas</td><td style="padding:10px 12px;border:1px solid #eee;white-space:pre-wrap;">${notes}</td></tr>` : ''}
      </table>
      <div style="background:#f0faf4;border-left:4px solid #2d8a56;padding:14px 18px;margin-top:24px;border-radius:4px;">
        <p style="margin:0;font-size:13px;color:#2d8a56;font-weight:bold;">⚡ Acción Requerida</p>
        <p style="margin:6px 0 0;font-size:13px;color:#555;">Responder dentro de las próximas 24 horas con precios y detalles del tour.</p>
      </div>
      <p style="margin-top:24px;font-size:12px;color:#aaa;text-align:center;">Este mensaje fue enviado desde el formulario de reservas de manujungleforever.com</p>
    </div>
  </div>`;
}

// ─── Confirmation email to the client ────────────────────────────────────────
function buildConfirmationHtml({ name, tour, date }) {
  const dateStr = date ? new Date(date).toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' }) : '';
  return `
  <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:620px;margin:0 auto;border:1px solid #ddd;border-radius:10px;overflow:hidden;">
    <div style="background:#002e24;padding:28px 32px;text-align:center;">
      <h1 style="color:#c9a84c;margin:0;font-size:22px;">🌿 ¡Gracias por tu consulta!</h1>
      <p style="color:rgba(255,255,255,0.65);margin:6px 0 0;font-size:13px;">Manu Jungle Forever</p>
    </div>
    <div style="padding:32px;">
      <p>Hola <strong>${name}</strong>,</p>
      <p>Hemos recibido tu solicitud de reserva para el tour <strong style="color:#2d8a56;">${tour}</strong>${dateStr ? ` con fecha de salida el <strong>${dateStr}</strong>` : ''}.</p>
      <p>Nuestro equipo te contactará dentro de las próximas <strong>24 horas</strong> con información sobre precios, disponibilidad y todos los detalles de tu aventura en el Amazonas.</p>
      <div style="background:#f0faf4;border:1px solid #c3e6cb;padding:18px 22px;border-radius:8px;margin:24px 0;text-align:center;">
        <p style="margin:0;font-size:13px;color:#555;">¿Necesitas respuesta inmediata?</p>
        <a href="https://api.whatsapp.com/send?phone=51901525679&text=Hola!%20Quiero%20m%C3%A1s%20informaci%C3%B3n%20sobre%20el%20tour%20${encodeURIComponent(tour)}" style="display:inline-block;margin-top:10px;background:#25d366;color:#fff;text-decoration:none;padding:10px 24px;border-radius:6px;font-weight:bold;font-size:14px;">💬 Escríbenos por WhatsApp</a>
      </div>
      <p style="font-size:13px;color:#777;">Atentamente,<br><strong>Jordy & el equipo de Manu Jungle Forever</strong><br>📧 discover@manujungleforever.com | 📞 +51 901 525 679</p>
    </div>
    <div style="background:#f7f7f7;padding:14px 32px;text-align:center;font-size:11px;color:#aaa;border-top:1px solid #eee;">
      Manu Jungle Forever · Fitzcarrald 17800, Nuevo Eden, Perú
    </div>
  </div>`;
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

    // Send notification to the company
    const toEmail = 'discover@manujungleforever.com';
    const subject = `[RESERVA] ${name} — ${tour}`;

    if (env.RESEND_API_KEY) {
      // Email to company
      await sendEmail(env, toEmail, subject, buildEmailHtml(payload), email);

      // Confirmation email to client
      try {
        await sendEmail(
          env,
          email,
          '✅ Hemos recibido tu consulta — Manu Jungle Forever',
          buildConfirmationHtml(payload),
          toEmail
        );
      } catch (confirmErr) {
        // Non-fatal: company email already sent
        console.warn('Could not send confirmation to client:', confirmErr);
      }
    } else {
      // Fallback: log and still return success (so we know if env var is missing)
      console.warn('RESEND_API_KEY not set. Booking data:', JSON.stringify(payload));
      return error('Configuración de servidor incompleta. Por favor contáctanos por WhatsApp.', 500);
    }

    return json({ ok: true, success: 'true', message: '¡Tu consulta fue enviada! Te responderemos en menos de 24 horas.' });

  } catch (e) {
    console.error('Booking handler error:', e);
    return error('Error procesando la solicitud. Por favor intenta de nuevo.', 500);
  }
}
