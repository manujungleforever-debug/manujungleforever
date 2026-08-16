-- Schema for Libro de Reclamaciones in Manu Jungle Forever
CREATE TABLE IF NOT EXISTS reclamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_reclamo TEXT UNIQUE NOT NULL,
    fecha TEXT NOT NULL,
    nombres TEXT NOT NULL,
    documento TEXT NOT NULL,
    domicilio TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL,
    apoderado TEXT,
    bien_tipo TEXT,
    bien_monto TEXT,
    bien_descripcion TEXT,
    tipo TEXT NOT NULL, -- 'Reclamo' or 'Queja'
    detalle TEXT NOT NULL,
    pedido TEXT NOT NULL,
    estado TEXT DEFAULT 'Pendiente', -- 'Pendiente' or 'Atendido'
    detalle_respuesta TEXT,
    fecha_respuesta TEXT
);
