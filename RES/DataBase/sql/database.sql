-- ZONAS
CREATE TABLE zona (
   id int auto_increment PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- UBICACIONES
CREATE TABLE ubicacion (
   id int auto_increment PRIMARY KEY,
    nombre TEXT NOT NULL,
    zona_id INTEGER NOT NULL,
    FOREIGN KEY (zona_id) REFERENCES zona(id)
);

-- TERMINALES
CREATE TABLE terminal (
   id int auto_increment PRIMARY KEY,
    estado TEXT NOT NULL,
    ubicacion_id INTEGER NOT NULL,
    FOREIGN KEY (ubicacion_id) REFERENCES ubicacion(id)
);

-- TECNICOS
CREATE TABLE tecnico (
   id int auto_increment PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
);

-- TELEOPERADORES
CREATE TABLE teleoperador (
   id int auto_increment PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL,
    ubicacion_id INTEGER NOT NULL,
    FOREIGN KEY (ubicacion_id) REFERENCES ubicacion(id)
);

-- HISTORIAL DE ESTADOS DE TERMINALES
CREATE TABLE terminal_estado_historial (
   id int auto_increment PRIMARY KEY,
    terminal_id INTEGER NOT NULL,
    estado_anterior TEXT,
    estado_nuevo TEXT NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (terminal_id) REFERENCES terminal(id)
);

-- INCIDENCIAS EN TERMINALES
CREATE TABLE incidencia (
    id int auto_increment PRIMARY KEY,
    terminal_id INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_reportada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    solucionada BOOLEAN DEFAULT FALSE,
    fecha_solucion TIMESTAMP,
    tecnico_id INTEGER,
    FOREIGN KEY (terminal_id) REFERENCES terminal(id),
    FOREIGN KEY (tecnico_id) REFERENCES tecnico(id)
);

-- RELACIÓN TECNICO-ZONA (opcional, si quieres soporte multi-zona)
CREATE TABLE tecnico_zona (
    tecnico_id INTEGER NOT NULL,
    zona_id INTEGER NOT NULL,
    PRIMARY KEY (tecnico_id, zona_id),
    FOREIGN KEY (tecnico_id) REFERENCES tecnico(id),
    FOREIGN KEY (zona_id) REFERENCES zona(id)
);

-- BITÁCORA DE MOVIMIENTOS DE TERMINAL
CREATE TABLE terminal_movimiento (
   id int auto_increment PRIMARY KEY,
    terminal_id INTEGER NOT NULL,
    ubicacion_origen INTEGER,
    ubicacion_destino INTEGER NOT NULL,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (terminal_id) REFERENCES terminal(id),
    FOREIGN KEY (ubicacion_origen) REFERENCES ubicacion(id),
    FOREIGN KEY (ubicacion_destino) REFERENCES ubicacion(id)
);
