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



insert INTO personajes (nombre, elemento, juego_id) values
('Bennett', 'Pyro',1),
('Kazuha','Anemo', 1),
('Arlecchino', 'Pyro' ,1),
('Xiao', 'Anemo', 1),
('Jing Yan', 'Rayo', 2),
('Kafka', 'Rayo', 2),
('Gepard', 'Hielo', 2),
('Topaz y Conti', 'Fuego', 2),
('Jiyan', 'Aero', 3),
('Calcharo', 'Electro', 3),
('Lingyang', 'Glacio', 3),
('Encore', 'Fusion', 3),
('Arion', 'Aire', 4),
('Mark', 'Montaña', 4),
('Umei', 'Bosque', 4),
('Sonny', 'Fuego', 4),
('Lycaon', 'Hielo', 5),
('Lighter', 'Fuego', 5);