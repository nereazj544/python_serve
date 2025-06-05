create table empresa(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT Null
);
create table juegos(
	id int auto_increment primary key,
    nombre varchar(255) not null,
    genero varchar (255) NOT NULL,
    empresa_id int,
    foreign key (empresa_id) references empresa(id)
);
create table personajes(
    id int auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT Null,
    elemento VARCHAR(255) NOT Null,
    rareza VARCHAR(10),
    juego_id int,
    foreign key (juego_id) references juegos(id)
);


insert INTO empresa (nombre) values ('Hoyoverse'), ('Kuro Game'), ('Level-5');

insert INTO juegos (nombre, genero, empresa_id) values
('Genshin Impact (GI)', 'Gachas', 1),
('Honkai Star Rail (HSR)', 'Gachas', 1),
('Wuthering Waves (WuWa)', 'Gachas', 2),
('Inazuma Eleven (IE)', 'Deportes', 3),
('Zenless Zone Zero (ZZZ)', 'Gachas', 1);



INSERT INTO personajes (nombre, elemento, rareza, juego_id) VALUES
('Bennett', 'Pyro', '4', 1),
('Kazuha', 'Anemo', '5', 1),
('Arlecchino', 'Pyro', '5', 1),
('Xiao', 'Anemo', '5', 1),
('Jing Yan', 'Rayo', '5', 2),
('Kafka', 'Rayo', '5', 2),
('Gepard', 'Hielo', '5', 2),
('Topaz y Conti', 'Fuego', '5', 2),
('Jiyan', 'Aero', '5', 3),
('Calcharo', 'Electro', '5', 3),
('Lingyang', 'Glacio', '5', 3),
('Encore', 'Fusion', '5', 3),
('Arion', 'Aire', NULL, 4),
('Mark', 'Montaña', NULL, 4),
('Umei', 'Bosque', NULL, 4),
('Sonny', 'Fuego', NULL, 4),
('Lycaon', 'Hielo', '5', 5),
('Lighter', 'Fuego', '5', 5);
