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
  dText('MANU JUNGLE FOREVER E.I.R.L.', marginX + 75, y - 12, 8, font);
  dText('RUC:', marginX + 5, y - 24, 8, bold);
  dText('20610333283', marginX + 75, y - 24, 8, font);
  dText('DOMICILIO:', marginX + 5, y - 36, 8, bold);
  dText('Fitzcarrald 17800, Nuevo Eden, Manu, Peru', marginX + 75, y - 36, 7, font);
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

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function error(msg, status = 400) {
  return json({ ok: false, error: msg }, status);
}

// ─── Hashing (bcrypt-lite via SubtleCrypto - PBKDF2) ────────────────────────
// Cloudflare Workers no tienen bcrypt nativo; usamos PBKDF2 (SHA-256) que es
// igual de seguro para este contexto.

async function hashPassword(password) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const saltHex = Array.from(salt).map(b => b.toString(16).padStart(2, '0')).join('');
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
  const derived = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' }, key, 256);
  const hashHex = Array.from(new Uint8Array(derived)).map(b => b.toString(16).padStart(2, '0')).join('');
  return `pbkdf2:${saltHex}:${hashHex}`;
}

async function verifyPassword(password, stored) {
  // Soporte backward-compat para el hash de semilla (simple check) y PBKDF2
  if (stored.startsWith('pbkdf2:')) {
    const [, saltHex, hashHex] = stored.split(':');
    const salt = new Uint8Array(saltHex.match(/.{2}/g).map(b => parseInt(b, 16)));
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
    const derived = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' }, key, 256);
    const computed = Array.from(new Uint8Array(derived)).map(b => b.toString(16).padStart(2, '0')).join('');
    return computed === hashHex;
  }
  // Contraseña en texto plano (sólo para el usuario semilla inicial)
  return password === stored;
}

// ─── JWT mínimo (HS256 via SubtleCrypto) ────────────────────────────────────

async function sign(payload, secret) {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  const body = btoa(JSON.stringify(payload)).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  const data = `${header}.${body}`;
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  const sigB64 = btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `${data}.${sigB64}`;
}

async function verify(token, secret) {
  try {
    const [header, body, sig] = token.split('.');
    if (!header || !body || !sig) return null;
    const data = `${header}.${body}`;
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
    const sigBuf = Uint8Array.from(atob(sig.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
    const valid = await crypto.subtle.verify('HMAC', key, sigBuf, new TextEncoder().encode(data));
    if (!valid) return null;
    const payload = JSON.parse(atob(body.replace(/-/g, '+').replace(/_/g, '/')));
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch { return null; }
}

async function getAuthUser(request, env) {
  const auth = request.headers.get('Authorization') || '';
  // También aceptar de cookie
  const cookie = request.headers.get('Cookie') || '';
  const cookieToken = cookie.split(';').map(c => c.trim()).find(c => c.startsWith('wachi_token='));
  const token = auth.replace('Bearer ', '') || (cookieToken ? cookieToken.split('=')[1] : '');
  if (!token) return null;
  return verify(token, env.JWT_SECRET || 'wachicargo_secret_dev_change_me');
}

// ─── Email via Resend (resend.com) ───────────────────────────────────────────
// Docs: https://resend.com/docs/api-reference/emails/send-email
// Requiere la variable de entorno RESEND_API_KEY en Cloudflare Dashboard.

async function sendEmail(env, to, subject, text, html = null, attachments = null, bcc = null) {
  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    console.warn('[Resend] RESEND_API_KEY no configurada. Email no enviado.');
    return { ok: false, error: 'RESEND_API_KEY no configurada' };
  }

  const fromEmail = env.FROM_EMAIL || 'noreply@wachicargo.site';

  const body = {
    from: `MANU JUNGLE FOREVER <${fromEmail}>`,
    to: [to],
    subject,
    text,
  };
  if (html) body.html = html;
  if (attachments) body.attachments = attachments;
  if (bcc) body.bcc = Array.isArray(bcc) ? bcc : [bcc];

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) {
      console.error('[Resend] Error al enviar email:', JSON.stringify(data));
      return { ok: false, error: data.message || 'Error Resend' };
    }
    return { ok: true, id: data.id };
  } catch (e) {
    console.error('[Resend] Excepción:', e.message);
    return { ok: false, error: e.message };
  }
}

// ─── Router principal ────────────────────────────────────────────────────────

