import socket
import time
import mysql.connector
from Logs_SQL import log_info, log_error, log_warning, log_debug, log_critical

#* CONFIGURACIONES SERVIDOR Y MYSQL
HOST = "localhost"
PORT = 8080
tiempo_espera = 5  # Tiempo de espera en segundos

#! PARAMETROS DE CONEXION A LA BASE DE DATOS
user = 'test_pithon'
password = '321_atomica'
database = 'db_python'

# =================================================

# TODO: METODOS DE CONSULTA A LA BASE DE DATOS
def table_personajes(conn: socket.socket):
    log_info("Seleccionada la tabla: Personajes")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    conn.send("\n¿Qué quieres hacer? 1. Insertar 2. Buscar 3. Borrar Personaje 4. Salir".encode())
    db_connection = mysql.connector.connect(
        host=HOST,
        user=user,
        password=password,
        database=database
    )
    cursor = db_connection.cursor()
    while True:
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        
        if msg == "1":
            conn.send("Ingrese el NOMBRE del personaje a AÑADIR: ".encode())
            nombre = conn.recv(1024).decode().capitalize()
            conn.send("Ingrese el ID del JUEGO al que pertenece: ".encode())
            juego_id = conn.recv(1024).decode()
            sql = "INSERT INTO personajes (nombre, juego_id) VALUES (%s, %s)"
            val = (nombre, juego_id)
            cursor.execute(sql, val)
            db_connection.commit()
            conn.send(f"Personaje {nombre} insertado correctamente.\nPARA CONTINUAR 'ENTER' ".encode())
            log_info(f"Personaje {nombre} insertado correctamente.")
            table_personajes(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
        elif msg == "2":
            conn.send("Ingrese el NOMBRE del personaje a BUSCAR: ".encode())
            nombre = conn.recv(1024).decode().capitalize()
            sql = f"SELECT p.nombre, j.nombre FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.nombre = '{nombre}'"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if resultado:
                conn.send(f"Personaje encontrado: {resultado}\nPARA CONTINUAR 'ENTER' ".encode())
                log_info(f"Personaje encontrado: {resultado}")
            else:
                conn.send("Personaje no encontrado.\nPARA CONTINUAR 'ENTER' ".encode())
                log_warning("Personaje no encontrado.")
                table_personajes(conn)
            log_info(f"Personaje buscado: {nombre}")
            table_personajes(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

        elif msg == "4":
            conn.send("Saliendo del servidor...".encode())
            log_info("Saliendo del servidor...")
            cursor.close()
            db_connection.close()
            log_info("Conexión a la base de datos cerrada.")
            break

#TODO: SERVIDOR SOCKETS

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        log_info(f"Servidor escuchando en {HOST}:{PORT}")
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print (f"Conexión establecida desde {addr}")
                log_info(f"Conexión establecida desde {addr}")

                conn.send("Elige una opción:\n1. Personajes 2. Juegos 3. Empresa \n4. Salir\nEscribe un número: ".encode())

                time.sleep(tiempo_espera)
                msg = conn.recv(1024).decode()
                print(f"Mensaje recibido: {msg}")
                log_info(f"Mensaje recibido: {msg}")

                if msg == "1":
                    print("Opción 1 seleccionada: Personajes")
                    log_info("Opción 1 seleccionada: Personajes")
                    table_personajes(conn)
                elif msg == "2":
                    print("Opción 2 seleccionada: Juegos")
                    log_info("Opción 2 seleccionada: Juegos")
                    # table_juegos(conn)
                elif msg == "3":
                    print("Opción 3 seleccionada: Empresa")
                    log_info("Opción 3 seleccionada: Empresa")
                    # table_empresa(conn)
                elif msg == "4":
                    print("Saliendo del servidor...")
                    log_info("Saliendo del servidor...")
                    conn.send("Saliendo del servidor...".encode())
                    break


if __name__ == "__main__":
    start_server()
    log_info("Servidor iniciado")
    print("Servidor iniciado")

