-- TABLAS

create table empresas(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) not null,
    pais VARCHAR(255) not null
)

create table juegos(
    id int auto_increment primary key,
    nombre varchar(255) not null,
    genero varchar (255) NOT NULL,
    clasificacion_edad varchar(255) NOT NULL,
    empresa_id int,
    foreign key (empresa_id) references empresas(id)
);

create table personajes(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT Null,
    elemento VARCHAR(255) NOT Null,
    genero VARCHAR(255) NOT NULL,
    rareza VARCHAR(10),
    arma VARCHAR(255),
    faccion VARCHAR(255) NOT NULL,
    juego_id int,
    foreign key (juego_id) references juegos(id)
);

create table habilidades(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    personaje_id int,
    foreign key (personaje_id) references personajes(id)
);

create table plataformas(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

create table juego_plataformas(
    id int auto_increment PRIMARY KEY,
    juego_id int,
    plataforma_id int,
    foreign key (juego_id) references juegos(id),
    foreign key (plataforma_id) references plataformas(id)
);



-- INSERTAR DATOS INICIALES
insert INTO empresas (nombre, pais) values 
('Hoyoverse', 'China'), 
('Kuro Game', 'China'), 
('Level-5', 'Japón');

insert INTO plataformas (nombre) values 
('PC'), 
('PlayStation'), 
('Xbox'), 
('Nintendo Switch'), 
('Móviles');

insert into juegos (nombre, genero, clasificacion_edad, empresa_id) values
('Genshin Impact (GI)', 'Gachas', 'T', 1),
('Honkai Star Rail (HSR)', 'Gachas', 'T', 1),
('Zenless Zone Zero (ZZZ)', 'Gachas', 'T', 1),
('Wuthering Waves (WuWa)', 'Gachas', 'T', 2),
('Inazuma Eleven (IE)', 'Deportes', 'E10+', 3);


insert into plataformas (nombre) values
('PC'), -- 1
('PlayStation 4'), -- 2
('PlayStation 5'), -- 3
('Xbox Series X/S'), -- 4
('Nintendo Switch'), -- 5
('Nintendo Switch 2'), -- 6
('iOS'), -- 7
('Android'); -- 8


insert into juego_plataformas (juego_id, plataforma_id) values
(1, 1), -- Genshin Impact en PC
(1, 2), -- Genshin Impact en PlayStation 4
(1, 3), -- Genshin Impact en PlayStation 5
(1, 4), -- Genshin Impact en Xbox Series X/S
(1, 7), -- Genshin Impact en iOS
(1, 8), -- Genshin Impact en Android
(2, 1), -- Honkai Star Rail en PC
(2, 2), -- Honkai Star Rail en PlayStation 4
(2, 3), -- Honkai Star Rail en PlayStation 5
(2, 7), -- Honkai Star Rail en iOS
(2, 8), -- Honkai Star Rail en Android
(3, 1), -- Zenless Zone Zero en PC
(3, 2), -- Zenless Zone Zero en PlayStation 4
(3, 3), -- Zenless Zone Zero en PlayStation 5
(3, 4), -- Zenless Zone Zero en Xbox Series X/S
(3, 7), -- Zenless Zone Zero en iOS
(3, 8), -- Zenless Zone Zero en Android
(4, 1), -- Wuthering Waves en PC
(4, 2), -- Wuthering Waves en PlayStation 4
(4, 3), -- Wuthering Waves en PlayStation 5
(4, 7), -- Wuthering Waves en iOS
(4, 8), -- Wuthering Waves en Android
(5, 1), -- Inazuma Eleven en PC
(5, 2), -- Inazuma Eleven en PlayStation 4
(5, 3), -- Inazuma Eleven en PlayStation 5
(5, 4), -- Inazuma Eleven en Xbox Series X/S
(5, 5), -- Inazuma Eleven en Nintendo Switch
(5, 6); -- Inazuma Eleven en Nintendo Switch 2