export async function onRequest(context) {
  const { request, env } = context;

  // Preflight CORS
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  const url = new URL(request.url);
  const path = url.pathname.replace(/\/$/, ''); // strip trailing slash

  // ── POST /api/auth/login ──────────────────────────────────────────────────
  if (path === '/api/auth/login' && request.method === 'POST') {
    const { usuario, password } = await request.json().catch(() => ({}));
    if (!usuario || !password) return error('Campos requeridos');

    const row = await env.DB.prepare('SELECT id, password, sucursal, rol FROM usuarios WHERE usuario = ?')
      .bind(usuario.trim()).first();

    if (!row) return error('Credenciales incorrectas', 401);

    const valid = await verifyPassword(password, row.password);
    if (!valid) return error('Credenciales incorrectas', 401);

    const secret = env.JWT_SECRET || 'wachicargo_secret_dev_change_me';
    const token = await sign({ sub: row.id, usr: usuario, exp: Math.floor(Date.now() / 1000) + 86400 * 7 }, secret);

    const res = json({ ok: true, token, usuario, sucursal: row.sucursal, rol: row.rol });
    res.headers.append('Set-Cookie', `wachi_token=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=604800`);
    return res;
  }

  // ── POST /api/auth/register ───────────────────────────────────────────────
  if (path === '/api/auth/register' && request.method === 'POST') {
    // Solo permitir registro si hay un admin autenticado
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { usuario, password, sucursal, rol } = await request.json().catch(() => ({}));
    if (!usuario || !password) return error('Campos requeridos');
    if (password.length < 8) return error('La contraseña debe tener al menos 8 caracteres');

    const hashed = await hashPassword(password);
    const sucursalVal = sucursal || 'TODOS';
    const rolVal = rol || 'operador';
    try {
      await env.DB.prepare('INSERT INTO usuarios (usuario, password, sucursal, rol) VALUES (?, ?, ?, ?)')
        .bind(usuario.trim(), hashed, sucursalVal, rolVal).run();
      return json({ ok: true, mensaje: 'Usuario creado correctamente' });
    } catch {
      return error('El nombre de usuario ya existe', 409);
    }
  }

  // ── GET /api/auth/me ──────────────────────────────────────────────────────
  if (path === '/api/auth/me' && request.method === 'GET') {
    const user = await getAuthUser(request, env);
    if (!user) return error('No autorizado', 401);
    const row = await env.DB.prepare('SELECT sucursal, rol FROM usuarios WHERE id = ?').bind(user.sub).first();
    return json({ ok: true, usuario: user.usr, sucursal: row ? row.sucursal : 'TODOS', rol: row ? row.rol : 'operador' });
  }

  // ── POST /api/auth/logout ─────────────────────────────────────────────────
  if (path === '/api/auth/logout' && request.method === 'POST') {
    const res = json({ ok: true });
    res.headers.append('Set-Cookie', 'wachi_token=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax');
    return res;
  }

  // ── GET /api/usuarios (admin - listar todos) ──────────────────────────────
  if (path === '/api/usuarios' && request.method === 'GET') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const { results } = await env.DB.prepare(
      'SELECT id, usuario, sucursal, rol, creado_en FROM usuarios ORDER BY creado_en DESC'
    ).all();
    return json({ ok: true, usuarios: results });
  }

  // ── PUT /api/usuarios/:id (admin - cambiar contraseña) ────────────────────
  const putUserMatch = path.match(/^\/api\/usuarios\/(\d+)$/);
  if (putUserMatch && request.method === 'PUT') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const id = parseInt(putUserMatch[1]);
    const body = await request.json().catch(() => ({}));

    // Si envían contraseña, actualizar ambos. Si no, solo sucursal y rol
    let result;
    const rolVal = body.rol || 'operador';
    const sucursalVal = body.sucursal || 'TODOS';

    if (body.password) {
      if (body.password.length < 8) return error('La contraseña debe tener al menos 8 caracteres');
      const hashed = await hashPassword(body.password);
      result = await env.DB.prepare('UPDATE usuarios SET password = ?, sucursal = ?, rol = ? WHERE id = ?')
        .bind(hashed, sucursalVal, rolVal, id).run();
    } else {
      result = await env.DB.prepare('UPDATE usuarios SET sucursal = ?, rol = ? WHERE id = ?')
        .bind(sucursalVal, rolVal, id).run();
    }

    if (!result.success) return error('Usuario no encontrado o error de bd', 404);
    return json({ ok: true });
  }

  // ── DELETE /api/usuarios/:id (admin - eliminar) ───────────────────────────
  const delUserMatch = path.match(/^\/api\/usuarios\/(\d+)$/);
  if (delUserMatch && request.method === 'DELETE') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const id = parseInt(delUserMatch[1]);
    const target = await env.DB.prepare('SELECT usuario FROM usuarios WHERE id = ?').bind(id).first();
    if (!target) return error('Usuario no encontrado', 404);
    if (target.usuario === admin.usr) return error('No puedes eliminar tu propia cuenta', 403);
    await env.DB.prepare('DELETE FROM usuarios WHERE id = ?').bind(id).run();
    return json({ ok: true });
  }

  // ── GET /api/rastreo?codigo=XXX ──────────────────────────────────────────
  if (path === '/api/rastreo' && request.method === 'GET') {
    const codigo = url.searchParams.get('codigo');
    if (!codigo) return error('Código de rastreo requerido');

    const paquete = await env.DB.prepare(
      'SELECT * FROM paquetes WHERE codigo_rastreo = ?'
    ).bind(codigo.trim().toUpperCase()).first();

    if (!paquete) return json({ ok: false, error: 'Código no encontrado' }, 404);

    const eventos = await env.DB.prepare(
      'SELECT estado, ubicacion, descripcion, fecha FROM tracking_events WHERE paquete_id = ? ORDER BY fecha DESC'
    ).bind(paquete.id).all();

    return json({ ok: true, paquete, historial: eventos.results });
  }

  // ── GET /api/paquetes (admin) ─────────────────────────────────────────────
  if (path === '/api/paquetes' && request.method === 'GET') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { results } = await env.DB.prepare(
      'SELECT * FROM paquetes ORDER BY fecha_actualizacion DESC'
    ).all();
    return json({ ok: true, paquetes: results });
  }

  // ── POST /api/paquetes (admin - crear) ────────────────────────────────────
  if (path === '/api/paquetes' && request.method === 'POST') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga } =
      await request.json().catch(() => ({}));

    if (!codigo_rastreo) return error('Código de rastreo requerido');

    try {
      const result = await env.DB.prepare(
        `INSERT INTO paquetes (codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga, fecha_actualizacion)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))`
      ).bind(
        codigo_rastreo.trim().toUpperCase(),
        estado || 'Pendiente',
        ubicacion_actual || '',
        embarcador || '',
        celular || '',
        origen || '',
        destino || '',
        destinatario || '',
        direccion_destino || '',
        descripcion || '',
        peso_kg || null,
        bultos || 1,
        tipo_carga || 'Carga General'
      ).run();

      if (!result.success) return error('Error al crear el paquete');

      // Obtener el paquete recién creado para devolverlo completo
      const newPkg = await env.DB.prepare("SELECT * FROM paquetes WHERE id = ?").bind(result.meta.last_row_id).first();

      // Registrar evento inicial
      await env.DB.prepare(
        `INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)`
      ).bind(newPkg.id, estado || 'Pendiente', ubicacion_actual || '', 'Paquete registrado en el sistema').run();

      return json({ ok: true, paquete: newPkg }, 201);
    } catch (e) {
      if (e.message && e.message.includes('UNIQUE')) return error('El código de rastreo ya existe', 409);
      return error('Error al crear el paquete: ' + e.message, 500);
    }
  }

  // ── PUT /api/paquetes/:id (admin - actualizar) ────────────────────────────
  const putMatch = path.match(/^\/api\/paquetes\/(\d+)$/);
  if (putMatch && request.method === 'PUT') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const id = parseInt(putMatch[1]);
    const { codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga } =
      await request.json().catch(() => ({}));

    const existing = await env.DB.prepare('SELECT id, estado FROM paquetes WHERE id = ?').bind(id).first();
    if (!existing) return error('Paquete no encontrado', 404);

    await env.DB.prepare(
      `UPDATE paquetes SET codigo_rastreo=?, estado=?, ubicacion_actual=?, embarcador=?, celular=?, origen=?, destino=?, destinatario=?, direccion_destino=?,
       descripcion=?, peso_kg=?, bultos=?, tipo_carga=?, fecha_actualizacion=datetime('now') WHERE id=?`
    ).bind(
      codigo_rastreo?.trim().toUpperCase() || existing.codigo_rastreo,
      estado || existing.estado,
      ubicacion_actual ?? '',
      embarcador ?? '',
      celular ?? '',
      origen ?? '',
      destino ?? '',
      destinatario ?? '',
      direccion_destino ?? '',
      descripcion ?? '',
      peso_kg ?? null,
      bultos ?? 1,
      tipo_carga ?? 'Carga General',
      id
    ).run();

    // Si el estado cambió, registrar evento de tracking
    if (estado && estado !== existing.estado) {
      await env.DB.prepare(
        `INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)`
      ).bind(id, estado, ubicacion_actual || '', `Estado actualizado a: ${estado}`).run();
    }

    return json({ ok: true, mensaje: 'Paquete actualizado' });
  }

  // ── DELETE /api/paquetes/:id (admin) ──────────────────────────────────────
  const delMatch = path.match(/^\/api\/paquetes\/(\d+)$/);
  if (delMatch && request.method === 'DELETE') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const id = parseInt(delMatch[1]);
    const existing = await env.DB.prepare('SELECT id FROM paquetes WHERE id = ?').bind(id).first();
    if (!existing) return error('Paquete no encontrado', 404);

    await env.DB.prepare('DELETE FROM paquetes WHERE id = ?').bind(id).run();
    return json({ ok: true, mensaje: 'Paquete eliminado' });
  }

  // ── POST /api/paquetes/batch (admin - actualización masiva) ──────────────
  if (path === '/api/paquetes/batch' && request.method === 'POST') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { ids, estado, ubicacion_actual, actualizaciones } = await request.json().catch(() => ({}));

    const statements = [];

    if (actualizaciones && Array.isArray(actualizaciones) && actualizaciones.length > 0) {
      // Formato nuevo: cada paquete trae su propia ubicación
      for (const item of actualizaciones) {
        statements.push(
          env.DB.prepare("UPDATE paquetes SET estado=?, ubicacion_actual=?, fecha_actualizacion=datetime('now') WHERE id=?")
            .bind(item.estado, item.ubicacion_actual || '', item.id)
        );
        statements.push(
          env.DB.prepare("INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)")
            .bind(item.id, item.estado, item.ubicacion_actual || '', `Actualización masiva: ${item.estado}`)
        );
      }
    } else {
      // Formato antiguo: lista de IDs
      if (!ids || !Array.isArray(ids) || ids.length === 0) return error('Lista de IDs o actualizaciones requerida');
      for (const id of ids) {
        statements.push(
          env.DB.prepare("UPDATE paquetes SET estado=?, ubicacion_actual=?, fecha_actualizacion=datetime('now') WHERE id=?")
            .bind(estado, ubicacion_actual || '', id)
        );
        statements.push(
          env.DB.prepare("INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)")
            .bind(id, estado, ubicacion_actual || '', `Actualización masiva: ${estado}`)
        );
      }
    }

    await env.DB.batch(statements);
    const count = actualizaciones ? actualizaciones.length : ids.length;
    return json({ ok: true, mensaje: `${count} paquetes actualizados correctamente` });
  }

  // ── POST /api/contacto ────────────────────────────────────────────────────
  if (path === '/api/contacto' && request.method === 'POST') {
    const { nombre, email, asunto, mensaje } = await request.json().catch(() => ({}));
    if (!nombre || !email || !mensaje) return error('Campos requeridos');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return error('Email inválido');

    // Guardar en D1
    await env.DB.prepare(
      'INSERT INTO contactos (nombre, email, asunto, mensaje) VALUES (?, ?, ?, ?)'
    ).bind(nombre.trim(), email.trim(), asunto?.trim() || 'Sin asunto', mensaje.trim()).run();

    // Enviar email interno via Resend
    const toEmail = env.TO_EMAIL || 'ventas@wachicargo.site';
    const emailText = [
      'NUEVO MENSAJE DE CONTACTO - MANU JUNGLE FOREVER',
      '=======================================',
      `Nombre:  ${nombre}`,
      `Email:   ${email}`,
      `Asunto:  ${asunto || 'Sin asunto'}`,
      '',
      'Mensaje:',
      mensaje,
    ].join('\n');

    const emailHtml = `
      <h2 style="color:#38bdf8;font-family:sans-serif">Nuevo mensaje de contacto</h2>
      <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse;width:100%">
        <tr><td style="padding:6px 12px;color:#666"><b>Nombre</b></td><td style="padding:6px 12px">${nombre}</td></tr>
        <tr style="background:#f9f9f9"><td style="padding:6px 12px;color:#666"><b>Email</b></td><td style="padding:6px 12px"><a href="mailto:${email}">${email}</a></td></tr>
        <tr><td style="padding:6px 12px;color:#666"><b>Asunto</b></td><td style="padding:6px 12px">${asunto || 'Sin asunto'}</td></tr>
        <tr style="background:#f9f9f9"><td style="padding:6px 12px;color:#666;vertical-align:top"><b>Mensaje</b></td><td style="padding:6px 12px;white-space:pre-wrap">${mensaje}</td></tr>
      </table>
      <p style="font-size:12px;color:#999;font-family:sans-serif;margin-top:24px">MANU JUNGLE FOREVER · ventas@wachicargo.site</p>
    `;

    await sendEmail(env, 'ventas+cotizaciones_wachicargo@wachicargo.site', `[CONTACTO] ${asunto || nombre}`, emailText, emailHtml);

    return json({ ok: true, mensaje: 'Mensaje enviado correctamente' });
  }

  // ── POST /api/reclamo ─────────────────────────────────────────────────────
  if (path === '/api/reclamo' && request.method === 'POST') {
    const { nombres, documento, domicilio, telefono, correo, apoderado, bien_tipo, bien_monto, bien_descripcion, tipo, detalle, pedido, honeypot } =
      await request.json().catch(() => ({}));

    // Anti-bot
    if (honeypot) return error('Validación fallida', 400);
    if (!nombres || !documento || !domicilio || !telefono || !correo || !bien_tipo || !bien_descripcion || !detalle || !pedido) {
      return error('Faltan campos obligatorios');
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) return error('Correo electrónico inválido');

    const anio = new Date().getFullYear();
    const countRes = await env.DB.prepare('SELECT COUNT(*) as c FROM reclamaciones WHERE fecha LIKE ?').bind(`${anio}-%`).first();
    const num = countRes ? countRes.c + 1 : 1;
    const codigo_reclamo = `${anio}-${String(num).padStart(6, '0')}`;
    const fecha = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    // Guardar en D1
    await env.DB.prepare(
      `INSERT INTO reclamaciones (codigo_reclamo, nombres, documento, telefono, correo, tipo, detalle, domicilio, apoderado, bien_tipo, bien_monto, bien_descripcion, pedido)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      codigo_reclamo, nombres.trim(), documento.trim(), telefono.trim(), correo.trim(), tipo || 'Reclamo', detalle.trim(),
      domicilio.trim(), (apoderado || '').trim(), bien_tipo.trim(), (bien_monto || '').trim(), bien_descripcion.trim(), pedido.trim()
    ).run();

    // Generar PDF
    const dataObj = { codigo_reclamo, fecha, nombres, documento, domicilio, telefono, correo, apoderado, bien_tipo, bien_monto, bien_descripcion, tipo: tipo || 'Reclamo', detalle, pedido };
    let pdfBytes = null;
    let pdfFileName = `${codigo_reclamo}.pdf`;
    try {
      pdfBytes = await generateReclamoPDF(dataObj);
      // Subir a R2
      if (env.R2_RECLAMOS) {
        await env.R2_RECLAMOS.put(pdfFileName, pdfBytes, { httpMetadata: { contentType: 'application/pdf' } });
      }
    } catch(err) {
      console.error('Error generando PDF:', err);
    }

    // Email a la empresa
    const msgEmpresa = `
NUEVO ${(tipo || 'RECLAMO').toUpperCase()} - LIBRO DE RECLAMACIONES
====================================================================
N°:    ${codigo_reclamo}
FECHA: ${fecha}

--- 1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE ---
Nombres:   ${nombres}
DNI/CE:    ${documento}
Domicilio: ${domicilio}
Teléfono:  ${telefono}
Correo:    ${correo}
Padre/Madre/Apoderado: ${apoderado || 'N/A'}

--- 2. IDENTIFICACIÓN DEL BIEN CONTRATADO ---
Tipo:        ${bien_tipo}
Monto (S/):  ${bien_monto || '0.00'}
Descripción: ${bien_descripcion}

--- 3. DETALLE DE LA RECLAMACIÓN Y PEDIDO DEL CONSUMIDOR ---
Tipo:    ${tipo}
Detalle:
${detalle}

Pedido:
${pedido}

Atender en máximo 15 días hábiles conforme a Ley N° 29571.
    `.trim();

    let attachments = null;
    if (pdfBytes) {
      let binary = '';
      for (let i = 0; i < pdfBytes.length; i++) binary += String.fromCharCode(pdfBytes[i]);
      const base64Pdf = btoa(binary);
      attachments = [{ filename: pdfFileName, content: base64Pdf }];
    }

    const toEmail = 'ventas+reclamos_wachicargo@wachicargo.site';
    await sendEmail(env, toEmail, `[${(tipo || 'RECLAMO').toUpperCase()}] ${codigo_reclamo}`, msgEmpresa,
      `<div style="font-family:sans-serif;max-width:800px;margin:0 auto;border:1px solid #ccc;padding:20px;">
        <h2 style="color:#e53e3e;text-align:center;border-bottom:2px solid #e53e3e;padding-bottom:10px;margin-bottom:10px;">HOJA DE RECLAMACIÓN - N° ${codigo_reclamo}</h2>
        <div style="text-align:center;font-size:12px;color:#555;margin-bottom:20px;">
            <b>Razón Social:</b> MANU JUNGLE FOREVER E.I.R.L. | <b>RUC:</b> 20610333283<br>
            <b>Domicilio Fiscal:</b> Fitzcarrald 17800, Nuevo Eden, Manu, Peru
        </div>
        <p style="text-align:right"><b>Fecha:</b> ${fecha}</p>

        <h3 style="background:#f0f0f0;padding:5px">1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Nombres:</td><td style="padding:5px">${nombres}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">DNI / CE:</td><td style="padding:5px">${documento}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Domicilio:</td><td style="padding:5px">${domicilio}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Teléfono:</td><td style="padding:5px">${telefono}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Correo:</td><td style="padding:5px">${correo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Padre/Madre:</td><td style="padding:5px">${apoderado || 'N/A'}</td></tr>
        </table>

        <h3 style="background:#f0f0f0;padding:5px">2. IDENTIFICACIÓN DEL BIEN CONTRATADO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Tipo:</td><td style="padding:5px">${bien_tipo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Monto Reclamado:</td><td style="padding:5px">S/ ${bien_monto || '0.00'}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Descripción:</td><td style="padding:5px">${bien_descripcion}</td></tr>
        </table>

        <h3 style="background:#f0f0f0;padding:5px">3. DETALLE DE LA RECLAMACIÓN Y PEDIDO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Tipo:</td><td style="padding:5px">${tipo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Detalle:</td><td style="padding:5px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${detalle}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Pedido:</td><td style="padding:5px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${pedido}</td></tr>
        </table>
        
        <p style="font-size:12px;color:#e53e3e;text-align:center;margin-top:20px;font-weight:bold;">El plazo de atención es de 15 días hábiles conforme a Ley N° 29571.</p>
       </div>`, attachments, 'ventas+reclamos_wachicargo@wachicargo.site'
    );

    // Email cargo al cliente (obligatorio INDECOPI)
    const msgClienteHtml = `
      <div style="font-family:sans-serif;max-width:800px;margin:0 auto;border:1px solid #ccc;padding:20px;">
        <h2 style="color:#e53e3e;text-align:center;border-bottom:2px solid #e53e3e;padding-bottom:10px;margin-bottom:10px;">CARGO DE RECEPCIÓN: HOJA DE RECLAMACIÓN - N° ${codigo_reclamo}</h2>
        <div style="text-align:center;font-size:12px;color:#555;margin-bottom:20px;">
            <b>Razón Social:</b> MANU JUNGLE FOREVER E.I.R.L. | <b>RUC:</b> 20610333283<br>
            <b>Domicilio Fiscal:</b> Fitzcarrald 17800, Nuevo Eden, Manu, Peru
        </div>
        <p>Estimado(a) <b>${nombres}</b>,</p>
        <p>Hemos recibido su <b>${tipo}</b> a través del Libro de Reclamaciones Virtual de MANU JUNGLE FOREVER.</p>
        <p style="text-align:right"><b>Fecha de Ingreso:</b> ${fecha}</p>

        <h3 style="background:#f0f0f0;padding:5px">COPIA DE SU REGISTRO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Nombres:</td><td style="padding:4px">${nombres}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">DNI / CE:</td><td style="padding:4px">${documento}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Domicilio:</td><td style="padding:4px">${domicilio}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Teléfono:</td><td style="padding:4px">${telefono}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Correo:</td><td style="padding:4px">${correo}</td></tr>
        </table>

        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Bien Contratado:</td><td style="padding:4px">${bien_tipo}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Monto:</td><td style="padding:4px">S/ ${bien_monto || '0.00'}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Descripción Bien:</td><td style="padding:4px">${bien_descripcion}</td></tr>
        </table>

        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Tipo:</td><td style="padding:4px">${tipo}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Detalle:</td><td style="padding:4px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${detalle}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Pedido:</td><td style="padding:4px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${pedido}</td></tr>
        </table>

        <div style="background:#fff3cd;border:1px solid #ffeeba;padding:15px;margin-top:20px;border-radius:5px">
            <h4 style="margin-top:0;color:#856404;">Aviso Legal (Ley N° 29571)</h4>
            <p style="margin-bottom:0;color:#856404;font-size:13px;">La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.<br><br><b>MANU JUNGLE FOREVER</b> cuenta con un plazo máximo de <b>quince (15) días hábiles</b> improrrogables para atender su solicitud y emitir una respuesta formal a su correo electrónico.</p>
        </div>
        <p style="text-align:center;font-size:12px;color:#999;margin-top:20px">Atentamente,<br><b>MANU JUNGLE FOREVER E.I.R.L.</b></p>
      </div>
    `;
    // Convert PDF bytes to Base64 for Resend
    let attachments2 = null;
    if (pdfBytes) {
      let binary = '';
      for (let i = 0; i < pdfBytes.length; i++) binary += String.fromCharCode(pdfBytes[i]);
      const base64Pdf = btoa(binary);
      attachments2 = [{ filename: pdfFileName, content: base64Pdf }];
    }

    // Send email to client
    await sendEmail(env, correo, `Cargo de Recepción - Hoja de Reclamación N° ${codigo_reclamo}`, 'Su cliente de correo no soporta HTML. Por favor, revise el adjunto.', msgClienteHtml, attachments2);

    return json({ ok: true, codigo_reclamo, mensaje: 'Reclamo registrado correctamente' });
  }

  // ── PANEL ADMIN / RECLAMACIONES ───────────────────────────────────────────
  if (path.startsWith('/api/admin/')) {
    // 1. JWT Auth Middleware (Only for Admins)
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = (dbAdmin && dbAdmin.rol === 'admin') || (admin && admin.usr === 'admin');
    if (!isAdmin) {
      return error('No autorizado (requiere rol admin)', 401);
    }

    const urlObj = new URL(request.url);
    const tipo = urlObj.searchParams.get('tipo');
    const buscar = urlObj.searchParams.get('buscar');
    const desde = urlObj.searchParams.get('desde');
    const hasta = urlObj.searchParams.get('hasta');

    let baseQuery = 'SELECT * FROM reclamaciones WHERE 1=1';
    let params = [];

    if (tipo && tipo !== 'Todos') {
      baseQuery += ' AND tipo = ?';
      params.push(tipo);
    }
    if (buscar) {
      baseQuery += ' AND (codigo_reclamo LIKE ? OR nombres LIKE ? OR documento LIKE ?)';
      params.push(`%${buscar}%`, `%${buscar}%`, `%${buscar}%`);
    }
    if (desde) {
      baseQuery += ' AND date(fecha) >= date(?)';
      params.push(desde);
    }
    if (hasta) {
      baseQuery += ' AND date(fecha) <= date(?)';
      params.push(hasta);
    }
    baseQuery += ' ORDER BY fecha DESC';

    const getResults = async () => {
      const stmt = env.DB.prepare(baseQuery);
      return await (params.length > 0 ? stmt.bind(...params) : stmt).all();
    };

    // ── GET /api/admin/reclamos (JSON) ──
    if (path === '/api/admin/reclamos' && request.method === 'GET') {
      const { results } = await getResults();
      return json(results);
    }

    // ── GET /api/admin/exportar (CSV) ──
    if (path === '/api/admin/exportar' && request.method === 'GET') {
      const { results } = await getResults();
      
      let csvContent = '\uFEFF'; // UTF-8 BOM
      csvContent += 'ID,Código,Fecha,Nombres,DNI/CE,Domicilio,Teléfono,Correo,Apoderado,Tipo Bien,Monto Bien,Desc. Bien,Tipo Reclamo/Queja,Detalle,Pedido,Estado\n';
      
      for (const r of results) {
        const row = [
          r.id, r.codigo_reclamo, r.fecha, r.nombres, r.documento, r.domicilio || '', r.telefono, r.correo, 
          r.apoderado || '', r.bien_tipo || '', r.bien_monto || '', r.bien_descripcion || '', r.tipo, r.detalle, r.pedido || '', r.estado
        ].map(col => {
          let str = String(col || '');
          if (str.includes(',') || str.includes('\n') || str.includes('"')) {
            str = `"${str.replace(/"/g, '""')}"`;
          }
          return str;
        }).join(',');
        csvContent += row + '\n';
      }

      return new Response(csvContent, {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="reporte-reclamaciones.csv"',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // ── GET /api/admin/reclamos/:codigo/pdf ──
    const pdfMatch = path.match(/^\/api\/admin\/reclamos\/(.+)\/pdf$/);
    if (pdfMatch && request.method === 'GET') {
      const codigo = pdfMatch[1];
      if (!env.R2_RECLAMOS) return error('R2 no configurado', 500);
      
      const object = await env.R2_RECLAMOS.get(`${codigo}.pdf`);
      if (!object) return error('PDF no encontrado', 404);

      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set('etag', object.httpEtag);
      headers.set('Access-Control-Allow-Origin', '*');
      headers.set('Content-Disposition', `attachment; filename="${codigo}.pdf"`);

      return new Response(object.body, { headers });
    }

    // ── PUT /api/admin/reclamos/:id/atender ──
    const atenderMatch = path.match(/^\/api\/admin\/reclamos\/(\d+)\/atender$/);
    if (atenderMatch && request.method === 'PUT') {
      const id = parseInt(atenderMatch[1]);
      const { detalle_respuesta } = await request.json().catch(() => ({}));

      if (!detalle_respuesta || !detalle_respuesta.trim()) {
        return error('El detalle de la respuesta es obligatorio');
      }

      // Obtener el reclamo actual
      const reclamo = await env.DB.prepare(
        'SELECT * FROM reclamaciones WHERE id = ?'
      ).bind(id).first();

      if (!reclamo) return error('Reclamo no encontrado', 404);
      if (reclamo.estado === 'Atendido') return error('Este reclamo ya fue atendido', 409);

      // Actualizar D1
      await env.DB.prepare(
        `UPDATE reclamaciones 
         SET estado = 'Atendido', 
             detalle_respuesta = ?, 
             fecha_respuesta = datetime('now')
         WHERE id = ?`
      ).bind(detalle_respuesta.trim(), id).run();

      // 1. Email de respuesta al cliente (sin BCC)
      const fechaRespuesta = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

      const htmlRespuesta = `
        <div style="font-family:sans-serif;max-width:700px;margin:0 auto;border:1px solid #ccc;padding:24px;border-radius:8px">
          <div style="text-align:center;border-bottom:2px solid #38bdf8;padding-bottom:16px;margin-bottom:20px">
            <h2 style="color:#38bdf8;margin:0">MANU JUNGLE FOREVER</h2>
            <p style="color:#555;font-size:13px;margin:4px 0">MANU JUNGLE FOREVER E.I.R.L. | RUC: 20610333283</p>
            <h3 style="color:#1e293b;margin:8px 0">RESPUESTA OFICIAL A SU ${reclamo.tipo.toUpperCase()}</h3>
            <p style="font-size:13px;color:#555">N° ${reclamo.codigo_reclamo} | Respondido el: ${fechaRespuesta}</p>
          </div>

          <p style="font-size:15px">Estimado(a) <strong>${reclamo.nombres}</strong>,</p>
          <p style="font-size:14px;color:#444">Hemos analizado su ${reclamo.tipo.toLowerCase()} registrado en nuestro Libro de Reclamaciones Virtual y procedemos a darle respuesta formal conforme a la Ley N° 29571.</p>

          <div style="background:#f0f9ff;border-left:4px solid #38bdf8;padding:16px;margin:20px 0;border-radius:0 8px 8px 0">
            <h4 style="margin:0 0 8px;color:#0369a1">RESPUESTA DE MANU JUNGLE FOREVER:</h4>
            <p style="margin:0;white-space:pre-wrap;font-size:14px;color:#1e293b">${detalle_respuesta.trim()}</p>
          </div>

          <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:16px">
            <tr style="background:#f8fafc">
              <td style="padding:8px 12px;font-weight:bold;width:40%">Su Reclamo N°:</td>
              <td style="padding:8px 12px">${reclamo.codigo_reclamo}</td>
            </tr>
            <tr>
              <td style="padding:8px 12px;font-weight:bold">Tipo:</td>
              <td style="padding:8px 12px">${reclamo.tipo}</td>
            </tr>
            <tr style="background:#f8fafc">
              <td style="padding:8px 12px;font-weight:bold">Fecha de Ingreso:</td>
              <td style="padding:8px 12px">${reclamo.fecha}</td>
            </tr>
            <tr>
              <td style="padding:8px 12px;font-weight:bold">Fecha de Respuesta:</td>
              <td style="padding:8px 12px">${fechaRespuesta}</td>
            </tr>
          </table>

          <div style="background:#fefce8;border:1px solid #fde68a;padding:14px;margin-top:20px;border-radius:6px;font-size:12px;color:#78350f">
            <strong>Aviso Legal:</strong> Si no queda satisfecho con esta respuesta, puede acudir al INDECOPI u otras vías de solución de controversias. La formulación del reclamo no es requisito previo para interponer una denuncia ante el INDECOPI.
          </div>

          <p style="text-align:center;font-size:12px;color:#999;margin-top:24px">Atentamente,<br><strong>MANU JUNGLE FOREVER E.I.R.L.</strong><br>ventas@wachicargo.site | +51 925 247 920</p>
        </div>
      `;

      await sendEmail(
        env,
        reclamo.correo,
        `Respuesta a su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} - MANU JUNGLE FOREVER`,
        `Estimado(a) ${reclamo.nombres}, le comunicamos que su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} ha sido atendido. Respuesta: ${detalle_respuesta.trim()}`,
        htmlRespuesta
      );

      // 2. Email copia a la empresa enviado directamente al alias con etiqueta para que el filtro de Zoho lo mueva
      await sendEmail(
        env,
        'ventas+reclamos_wachicargo@wachicargo.site',
        `[COPIA ATENCIÓN] Respuesta a su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} - MANU JUNGLE FOREVER`,
        `Copia de respuesta oficial enviada al cliente ${reclamo.nombres} (${reclamo.correo}). Respuesta: ${detalle_respuesta.trim()}`,
        htmlRespuesta
      );

      return json({ ok: true, mensaje: `${reclamo.tipo} marcado como Atendido y correo enviado al cliente.` });
    }

    return error('Admin endpoint not found', 404);
  }

  // ── 404 ───────────────────────────────────────────────────────────────────
  return error('Ruta no encontrada', 404);
}

