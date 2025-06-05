
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
    juego_id int,
    foreign key (juego_id) references juegos(id)
);


insert INTO empresa (nombre) values ('Hoyoverse'), ('Kuro Game'), ('Level-5');

insert INTO juegos (nombre, genero, empresa_id) values
('Genshin Impact', 'Gachas', 1),
('Honkai Star Rail', 'Gachas', 1),
('Wuthering Waves', 'Gachas', 2),
('Inazuma Eleven', 'Deportes', 3);


insert INTO personajes (nombre, juego_id) values
('Bennett', 1),
('Kazuha', 1),
('Arlecchino',  1),
('Xiao',  1),
('Jing Yan',  2),
('Kafka',  2),
('Gepard', 2),
('Topaz y Conti', 2),
('Jiyan', 3),
('Calcharo', 3),
('Lingyang', 3),
('Encore', 3),
('Arion', 4),
('Mark', 4),
('Umei', 4),
('Sonny', 4);