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

-- ZONAS
INSERT INTO zona (nombre) VALUES
  ('Teyvat'),
  ('Hyrule'),
  ('Kanto'),
  ('Raccoon City');

-- UBICACIONES
INSERT INTO ubicacion (nombre, zona_id) VALUES
  ('Mondstadt', 1),   -- Teyvat
  ('Liyue', 1),       -- Teyvat
  ('Castillo Hyrule', 2), -- Hyrule
  ('Bosque Kokiri', 2),   -- Hyrule
  ('Ciudad Plateada', 3), -- Kanto
  ('Pueblo Paleta', 3),   -- Kanto
  ('Comisaría de Policía', 4), -- Raccoon City
  ('Hospital', 4);         -- Raccoon City

-- TECNICOS
INSERT INTO tecnico (nombre, apellido, telefono, email) VALUES
  ('Bennett', 'Adventurer', '123456789', 'bennett@teyvat.com'),
  ('Link', 'Hero', '555000111', 'link@hyrule.com'),
  ('Misty', 'Waterflower', '987654321', 'misty@kanto.com'),
  ('Jill', 'Valentine', '666222111', 'jill@racoon.com');

-- TELEOPERADORES
INSERT INTO teleoperador (nombre, apellido, telefono, email, ubicacion_id) VALUES
  ('Aiden', 'Stone', '700900800', 'aiden@teyvat.com', 1), -- Mondstadt
  ('Paimon', 'Navigator', '123123123', 'paimon@teyvat.com', 2), -- Liyue
  ('Zelda', 'Princess', '321321321', 'zelda@hyrule.com', 3), -- Castillo Hyrule
  ('Saria', 'Forest', '456456456', 'saria@hyrule.com', 4), -- Bosque Kokiri
  ('Ash', 'Ketchum', '999111888', 'ash@kanto.com', 5), -- Ciudad Plateada
  ('Nurse', 'Joy', '444555666', 'joy@kanto.com', 6), -- Pueblo Paleta
  ('Leon', 'Kennedy', '333222111', 'leon@racoon.com', 7), -- Comisaría de Policía
  ('Claire', 'Redfield', '777888999', 'claire@racoon.com', 8); -- Hospital

-- TERMINALES
INSERT INTO terminal (estado, ubicacion_id) VALUES
  ('Operativo', 1),
  ('En Reparación', 2),
  ('Operativo', 3),
  ('Averiado', 4),
  ('Operativo', 5),
  ('Averiado', 6),
  ('Operativo', 7),
  ('En Reparación', 8);

-- HISTORIAL DE ESTADOS
INSERT INTO terminal_estado_historial (terminal_id, estado_anterior, estado_nuevo, fecha_cambio) VALUES
  (1, NULL, 'Operativo', '2025-06-01 10:00:00'),
  (2, 'Operativo', 'En Reparación', '2025-06-02 12:30:00'),
  (4, 'Operativo', 'Averiado', '2025-06-05 15:00:00'),
  (6, 'Operativo', 'Averiado', '2025-06-07 11:45:00'),
  (8, 'Averiado', 'En Reparación', '2025-06-08 09:25:00');

-- INCIDENCIAS
INSERT INTO incidencia (terminal_id, descripcion, fecha_reportada, solucionada, fecha_solucion, tecnico_id) VALUES
  (2, 'Pantalla en negro tras actualización.', '2025-06-02 12:35:00', 1, '2025-06-03 10:00:00', 1),    -- Solucionada por Bennett
  (4, 'No responde el teclado.', '2025-06-05 15:10:00', 0, NULL, 2),         -- Asignada a Link, no resuelta
  (6, 'Problema de red intermitente.', '2025-06-07 12:00:00', 1, '2025-06-07 16:00:00', 3),             -- Solucionada por Misty
  (8, 'Bloqueo del sistema.', '2025-06-08 09:30:00', 0, NULL, 4);            -- Diagnóstico de Jill, sin solución aún

-- RELACIÓN TECNICO-ZONA
INSERT INTO tecnico_zona (tecnico_id, zona_id) VALUES
  (1,1),  -- Bennett en Teyvat
  (2,2),  -- Link en Hyrule
  (3,3),  -- Misty en Kanto
  (4,4);  -- Jill en Raccoon City

-- BITÁCORA DE MOVIMIENTOS DE TERMINAL
INSERT INTO terminal_movimiento (terminal_id, ubicacion_origen, ubicacion_destino, fecha_movimiento) VALUES
  (2,1,2,'2025-06-02 08:10:00'),  -- De Mondstadt a Liyue
  (4,3,4,'2025-06-05 14:00:00'),  -- De Castillo Hyrule a Bosque Kokiri
  (6,5,6,'2025-06-07 10:00:00'),  -- De Ciudad Plateada a Pueblo Paleta
  (8,7,8,'2025-06-08 09:00:00');  -- De Comisaría a Hospital