async function sendEmail(env, to, subject, text, html = null, attachments = null, bcc = null) {
  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    console.warn('[Resend] RESEND_API_KEY no configurada. Email no enviado.');
    return { ok: false, error: 'RESEND_API_KEY no configurada' };
  }

  const fromEmail = env.FROM_EMAIL || 'noreply@wachicargo.site';

  const body = {
    from: `WACHICARGO <${fromEmail}>`,
    to: [to],
    subject,
    text,
  };
  if (html) body.html = html;
  if (attachments) body.attachments = attachments;
  if (bcc) body.bcc = Array.isArray(bcc) ? bcc : [bcc];

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) {
      console.error('[Resend] Error al enviar email:', JSON.stringify(data));
      return { ok: false, error: data.message || 'Error Resend' };
    }
    return { ok: true, id: data.id };
  } catch (e) {
    console.error('[Resend] Excepción:', e.message);
    return { ok: false, error: e.message };
  }
}

// ─── Router principal ────────────────────────────────────────────────────────

export async function onRequest(context) {
  const { request, env } = context;

  // Preflight CORS
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  const url = new URL(request.url);
  const path = url.pathname.replace(/\/$/, ''); // strip trailing slash

  // ── POST /api/auth/login ──────────────────────────────────────────────────
  if (path === '/api/auth/login' && request.method === 'POST') {
    const { usuario, password } = await request.json().catch(() => ({}));
    if (!usuario || !password) return error('Campos requeridos');

    const row = await env.DB.prepare('SELECT id, password, sucursal, rol FROM usuarios WHERE usuario = ?')
      .bind(usuario.trim()).first();

    if (!row) return error('Credenciales incorrectas', 401);

    const valid = await verifyPassword(password, row.password);
    if (!valid) return error('Credenciales incorrectas', 401);

    const secret = env.JWT_SECRET || 'wachicargo_secret_dev_change_me';
    const token = await sign({ sub: row.id, usr: usuario, exp: Math.floor(Date.now() / 1000) + 86400 * 7 }, secret);

    const res = json({ ok: true, token, usuario, sucursal: row.sucursal, rol: row.rol });
    res.headers.append('Set-Cookie', `wachi_token=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=604800`);
    return res;
  }

  // ── POST /api/auth/register ───────────────────────────────────────────────
  if (path === '/api/auth/register' && request.method === 'POST') {
    // Solo permitir registro si hay un admin autenticado
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { usuario, password, sucursal, rol } = await request.json().catch(() => ({}));
    if (!usuario || !password) return error('Campos requeridos');
    if (password.length < 8) return error('La contraseña debe tener al menos 8 caracteres');

    const hashed = await hashPassword(password);
    const sucursalVal = sucursal || 'TODOS';
    const rolVal = rol || 'operador';
    try {
      await env.DB.prepare('INSERT INTO usuarios (usuario, password, sucursal, rol) VALUES (?, ?, ?, ?)')
        .bind(usuario.trim(), hashed, sucursalVal, rolVal).run();
      return json({ ok: true, mensaje: 'Usuario creado correctamente' });
    } catch {
      return error('El nombre de usuario ya existe', 409);
    }
  }

  // ── GET /api/auth/me ──────────────────────────────────────────────────────
  if (path === '/api/auth/me' && request.method === 'GET') {
    const user = await getAuthUser(request, env);
    if (!user) return error('No autorizado', 401);
    const row = await env.DB.prepare('SELECT sucursal, rol FROM usuarios WHERE id = ?').bind(user.sub).first();
    return json({ ok: true, usuario: user.usr, sucursal: row ? row.sucursal : 'TODOS', rol: row ? row.rol : 'operador' });
  }

  // ── POST /api/auth/logout ─────────────────────────────────────────────────
  if (path === '/api/auth/logout' && request.method === 'POST') {
    const res = json({ ok: true });
    res.headers.append('Set-Cookie', 'wachi_token=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax');
    return res;
  }

  // ── GET /api/usuarios (admin - listar todos) ──────────────────────────────
  if (path === '/api/usuarios' && request.method === 'GET') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const { results } = await env.DB.prepare(
      'SELECT id, usuario, sucursal, rol, creado_en FROM usuarios ORDER BY creado_en DESC'
    ).all();
    return json({ ok: true, usuarios: results });
  }

  // ── PUT /api/usuarios/:id (admin - cambiar contraseña) ────────────────────
  const putUserMatch = path.match(/^\/api\/usuarios\/(\d+)$/);
  if (putUserMatch && request.method === 'PUT') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const id = parseInt(putUserMatch[1]);
    const body = await request.json().catch(() => ({}));

    // Si envían contraseña, actualizar ambos. Si no, solo sucursal y rol
    let result;
    const rolVal = body.rol || 'operador';
    const sucursalVal = body.sucursal || 'TODOS';

    if (body.password) {
      if (body.password.length < 8) return error('La contraseña debe tener al menos 8 caracteres');
      const hashed = await hashPassword(body.password);
      result = await env.DB.prepare('UPDATE usuarios SET password = ?, sucursal = ?, rol = ? WHERE id = ?')
        .bind(hashed, sucursalVal, rolVal, id).run();
    } else {
      result = await env.DB.prepare('UPDATE usuarios SET sucursal = ?, rol = ? WHERE id = ?')
        .bind(sucursalVal, rolVal, id).run();
    }

    if (!result.success) return error('Usuario no encontrado o error de bd', 404);
    return json({ ok: true });
  }

  // ── DELETE /api/usuarios/:id (admin - eliminar) ───────────────────────────
  const delUserMatch = path.match(/^\/api\/usuarios\/(\d+)$/);
  if (delUserMatch && request.method === 'DELETE') {
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = dbAdmin && dbAdmin.rol === 'admin' || (admin && admin.usr === 'admin');
    if (!isAdmin) return error('Acceso denegado. Solo el administrador.', 403);
    const id = parseInt(delUserMatch[1]);
    const target = await env.DB.prepare('SELECT usuario FROM usuarios WHERE id = ?').bind(id).first();
    if (!target) return error('Usuario no encontrado', 404);
    if (target.usuario === admin.usr) return error('No puedes eliminar tu propia cuenta', 403);
    await env.DB.prepare('DELETE FROM usuarios WHERE id = ?').bind(id).run();
    return json({ ok: true });
  }

  // ── GET /api/rastreo?codigo=XXX ──────────────────────────────────────────
  if (path === '/api/rastreo' && request.method === 'GET') {
    const codigo = url.searchParams.get('codigo');
    if (!codigo) return error('Código de rastreo requerido');

    const paquete = await env.DB.prepare(
      'SELECT * FROM paquetes WHERE codigo_rastreo = ?'
    ).bind(codigo.trim().toUpperCase()).first();

    if (!paquete) return json({ ok: false, error: 'Código no encontrado' }, 404);

    const eventos = await env.DB.prepare(
      'SELECT estado, ubicacion, descripcion, fecha FROM tracking_events WHERE paquete_id = ? ORDER BY fecha DESC'
    ).bind(paquete.id).all();

    return json({ ok: true, paquete, historial: eventos.results });
  }

  // ── GET /api/paquetes (admin) ─────────────────────────────────────────────
  if (path === '/api/paquetes' && request.method === 'GET') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { results } = await env.DB.prepare(
      'SELECT * FROM paquetes ORDER BY fecha_actualizacion DESC'
    ).all();
    return json({ ok: true, paquetes: results });
  }

  // ── POST /api/paquetes (admin - crear) ────────────────────────────────────
  if (path === '/api/paquetes' && request.method === 'POST') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga } =
      await request.json().catch(() => ({}));

    if (!codigo_rastreo) return error('Código de rastreo requerido');

    try {
      const result = await env.DB.prepare(
        `INSERT INTO paquetes (codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga, fecha_actualizacion)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))`
      ).bind(
        codigo_rastreo.trim().toUpperCase(),
        estado || 'Pendiente',
        ubicacion_actual || '',
        embarcador || '',
        celular || '',
        origen || '',
        destino || '',
        destinatario || '',
        direccion_destino || '',
        descripcion || '',
        peso_kg || null,
        bultos || 1,
        tipo_carga || 'Carga General'
      ).run();

      if (!result.success) return error('Error al crear el paquete');

      // Obtener el paquete recién creado para devolverlo completo
      const newPkg = await env.DB.prepare("SELECT * FROM paquetes WHERE id = ?").bind(result.meta.last_row_id).first();

      // Registrar evento inicial
      await env.DB.prepare(
        `INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)`
      ).bind(newPkg.id, estado || 'Pendiente', ubicacion_actual || '', 'Paquete registrado en el sistema').run();

      return json({ ok: true, paquete: newPkg }, 201);
    } catch (e) {
      if (e.message && e.message.includes('UNIQUE')) return error('El código de rastreo ya existe', 409);
      return error('Error al crear el paquete: ' + e.message, 500);
    }
  }

  // ── PUT /api/paquetes/:id (admin - actualizar) ────────────────────────────
  const putMatch = path.match(/^\/api\/paquetes\/(\d+)$/);
  if (putMatch && request.method === 'PUT') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const id = parseInt(putMatch[1]);
    const { codigo_rastreo, estado, ubicacion_actual, embarcador, celular, origen, destino, destinatario, direccion_destino, descripcion, peso_kg, bultos, tipo_carga } =
      await request.json().catch(() => ({}));

    const existing = await env.DB.prepare('SELECT id, estado FROM paquetes WHERE id = ?').bind(id).first();
    if (!existing) return error('Paquete no encontrado', 404);

    await env.DB.prepare(
      `UPDATE paquetes SET codigo_rastreo=?, estado=?, ubicacion_actual=?, embarcador=?, celular=?, origen=?, destino=?, destinatario=?, direccion_destino=?,
       descripcion=?, peso_kg=?, bultos=?, tipo_carga=?, fecha_actualizacion=datetime('now') WHERE id=?`
    ).bind(
      codigo_rastreo?.trim().toUpperCase() || existing.codigo_rastreo,
      estado || existing.estado,
      ubicacion_actual ?? '',
      embarcador ?? '',
      celular ?? '',
      origen ?? '',
      destino ?? '',
      destinatario ?? '',
      direccion_destino ?? '',
      descripcion ?? '',
      peso_kg ?? null,
      bultos ?? 1,
      tipo_carga ?? 'Carga General',
      id
    ).run();

    // Si el estado cambió, registrar evento de tracking
    if (estado && estado !== existing.estado) {
      await env.DB.prepare(
        `INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)`
      ).bind(id, estado, ubicacion_actual || '', `Estado actualizado a: ${estado}`).run();
    }

    return json({ ok: true, mensaje: 'Paquete actualizado' });
  }

  // ── DELETE /api/paquetes/:id (admin) ──────────────────────────────────────
  const delMatch = path.match(/^\/api\/paquetes\/(\d+)$/);
  if (delMatch && request.method === 'DELETE') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const id = parseInt(delMatch[1]);
    const existing = await env.DB.prepare('SELECT id FROM paquetes WHERE id = ?').bind(id).first();
    if (!existing) return error('Paquete no encontrado', 404);

    await env.DB.prepare('DELETE FROM paquetes WHERE id = ?').bind(id).run();
    return json({ ok: true, mensaje: 'Paquete eliminado' });
  }

  // ── POST /api/paquetes/batch (admin - actualización masiva) ──────────────
  if (path === '/api/paquetes/batch' && request.method === 'POST') {
    const admin = await getAuthUser(request, env);
    if (!admin) return error('No autorizado', 401);

    const { ids, estado, ubicacion_actual, actualizaciones } = await request.json().catch(() => ({}));

    const statements = [];

    if (actualizaciones && Array.isArray(actualizaciones) && actualizaciones.length > 0) {
      // Formato nuevo: cada paquete trae su propia ubicación
      for (const item of actualizaciones) {
        statements.push(
          env.DB.prepare("UPDATE paquetes SET estado=?, ubicacion_actual=?, fecha_actualizacion=datetime('now') WHERE id=?")
            .bind(item.estado, item.ubicacion_actual || '', item.id)
        );
        statements.push(
          env.DB.prepare("INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)")
            .bind(item.id, item.estado, item.ubicacion_actual || '', `Actualización masiva: ${item.estado}`)
        );
      }
    } else {
      // Formato antiguo: lista de IDs
      if (!ids || !Array.isArray(ids) || ids.length === 0) return error('Lista de IDs o actualizaciones requerida');
      for (const id of ids) {
        statements.push(
          env.DB.prepare("UPDATE paquetes SET estado=?, ubicacion_actual=?, fecha_actualizacion=datetime('now') WHERE id=?")
            .bind(estado, ubicacion_actual || '', id)
        );
        statements.push(
          env.DB.prepare("INSERT INTO tracking_events (paquete_id, estado, ubicacion, descripcion) VALUES (?, ?, ?, ?)")
            .bind(id, estado, ubicacion_actual || '', `Actualización masiva: ${estado}`)
        );
      }
    }

    await env.DB.batch(statements);
    const count = actualizaciones ? actualizaciones.length : ids.length;
    return json({ ok: true, mensaje: `${count} paquetes actualizados correctamente` });
  }

  // ── POST /api/contacto ────────────────────────────────────────────────────
  if (path === '/api/contacto' && request.method === 'POST') {
    const { nombre, email, asunto, mensaje } = await request.json().catch(() => ({}));
    if (!nombre || !email || !mensaje) return error('Campos requeridos');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return error('Email inválido');

    // Guardar en D1
    await env.DB.prepare(
      'INSERT INTO contactos (nombre, email, asunto, mensaje) VALUES (?, ?, ?, ?)'
    ).bind(nombre.trim(), email.trim(), asunto?.trim() || 'Sin asunto', mensaje.trim()).run();

    // Enviar email interno via Resend
    const toEmail = env.TO_EMAIL || 'ventas@wachicargo.site';
    const emailText = [
      'NUEVO MENSAJE DE CONTACTO - WACHICARGO',
      '=======================================',
      `Nombre:  ${nombre}`,
      `Email:   ${email}`,
      `Asunto:  ${asunto || 'Sin asunto'}`,
      '',
      'Mensaje:',
      mensaje,
    ].join('\n');

    const emailHtml = `
      <h2 style="color:#38bdf8;font-family:sans-serif">Nuevo mensaje de contacto</h2>
      <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse;width:100%">
        <tr><td style="padding:6px 12px;color:#666"><b>Nombre</b></td><td style="padding:6px 12px">${nombre}</td></tr>
        <tr style="background:#f9f9f9"><td style="padding:6px 12px;color:#666"><b>Email</b></td><td style="padding:6px 12px"><a href="mailto:${email}">${email}</a></td></tr>
        <tr><td style="padding:6px 12px;color:#666"><b>Asunto</b></td><td style="padding:6px 12px">${asunto || 'Sin asunto'}</td></tr>
        <tr style="background:#f9f9f9"><td style="padding:6px 12px;color:#666;vertical-align:top"><b>Mensaje</b></td><td style="padding:6px 12px;white-space:pre-wrap">${mensaje}</td></tr>
      </table>
      <p style="font-size:12px;color:#999;font-family:sans-serif;margin-top:24px">WACHICARGO · ventas@wachicargo.site</p>
    `;

    await sendEmail(env, 'ventas+cotizaciones_wachicargo@wachicargo.site', `[CONTACTO] ${asunto || nombre}`, emailText, emailHtml);

    return json({ ok: true, mensaje: 'Mensaje enviado correctamente' });
  }

  // ── POST /api/reclamo ─────────────────────────────────────────────────────
  if (path === '/api/reclamo' && request.method === 'POST') {
    const { nombres, documento, domicilio, telefono, correo, apoderado, bien_tipo, bien_monto, bien_descripcion, tipo, detalle, pedido, honeypot } =
      await request.json().catch(() => ({}));

    // Anti-bot
    if (honeypot) return error('Validación fallida', 400);
    if (!nombres || !documento || !domicilio || !telefono || !correo || !bien_tipo || !bien_descripcion || !detalle || !pedido) {
      return error('Faltan campos obligatorios');
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) return error('Correo electrónico inválido');

    const anio = new Date().getFullYear();
    const countRes = await env.DB.prepare('SELECT COUNT(*) as c FROM reclamaciones WHERE fecha LIKE ?').bind(`${anio}-%`).first();
    const num = countRes ? countRes.c + 1 : 1;
    const codigo_reclamo = `${anio}-${String(num).padStart(6, '0')}`;
    const fecha = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    // Guardar en D1
    await env.DB.prepare(
      `INSERT INTO reclamaciones (codigo_reclamo, nombres, documento, telefono, correo, tipo, detalle, domicilio, apoderado, bien_tipo, bien_monto, bien_descripcion, pedido)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      codigo_reclamo, nombres.trim(), documento.trim(), telefono.trim(), correo.trim(), tipo || 'Reclamo', detalle.trim(),
      domicilio.trim(), (apoderado || '').trim(), bien_tipo.trim(), (bien_monto || '').trim(), bien_descripcion.trim(), pedido.trim()
    ).run();

    // Generar PDF
    const dataObj = { codigo_reclamo, fecha, nombres, documento, domicilio, telefono, correo, apoderado, bien_tipo, bien_monto, bien_descripcion, tipo: tipo || 'Reclamo', detalle, pedido };
    let pdfBytes = null;
    let pdfFileName = `${codigo_reclamo}.pdf`;
    try {
      pdfBytes = await generateReclamoPDF(dataObj);
      // Subir a R2
      if (env.R2_RECLAMOS) {
        await env.R2_RECLAMOS.put(pdfFileName, pdfBytes, { httpMetadata: { contentType: 'application/pdf' } });
      }
    } catch(err) {
      console.error('Error generando PDF:', err);
    }

    // Email a la empresa
    const msgEmpresa = `
NUEVO ${(tipo || 'RECLAMO').toUpperCase()} - LIBRO DE RECLAMACIONES
====================================================================
N°:    ${codigo_reclamo}
FECHA: ${fecha}

--- 1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE ---
Nombres:   ${nombres}
DNI/CE:    ${documento}
Domicilio: ${domicilio}
Teléfono:  ${telefono}
Correo:    ${correo}
Padre/Madre/Apoderado: ${apoderado || 'N/A'}

--- 2. IDENTIFICACIÓN DEL BIEN CONTRATADO ---
Tipo:        ${bien_tipo}
Monto (S/):  ${bien_monto || '0.00'}
Descripción: ${bien_descripcion}

--- 3. DETALLE DE LA RECLAMACIÓN Y PEDIDO DEL CONSUMIDOR ---
Tipo:    ${tipo}
Detalle:
${detalle}

Pedido:
${pedido}

Atender en máximo 15 días hábiles conforme a Ley N° 29571.
    `.trim();

    let attachments = null;
    if (pdfBytes) {
      let binary = '';
      for (let i = 0; i < pdfBytes.length; i++) binary += String.fromCharCode(pdfBytes[i]);
      const base64Pdf = btoa(binary);
      attachments = [{ filename: pdfFileName, content: base64Pdf }];
    }

    const toEmail = 'ventas+reclamos_wachicargo@wachicargo.site';
    await sendEmail(env, toEmail, `[${(tipo || 'RECLAMO').toUpperCase()}] ${codigo_reclamo}`, msgEmpresa,
      `<div style="font-family:sans-serif;max-width:800px;margin:0 auto;border:1px solid #ccc;padding:20px;">
        <h2 style="color:#e53e3e;text-align:center;border-bottom:2px solid #e53e3e;padding-bottom:10px;margin-bottom:10px;">HOJA DE RECLAMACIÓN - N° ${codigo_reclamo}</h2>
        <div style="text-align:center;font-size:12px;color:#555;margin-bottom:20px;">
            <b>Razón Social:</b> SERVICIOS Y REPRESENTACIONES WACHI E.I.R.L. | <b>RUC:</b> 20604814180<br>
            <b>Domicilio Fiscal:</b> MZA. K LOTE. 11 URB. AMADEO REPETTO (A 1CDR DE PARQUE JORGE NAVARRTE O TEMPLO) CUSCO - CUSCO - SANTIAGO
        </div>
        <p style="text-align:right"><b>Fecha:</b> ${fecha}</p>

        <h3 style="background:#f0f0f0;padding:5px">1. IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Nombres:</td><td style="padding:5px">${nombres}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">DNI / CE:</td><td style="padding:5px">${documento}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Domicilio:</td><td style="padding:5px">${domicilio}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Teléfono:</td><td style="padding:5px">${telefono}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Correo:</td><td style="padding:5px">${correo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Padre/Madre:</td><td style="padding:5px">${apoderado || 'N/A'}</td></tr>
        </table>

        <h3 style="background:#f0f0f0;padding:5px">2. IDENTIFICACIÓN DEL BIEN CONTRATADO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Tipo:</td><td style="padding:5px">${bien_tipo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold">Monto Reclamado:</td><td style="padding:5px">S/ ${bien_monto || '0.00'}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Descripción:</td><td style="padding:5px">${bien_descripcion}</td></tr>
        </table>

        <h3 style="background:#f0f0f0;padding:5px">3. DETALLE DE LA RECLAMACIÓN Y PEDIDO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px">
          <tr><td style="padding:5px;width:150px;font-weight:bold">Tipo:</td><td style="padding:5px">${tipo}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Detalle:</td><td style="padding:5px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${detalle}</td></tr>
          <tr><td style="padding:5px;font-weight:bold;vertical-align:top">Pedido:</td><td style="padding:5px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${pedido}</td></tr>
        </table>
        
        <p style="font-size:12px;color:#e53e3e;text-align:center;margin-top:20px;font-weight:bold;">El plazo de atención es de 15 días hábiles conforme a Ley N° 29571.</p>
       </div>`, attachments, 'ventas+reclamos_wachicargo@wachicargo.site'
    );

    // Email cargo al cliente (obligatorio INDECOPI)
    const msgClienteHtml = `
      <div style="font-family:sans-serif;max-width:800px;margin:0 auto;border:1px solid #ccc;padding:20px;">
        <h2 style="color:#e53e3e;text-align:center;border-bottom:2px solid #e53e3e;padding-bottom:10px;margin-bottom:10px;">CARGO DE RECEPCIÓN: HOJA DE RECLAMACIÓN - N° ${codigo_reclamo}</h2>
        <div style="text-align:center;font-size:12px;color:#555;margin-bottom:20px;">
            <b>Razón Social:</b> SERVICIOS Y REPRESENTACIONES WACHI E.I.R.L. | <b>RUC:</b> 20604814180<br>
            <b>Domicilio Fiscal:</b> MZA. K LOTE. 11 URB. AMADEO REPETTO (A 1CDR DE PARQUE JORGE NAVARRTE O TEMPLO) CUSCO - CUSCO - SANTIAGO
        </div>
        <p>Estimado(a) <b>${nombres}</b>,</p>
        <p>Hemos recibido su <b>${tipo}</b> a través del Libro de Reclamaciones Virtual de WACHICARGO.</p>
        <p style="text-align:right"><b>Fecha de Ingreso:</b> ${fecha}</p>

        <h3 style="background:#f0f0f0;padding:5px">COPIA DE SU REGISTRO</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Nombres:</td><td style="padding:4px">${nombres}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">DNI / CE:</td><td style="padding:4px">${documento}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Domicilio:</td><td style="padding:4px">${domicilio}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Teléfono:</td><td style="padding:4px">${telefono}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Correo:</td><td style="padding:4px">${correo}</td></tr>
        </table>

        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Bien Contratado:</td><td style="padding:4px">${bien_tipo}</td></tr>
          <tr><td style="padding:4px;font-weight:bold">Monto:</td><td style="padding:4px">S/ ${bien_monto || '0.00'}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Descripción Bien:</td><td style="padding:4px">${bien_descripcion}</td></tr>
        </table>

        <table style="width:100%;border-collapse:collapse;margin-bottom:15px;font-size:13px">
          <tr><td style="padding:4px;width:150px;font-weight:bold">Tipo:</td><td style="padding:4px">${tipo}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Detalle:</td><td style="padding:4px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${detalle}</td></tr>
          <tr><td style="padding:4px;font-weight:bold;vertical-align:top">Pedido:</td><td style="padding:4px;white-space:pre-wrap;background:#f9f9f9;border:1px solid #eee">${pedido}</td></tr>
        </table>

        <div style="background:#fff3cd;border:1px solid #ffeeba;padding:15px;margin-top:20px;border-radius:5px">
            <h4 style="margin-top:0;color:#856404;">Aviso Legal (Ley N° 29571)</h4>
            <p style="margin-bottom:0;color:#856404;font-size:13px;">La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.<br><br><b>WACHICARGO</b> cuenta con un plazo máximo de <b>quince (15) días hábiles</b> improrrogables para atender su solicitud y emitir una respuesta formal a su correo electrónico.</p>
        </div>
        <p style="text-align:center;font-size:12px;color:#999;margin-top:20px">Atentamente,<br><b>WACHICARGO E.I.R.L.</b></p>
      </div>
    `;
    // Convert PDF bytes to Base64 for Resend
    let attachments2 = null;
    if (pdfBytes) {
      let binary = '';
      for (let i = 0; i < pdfBytes.length; i++) binary += String.fromCharCode(pdfBytes[i]);
      const base64Pdf = btoa(binary);
      attachments2 = [{ filename: pdfFileName, content: base64Pdf }];
    }

    // Send email to client
    await sendEmail(env, correo, `Cargo de Recepción - Hoja de Reclamación N° ${codigo_reclamo}`, 'Su cliente de correo no soporta HTML. Por favor, revise el adjunto.', msgClienteHtml, attachments2);

    return json({ ok: true, codigo_reclamo, mensaje: 'Reclamo registrado correctamente' });
  }

  // ── PANEL ADMIN / RECLAMACIONES ───────────────────────────────────────────
  if (path.startsWith('/api/admin/')) {
    // 1. JWT Auth Middleware (Only for Admins)
    const admin = await getAuthUser(request, env);
    const dbAdmin = admin ? await env.DB.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(admin.sub).first() : null;
    const isAdmin = (dbAdmin && dbAdmin.rol === 'admin') || (admin && admin.usr === 'admin');
    if (!isAdmin) {
      return error('No autorizado (requiere rol admin)', 401);
    }

    const urlObj = new URL(request.url);
    const tipo = urlObj.searchParams.get('tipo');
    const buscar = urlObj.searchParams.get('buscar');
    const desde = urlObj.searchParams.get('desde');
    const hasta = urlObj.searchParams.get('hasta');

    let baseQuery = 'SELECT * FROM reclamaciones WHERE 1=1';
    let params = [];

    if (tipo && tipo !== 'Todos') {
      baseQuery += ' AND tipo = ?';
      params.push(tipo);
    }
    if (buscar) {
      baseQuery += ' AND (codigo_reclamo LIKE ? OR nombres LIKE ? OR documento LIKE ?)';
      params.push(`%${buscar}%`, `%${buscar}%`, `%${buscar}%`);
    }
    if (desde) {
      baseQuery += ' AND date(fecha) >= date(?)';
      params.push(desde);
    }
    if (hasta) {
      baseQuery += ' AND date(fecha) <= date(?)';
      params.push(hasta);
    }
    baseQuery += ' ORDER BY fecha DESC';

    const getResults = async () => {
      const stmt = env.DB.prepare(baseQuery);
      return await (params.length > 0 ? stmt.bind(...params) : stmt).all();
    };

    // ── GET /api/admin/reclamos (JSON) ──
    if (path === '/api/admin/reclamos' && request.method === 'GET') {
      const { results } = await getResults();
      return json(results);
    }

    // ── GET /api/admin/exportar (CSV) ──
    if (path === '/api/admin/exportar' && request.method === 'GET') {
      const { results } = await getResults();
      
      let csvContent = '\uFEFF'; // UTF-8 BOM
      csvContent += 'ID,Código,Fecha,Nombres,DNI/CE,Domicilio,Teléfono,Correo,Apoderado,Tipo Bien,Monto Bien,Desc. Bien,Tipo Reclamo/Queja,Detalle,Pedido,Estado\n';
      
      for (const r of results) {
        const row = [
          r.id, r.codigo_reclamo, r.fecha, r.nombres, r.documento, r.domicilio || '', r.telefono, r.correo, 
          r.apoderado || '', r.bien_tipo || '', r.bien_monto || '', r.bien_descripcion || '', r.tipo, r.detalle, r.pedido || '', r.estado
        ].map(col => {
          let str = String(col || '');
          if (str.includes(',') || str.includes('\n') || str.includes('"')) {
            str = `"${str.replace(/"/g, '""')}"`;
          }
          return str;
        }).join(',');
        csvContent += row + '\n';
      }

      return new Response(csvContent, {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="reporte-reclamaciones.csv"',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // ── GET /api/admin/reclamos/:codigo/pdf ──
    const pdfMatch = path.match(/^\/api\/admin\/reclamos\/(.+)\/pdf$/);
    if (pdfMatch && request.method === 'GET') {
      const codigo = pdfMatch[1];
      if (!env.R2_RECLAMOS) return error('R2 no configurado', 500);
      
      const object = await env.R2_RECLAMOS.get(`${codigo}.pdf`);
      if (!object) return error('PDF no encontrado', 404);

      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set('etag', object.httpEtag);
      headers.set('Access-Control-Allow-Origin', '*');
      headers.set('Content-Disposition', `attachment; filename="${codigo}.pdf"`);

      return new Response(object.body, { headers });
    }

    // ── PUT /api/admin/reclamos/:id/atender ──
    const atenderMatch = path.match(/^\/api\/admin\/reclamos\/(\d+)\/atender$/);
    if (atenderMatch && request.method === 'PUT') {
      const id = parseInt(atenderMatch[1]);
      const { detalle_respuesta } = await request.json().catch(() => ({}));

      if (!detalle_respuesta || !detalle_respuesta.trim()) {
        return error('El detalle de la respuesta es obligatorio');
      }

      // Obtener el reclamo actual
      const reclamo = await env.DB.prepare(
        'SELECT * FROM reclamaciones WHERE id = ?'
      ).bind(id).first();

      if (!reclamo) return error('Reclamo no encontrado', 404);
      if (reclamo.estado === 'Atendido') return error('Este reclamo ya fue atendido', 409);

      // Actualizar D1
      await env.DB.prepare(
        `UPDATE reclamaciones 
         SET estado = 'Atendido', 
             detalle_respuesta = ?, 
             fecha_respuesta = datetime('now')
         WHERE id = ?`
      ).bind(detalle_respuesta.trim(), id).run();

      // 1. Email de respuesta al cliente (sin BCC)
      const fechaRespuesta = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

      const htmlRespuesta = `
        <div style="font-family:sans-serif;max-width:700px;margin:0 auto;border:1px solid #ccc;padding:24px;border-radius:8px">
          <div style="text-align:center;border-bottom:2px solid #38bdf8;padding-bottom:16px;margin-bottom:20px">
            <h2 style="color:#38bdf8;margin:0">WACHICARGO</h2>
            <p style="color:#555;font-size:13px;margin:4px 0">SERVICIOS Y REPRESENTACIONES WACHI E.I.R.L. | RUC: 20604814180</p>
            <h3 style="color:#1e293b;margin:8px 0">RESPUESTA OFICIAL A SU ${reclamo.tipo.toUpperCase()}</h3>
            <p style="font-size:13px;color:#555">N° ${reclamo.codigo_reclamo} | Respondido el: ${fechaRespuesta}</p>
          </div>

          <p style="font-size:15px">Estimado(a) <strong>${reclamo.nombres}</strong>,</p>
          <p style="font-size:14px;color:#444">Hemos analizado su ${reclamo.tipo.toLowerCase()} registrado en nuestro Libro de Reclamaciones Virtual y procedemos a darle respuesta formal conforme a la Ley N° 29571.</p>

          <div style="background:#f0f9ff;border-left:4px solid #38bdf8;padding:16px;margin:20px 0;border-radius:0 8px 8px 0">
            <h4 style="margin:0 0 8px;color:#0369a1">RESPUESTA DE WACHICARGO:</h4>
            <p style="margin:0;white-space:pre-wrap;font-size:14px;color:#1e293b">${detalle_respuesta.trim()}</p>
          </div>

          <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:16px">
            <tr style="background:#f8fafc">
              <td style="padding:8px 12px;font-weight:bold;width:40%">Su Reclamo N°:</td>
              <td style="padding:8px 12px">${reclamo.codigo_reclamo}</td>
            </tr>
            <tr>
              <td style="padding:8px 12px;font-weight:bold">Tipo:</td>
              <td style="padding:8px 12px">${reclamo.tipo}</td>
            </tr>
            <tr style="background:#f8fafc">
              <td style="padding:8px 12px;font-weight:bold">Fecha de Ingreso:</td>
              <td style="padding:8px 12px">${reclamo.fecha}</td>
            </tr>
            <tr>
              <td style="padding:8px 12px;font-weight:bold">Fecha de Respuesta:</td>
              <td style="padding:8px 12px">${fechaRespuesta}</td>
            </tr>
          </table>

          <div style="background:#fefce8;border:1px solid #fde68a;padding:14px;margin-top:20px;border-radius:6px;font-size:12px;color:#78350f">
            <strong>Aviso Legal:</strong> Si no queda satisfecho con esta respuesta, puede acudir al INDECOPI u otras vías de solución de controversias. La formulación del reclamo no es requisito previo para interponer una denuncia ante el INDECOPI.
          </div>

          <p style="text-align:center;font-size:12px;color:#999;margin-top:24px">Atentamente,<br><strong>WACHICARGO E.I.R.L.</strong><br>ventas@wachicargo.site | +51 925 247 920</p>
        </div>
      `;

      await sendEmail(
        env,
        reclamo.correo,
        `Respuesta a su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} - WACHICARGO`,
        `Estimado(a) ${reclamo.nombres}, le comunicamos que su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} ha sido atendido. Respuesta: ${detalle_respuesta.trim()}`,
        htmlRespuesta
      );

      // 2. Email copia a la empresa enviado directamente al alias con etiqueta para que el filtro de Zoho lo mueva
      await sendEmail(
        env,
        'ventas+reclamos_wachicargo@wachicargo.site',
        `[COPIA ATENCIÓN] Respuesta a su ${reclamo.tipo} N° ${reclamo.codigo_reclamo} - WACHICARGO`,
        `Copia de respuesta oficial enviada al cliente ${reclamo.nombres} (${reclamo.correo}). Respuesta: ${detalle_respuesta.trim()}`,
        htmlRespuesta
      );

      return json({ ok: true, mensaje: `${reclamo.tipo} marcado como Atendido y correo enviado al cliente.` });
    }

    return error('Admin endpoint not found', 404);
  }

  // ── 404 ───────────────────────────────────────────────────────────────────
  return error('Ruta no encontrada', 404);
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const data = await request.formData().catch(() => null);
    if (!data) return error('Formato inválido');

    const nombres = data.get('nombres') || '';
    const documento = data.get('documento') || '';
    const domicilio = data.get('domicilio') || '';
    const telefono = data.get('telefono') || '';
    const correo = data.get('correo') || '';
    const apoderado = data.get('apoderado') || '';
    
    const bien_tipo = data.get('bien_tipo') || '';
    const bien_monto = data.get('bien_monto') || '';
    const bien_descripcion = data.get('bien_descripcion') || '';
    
    const tipo = data.get('tipo') || 'Reclamo';
    const detalle = data.get('detalle') || '';
    const pedido = data.get('pedido') || '';

    if (!nombres || !documento || !domicilio || !telefono || !correo || !detalle || !pedido) {
      return error('Faltan campos obligatorios');
    }

    // Generar código
    const anio = new Date().getFullYear();
    const codigo_reclamo = `${anio}-${Math.floor(Math.random() * 900000) + 100000}`; // Random 6 digit for simplicity without DB
    const fecha = new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' });

    const dataObj = { codigo_reclamo, fecha, nombres, documento, domicilio, telefono, correo, apoderado, bien_tipo, bien_monto, bien_descripcion, tipo, detalle, pedido };

    // Generar PDF
    let pdfBytes;
    try {
      pdfBytes = await generateReclamoPDF(dataObj);
    } catch (e) {
      console.error('Error generando PDF:', e);
      return error('Error interno al generar el documento', 500);
    }

    // Adjuntos
    const pdfBase64 = btoa(String.fromCharCode(...new Uint8Array(pdfBytes)));
    const attachments = [{
      filename: `${codigo_reclamo}.pdf`,
      content: pdfBase64
    }];

    // Correo Empresa
    const toEmail = 'discover@manujungleforever.com';
    const msgEmpresa = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;">
        <h2 style="color:#2d8a56;text-align:center;border-bottom:2px solid #2d8a56;padding-bottom:10px;margin-bottom:10px;">NUEVO ${tipo.toUpperCase()} - LIBRO DE RECLAMACIONES</h2>
        <p><strong>N°:</strong>    ${codigo_reclamo}</p>
        <p><strong>Fecha:</strong> ${fecha}</p>
        <p><strong>Cliente:</strong> ${nombres} (DNI/CE: ${documento})</p>
        <p><strong>Contacto:</strong> ${correo} | ${telefono}</p>
        <div style="background:#f9f9f9;padding:15px;border-left:4px solid #2d8a56;margin-top:20px;">
          <h3 style="margin-top:0;color:#2d8a56;">Detalle de la ${tipo}:</h3>
          <p style="white-space:pre-wrap;">${detalle}</p>
          <h3 style="margin-top:15px;color:#2d8a56;">Pedido del Cliente:</h3>
          <p style="white-space:pre-wrap;">${pedido}</p>
        </div>
        <p style="text-align:center;margin-top:20px;font-size:12px;color:#777;">El documento PDF oficial con la firma legal se encuentra adjunto a este correo.</p>
      </div>`;

    // Correo Cliente
    const msgClienteHtml = `
      <div style="font-family:Arial,sans-serif;color:#333;line-height:1.6;max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:8px;">
        <h2 style="color:#2d8a56;text-align:center;border-bottom:2px solid #2d8a56;padding-bottom:10px;margin-bottom:10px;">CARGO DE RECEPCIÓN: HOJA DE RECLAMACIÓN - N° ${codigo_reclamo}</h2>
        <p>Estimado(a) <strong>${nombres}</strong>,</p>
        <p>Le informamos que hemos recibido satisfactoriamente su <strong>${tipo.toLowerCase()}</strong> a través de nuestro Libro de Reclamaciones Virtual.</p>
        <div style="background:#f9f9f9;padding:15px;border:1px solid #eee;margin:20px 0;text-align:center;">
          <p style="margin:0;font-size:14px;color:#555;">Fecha de registro:</p>
          <h3 style="margin:5px 0 0 0;color:#2d8a56;">${fecha}</h3>
        </div>
        <p>Adjuntamos a este correo el documento PDF oficial que sirve como <strong>Cargo de Recepción</strong> de su reclamo/queja. Este documento contiene todos los detalles que usted proporcionó.</p>
        <div style="background:#fff3cd;border-left:4px solid #ffeeba;padding:15px;margin-top:20px;">
            <p style="margin-bottom:0;color:#856404;font-size:13px;">La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.<br><br><b>MANU JUNGLE FOREVER</b> cuenta con un plazo máximo de <b>quince (15) días hábiles</b> improrrogables para atender su solicitud y emitir una respuesta formal a su correo electrónico.</p>
        </div>
        <p style="margin-top:20px;text-align:center;font-size:12px;color:#777;">Atentamente,<br><strong>Manu Jungle Forever</strong></p>
      </div>`;

    if (env.RESEND_API_KEY) {
      await sendEmail(env, toEmail, `[${tipo.toUpperCase()}] ${codigo_reclamo}`, msgEmpresa, msgEmpresa, attachments, toEmail);
      await sendEmail(env, correo, `Cargo de Recepción - Hoja de Reclamación N° ${codigo_reclamo}`, 'Adjunto su cargo.', msgClienteHtml, attachments, toEmail);
    } else {
      console.warn("RESEND_API_KEY no configurada. Saltando envío de correos.");
    }

    // Guardar en GitHub
    if (env.GITHUB_TOKEN) {
      try {
        const repo = 'manujungleforever-debug/manujungleforever';
        const branch = 'main';
        const filePath = 'www.manujungleforever.com/data/reclamos.json';
        const url = `https://api.github.com/repos/${repo}/contents/${filePath}?ref=${branch}`;
        const headers = {
          'User-Agent': 'Cloudflare-Worker',
          'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        };
        
        let fileSha = null;
        let reclamos = [];
        
        const getRes = await fetch(url, { headers });
        if (getRes.ok) {
          const dataGet = await getRes.json();
          fileSha = dataGet.sha;
          reclamos = JSON.parse(atob(dataGet.content));
        }
        
        // Append new
        reclamos.unshift({ ...dataObj, id: Date.now(), estado: 'Pendiente' });
        
        const contentB64 = btoa(unescape(encodeURIComponent(JSON.stringify(reclamos, null, 2))));
        const body = {
          message: `Nuevo reclamo: ${codigo_reclamo}`,
          content: contentB64,
          branch: branch
        };
        if (fileSha) body.sha = fileSha;
        
        await fetch(`https://api.github.com/repos/${repo}/contents/${filePath}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(body)
        });
        
      } catch(err) {
        console.error("Error guardando en GitHub:", err);
      }
    }

    return json({ ok: true, success: true, codigo_reclamo, message: 'Reclamo registrado correctamente' });
  } catch (e) {
    console.error('Error general reclamo:', e);
    return error('Error procesando la solicitud', 500);
  }
}
