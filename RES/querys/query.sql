select j.nombre, p.nombre,  p.genero from personajes p inner join juegos j on j.id = p.juego_id 
where p.genero = 'masculino' and j.empresa_id like 1 order by p.nombre ASC ;