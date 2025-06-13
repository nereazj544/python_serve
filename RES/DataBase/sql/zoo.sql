CREATE TABLE animales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    especie VARCHAR(255) NOT NULL
);

CREATE TABLE recintos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255),
    capacidad INT
);

CREATE TABLE numero_recinto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT,
    recinto_id INT,
    FOREIGN KEY (recinto_id) REFERENCES recintos(id)
);

CREATE TABLE cuidador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    numero_recinto_id INT,
    FOREIGN KEY (numero_recinto_id) REFERENCES numero_recinto(id)
);

-- Inserciones
INSERT INTO animales (nombre, especie) VALUES
('Tigre', 'Felino'),
('León', 'Felino'),
('Pantera', 'Felino'),
('Cocodrilo', 'Reptil');

INSERT INTO recintos (nombre, ubicacion, capacidad) VALUES
('Recinto de Felinos', 'Zona Norte', 5),
('Recinto de Reptiles', 'Zona Sur', 3);

INSERT INTO numero_recinto (numero, recinto_id) VALUES
(1, 1),
(2, 2);

INSERT INTO cuidador (nombre, numero_recinto_id) VALUES
('Rita', 1),
('Rick', 2);
