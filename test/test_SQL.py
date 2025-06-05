
import mysql.connector

# ? CONEXION A LA BASE DE DATOS
conn = mysql.connector.connect(
    host = "localhost",
    user = 'test_pithon',
    password = '321_atomica',
    database = 'db_python'
)

# ? CONFIGURACION DE LA QUERY
query = "SELECT p.nombre, j.nombre FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id ORDER BY p.nombre ASC;"
cursor = conn.cursor()
# ? EJECUCION DE LA QUERY
cursor.execute(query)

# ? OBTENCION DE LOS RESULTADOS
resultados = cursor.fetchall()
# ? IMPRESION DE LOS RESULTADOS
for resultado in resultados:
    print(resultado)


#! INSERTAR
# nombre = input("Ingrese el nombre del personaje: ")
# juego_id = int(input("Ingrese el ID del juego: "))
# insert_query = "INSERT INTO personajes (nombre, juego_id)"
# values = (nombre, juego_id)
# cursor.execute(insert_query, values)
# conn.commit()
# print(f"Personaje {nombre} insertado correctamente.")

# nombre = input("Ingrese el nombre del personaje: ").capitalize()
# juego_id = int(input("Ingrese el ID del juego: "))
# sql = "INSERT INTO personajes (nombre, juego_id) VALUES (%s, %s)"
# val = (nombre, juego_id)
# cursor.execute(sql, val)
# conn.commit()
# print(f"Personaje {nombre} insertado correctamente.")

