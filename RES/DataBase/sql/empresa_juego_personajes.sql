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
    genero VARCHAR(255) NOT NULL,
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



('Bennett', 'Pyro', 'Masculino', '4', 1),
('Kazuha', 'Anemo', 'Masculino', '5', 1),
('Arlecchino', 'Pyro', 'Femenino', '5', 1),
('Xiao', 'Anemo', 'Masculino', '5', 1),
('Jing Yan', 'Rayo', 'Masculino', '5', 2),
('Kafka', 'Rayo', 'Femenino', '5', 2),
('Gepard', 'Hielo', 'Masculino', '5', 2),
('Topaz y Conti', 'Fuego', 'Femenino', '5', 2),
('Jiyan', 'Aero', 'Masculino', '5', 3),
('Calcharo', 'Electro', 'Masculino', '5', 3),
('Lingyang', 'Glacio', 'Masculino', '5', 3),
('Encore', 'Fusion', 'Femenino', '5', 3),
('Arion', 'Aire', 'Masculino', NULL, 4),
('Mark', 'Montaña','Masculino', NULL, 4),
('Umei', 'Bosque', 'Masculino', NULL, 4),
('Sonny', 'Fuego', 'Masculino', NULL, 4),
('Lycaon', 'Hielo', 'Masculino', '5', 5),
('Lighter', 'Fuego', 'Masculino','5' ,5);