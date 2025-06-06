
''' 
SERVIDOR V1_Masivo.py

Este servidor lo que hace es que va a realizar son consultas a dos bases de datos diferentes (SQL y MongoDB). 

Donde el cliente sera el encargado de enviar las 'peticiones' y el servidor las procesara.

En esta versión, el servidor sera simple (no asincrono (eso sera en la versión 2)) y se encargara de procesar las peticiones de forma secuencial.

'''


#TODO: Librerias
    # ? SOCKETS
import socket  # Configuración del servidor y cliente
import time  # Para manejar tiempos de espera y pausas

    #! BASES DE DATOS
from pymongo import MongoClient  # Para manejar la base de datos MongoDB
import mysql.connector  # Para manejar la base de datos MySQL

    # ? LOGS 

from logs.Logs_Masivo_V1 import log_info, log_error, log_warning, log_debug, log_critical  
# Para manejar los logs


# * ==========================================================


# TODO: CONFIGURACIONES SERVIDOR Y BASE DE DATOS
    #* SERVIDOR
HOST = "localhost"
PORT = 8080
tiempo_espera = 5  # Tiempo de espera en segundos

# TODO: PARAMETROS DE CONEXION A LA BASE DE DATOS

    #* MONGODB
DB_MONGO = "MaxServer"
COLLECTION_MONGO_1 = "Personajes"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Empresa"

client = MongoClient("mongodb://localhost:27017/")

    #* MYSQL
DB_MYSQL = "db_python"
USER = 'test_pithon'
PASSWORD = '321_atomica'
TABLE_MYSQL_1 = "personajes"
TABLE_MYSQL_2 = "juegos"
TABLE_MYSQL_3 = "empresa"

db_conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DB_MYSQL
)

# =================================================
# TODO: CONSULTAS A MySQL
def collection_MYSQL_1(conn:socket.socket): # Personajes
    conn.send("== SELECCION COLECCION: PERSONAJES (MySQL) ==\n"\
    "¿Que quieres hacer?\n"\
    "1. Insertar Personajes\n" \
    "2. Consultar Personajes\n" \
    "3. Volver a las opciones\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MySQL")

    if msg == "1": #? Insertar - Personajes
        log_info("Seleccionada la opcion: Insertar Personajes")
        
        conn.send("== INSERTAR PERSONAJES (MySQL) ==\n"\
        "Introduce el NOMBRE del personaje: ".encode())
        NOMBRE = conn.recv(1024).decode().capitalize()
        log_info(f"Nombre del personaje recibido: {NOMBRE}")
        
        conn.send("Introduce el ELEMENTO del personaje: ".encode())
        ELEMENTO = conn.recv(1024).decode()
        log_info(f"Elemento del personaje recibido: {ELEMENTO}")
        
        conn.send("Introduce la RAREZA del personaje:".encode())
        RAREZA = conn.recv(1024).decode()
        log_info(f"Rareza del personaje recibido: {RAREZA}")
        
        conn.send("Introduce el GENERO del personaje: ".encode())
        GENERO = conn.recv(1024).decode().capitalize()
        log_info(f"Género del personaje recibido: {GENERO}")

        conn.send("Introduce el ID del juego al que pertenece: ".encode())
        JUEGO_ID = conn.recv(1024).decode()
        log_info(f"ID del juego recibido: {JUEGO_ID}")

        #? INSERTAR DATOS EN MySQL
        cr = db_conn.cursor()
        query = "INSERT INTO personajes (nombre, elemento, genero, rareza, juego_id) VALUES (%s, %s, %s, %s, %s)"
        values = (NOMBRE, ELEMENTO, GENERO, RAREZA,  JUEGO_ID)
        cr.execute(query, values)
        db_conn.commit()
        log_info(f"Datos insertados en MySQL: {values}")
        conn.send("Personaje insertado correctamente.\nPARA CONTINUAR 'ENTER' ".encode())
        collection_MYSQL_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

    elif msg == "2": #? Consultar - Personajes
        log_info("Seleccionada la opcion: Consultar Personajes")
        conn.send("== CONSULTAR PERSONAJES (MySQL) ==\n"\
        "¿Que quieres hacer?\n"\
            "1. Consultar todos los personajes\n" \
            "2. Consultar personaje por NOMBRE\n" \
            "3. Otras consultas\n" \
            "4. Volver a las opciones\n".encode())
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
        log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MySQL")

        if msg == "1": #? Consultar todos los personajes
            log_info("Seleccionada la opcion: Consultar todos los personajes")
            conn.send("== CONSULTAR TODOS LOS PERSONAJES (MySQL) ==\n Enter para continuar".encode())
            cursor = db_conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_MYSQL_1}")
            resultados = cursor.fetchall()
            for fila in resultados:
                conn.send(f"ID: {fila[0]}, Nombre: {fila[1]}, Elemento: {fila[2]}, Genero: {fila[3]}, Rareza: {fila[4]}, Juego ID: {fila[5]}\n".encode())
            cursor.close()
            conn.send("PARA CONTINUAR 'ENTER' ".encode())
            collection_MYSQL_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

        elif msg == "2": #? Consultar personaje por NOMBRE
            log_info("Seleccionada la opcion: Consultar personaje por NOMBRE")
            conn.send("Introduce el NOMBRE del personaje a consultar: ".encode())
            NOMBRE = conn.recv(1024).decode().capitalize()
            log_info(f"Nombre del personaje recibido: {NOMBRE}")
            cursor = db_conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_MYSQL_1} WHERE nombre = %s", (NOMBRE))
            fila = cursor.fetchone()
            if fila:
                conn.send(f"Personaje encontrado: ID: {fila[0]}, Nombre: {fila[1]}, Elemento: {fila[2]}, Genero: {fila[3]}, Rareza: {fila[4]}, Juego ID: {fila[5]}\nPARA CONTINUAR 'ENTER' ".encode())
            else:
                conn.send("Personaje no encontrado.\nPARA CONTINUAR 'ENTER' ".encode())
            cursor.close()
            collection_MYSQL_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

        elif msg == "3": #? Otras consultas
            log_info("Seleccionada la opcion: Otras consultas")
            conn.send("== OTRAS CONSULTAS (MySQL) ==\n".encode())
            # TODO: Implementar otras consultas
            conn.send("PARA CONTINUAR 'ENTER' ".encode())
            collection_MYSQL_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

    elif msg == "4": #? Volver a las opciones
        log_info("Seleccionada la opcion: Volver a las opciones")
        collection_MYSQL_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion


def collection_MYSQL_2(conn:socket.socket): # Juegos
    pass



def collection_MYSQL_3(conn:socket.socket): # Empresa
    pass


#TODO: CONSULTAS A MONGODB
def collection_MDB_1(conn:socket.socket): # Personajes
    conn.send("== SELECCION COLECCION: PERSONAJES ==\n"\
    "¿Que quieres hacer?\n"\
    "1. Insertar Personajes\n" \
    "2. Consultar Personajes\n" \
    "3. Volver a las opciones\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")

    collection_1 = client[DB_MONGO][COLLECTION_MONGO_1]

    if msg == "1": #? Insertar - Personajes
        log_info("Seleccionada la opcion: Insertar Personajes")
        conn.send("== INSERTAR PERSONAJES ==\n"\
        "Introduce el NOMBRE del personaje: ".encode())
        NOMBRE = conn.recv(1024).decode().capitalize()
        log_info(f"Nombre del personaje recibido: {NOMBRE}")
        conn.send("Introduce el ELEMENTO del personaje: ".encode())
        ELEMENTO = conn.recv(1024).decode()
        log_info(f"Elemento del personaje recibido: {ELEMENTO}")
        conn.send("Introduce la RAREZA del personaje: ".encode())
        RAREZA = conn.recv(1024).decode()
        log_info(f"Rareza del personaje recibido: {RAREZA}")
        conn.send("Introduce el ID del juego al que pertenece: ".encode())
        ID_JUEGO = conn.recv(1024).decode()
        log_info(f"ID del juego recibido: {ID_JUEGO}")

        # INSERTAR DATOS EN MONGODB
        
        data ={
            "id": str(collection_1.count_documents({}) + 1),  # Genera un ID unico
            "nombre": NOMBRE,
            "elemento": ELEMENTO,
            "rareza": RAREZA,
            "id_juego": ID_JUEGO
        }

        collection_1.insert_one(data)
        log_info(f"Datos insertados en MongoDB: {data}")
        conn.send("Personaje insertado correctamente.\nPARA CONTINUAR 'ENTER' ".encode())
        collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

    elif msg == "2": #? Consultar - Personajes
        conn.send("== CONSULTAR PERSONAJES ==\n"\
        "¿Que quieres hacer?\n"\
        "1. Consultar todos los personajes\n" \
        "2. Consultar personaje por NOMBRE\n" \
        "3. Otras consultas\n" \
        "4. Volver a las opciones\n".encode())
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
        log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")
        if msg == "1": #? Consultar todos los personajes
            log_info("Seleccionada la opcion: Consultar todos los personajes")
            
            # TODO: Añadir la consulta a MongoDB

            collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
        
        # TODO: CONSULTAS
        
        elif msg == "2": #? Consultar personaje por NOMBRE
            log_info("Seleccionada la opcion: Consultar personaje por NOMBRE")
            conn.send("Introduce el NOMBRE del personaje a consultar: ".encode())
            NOMBRE = conn.recv(1024).decode().capitalize()
            log_info(f"Nombre del personaje recibido: {NOMBRE}")
            personaje = collection_1.find_one({"nombre": NOMBRE})
            if personaje:
                conn.send(f"Personaje encontrado: {personaje['nombre']}, Elemento: {personaje['elemento']}, Rareza: {personaje['rareza']}, ID Juego: {personaje['juego_id']}\nPARA CONTINUAR 'ENTER' ".encode())
                log_info(f"Personaje encontrado: {personaje}")
                collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
            else:
                conn.send("Personaje no encontrado.\nPARA CONTINUAR 'ENTER' ".encode())
                log_warning(f"Personaje no encontrado: {NOMBRE}")
                collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
        
        
        
        # TODO: OTRAS CONSULTAS
        
        elif msg == "3": #? Otras consultas
            log_info("Seleccionada la opcion: Otras consultas")
            conn.send("== OTRAS CONSULTAS ==\n"\
            "¿Que quieres hacer?\n"\
            "1. Consultar personajes por ELEMENTO\n" \
            "2. Consultar personajes por RAREZA\n" \
            "3. Consultar personajes por GENERO\n" \
            "4. Volver a las opciones\n".encode())
            msg = conn.recv(1024).decode()
            log_info(f"Mensaje recibido: {msg}")	
            time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
            log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")

            if msg == "1": # Consultar personajes por ELEMENTO
                log_info("Seleccionada la opcion: Consultar personajes por ELEMENTO")
                conn.send("Introduce el ELEMENTO a consultar:".encode())
                ELEMENTO = conn.recv(1024).decode().capitalize()
                log_info(f"Elemento recibido: {ELEMENTO}")
                personajes = collection_1.find({"elemento": ELEMENTO})
                if personajes:
                    _list =[f"Elemento: {p['elemento']}, Nombre: {p['nombre']}, Rareza: {p['rareza']}" for p in personajes]
                    conn.send("\n".join(_list).encode())
                    collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
                else:
                    conn.send("No se encontraron personajes con ese elemento.\n".encode())
                    collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

            elif msg == "2": #? Consultar personajes por RAREZA
                log_info("Seleccionada la opcion: Consultar personajes por RAREZA")
                conn.send("Introduce la RAREZA a consultar:".encode())
                RAREZA = conn.recv(1024).decode().capitalize()
                log_info(f"Rareza recibida: {RAREZA}")
                personajes = collection_1.find({"rareza": RAREZA})
                if personajes:
                    _list =[f"Elemento: {p['elemento']}, Nombre: {p['nombre']}, Rareza: {p['rareza']}" for p in personajes]
                    conn.send("\n".join(_list).encode())
                    collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion
                else:
                    conn.send("No se encontraron personajes con esa rareza.\n".encode())
                    collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

            elif msg == "3": #? Consultar personajes por GENERO
                log_info("Seleccionada la opcion: Consultar personajes por GENERO")
                conn.send("Introduce el GENERO a consultar:".encode())
                GENERO = conn.recv(1024).decode().capitalize()
                log_info(f"Género recibido: {GENERO}")
                personajes = collection_1.find({"genero": GENERO})
                if personajes:
                    _list =[f"Elemento: {p['elemento']}, Nombre: {p['nombre']}, Rareza: {p['rareza']}" for p in personajes]
                    conn.send("\n".join(_list).encode())
                    collection_MDB_1(conn)
                else:
                    conn.send("No se encontraron personajes con ese género.\n".encode())
                    collection_MDB_1(conn)  # Reinicia la funcion para que se pueda hacer otra operacion

    elif msg == "3": #? Volver a las opciones de MongoDB
        log_info("Seleccionada la opcion: Volver a las opciones")
        conn.send("Volviendo a las opciones...\n PRESIONA ENTER PARA CONFIRMAR".encode())
        time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
        log_debug(f"Esperar {tiempo_espera}s antes de volver a las opciones")
        MongoDB(conn)

def collection_MDB_2(conn:socket.socket): # Juegos
    conn.send("== SELECCION COLECCION: JUEGOS ==\n"\
    "¿Que quieres hacer?\n"\
    "1. Insertar Juegos\n" \
    "2. Consultar Juegos\n" \
    "3. Volver a las opciones\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")

    collection_2 = client[DB_MONGO][COLLECTION_MONGO_2]
    if msg == "1": #? Insertar - Juegos
        log_info("Seleccionada la opcion: Insertar Juegos")
        conn.send("== INSERTAR JUEGOS ==".encode())
        conn.send("Introduce el NOMBRE del juego: ".encode())
        NOMBRE = conn.recv(1024).decode().capitalize()
        log_info(f"Nombre del juego recibido: {NOMBRE}")
        conn.send("Introduce el GENERO del juego: ".encode())
        GENERO = conn.recv(1024).decode().capitalize()
        log_info(f"Género del juego recibido: {GENERO}")
        conn.send("Introduce la ID de la EMPRESA del juego: ".encode())
        ID_EMPRESA = conn.recv(1024).decode()
        log_info(f"ID de la empresa del juego recibido: {ID_EMPRESA}")
        
        data ={
            "id": str(collection_2.count_documents({}) + 1),  # Genera un ID unico
            "nombre": NOMBRE,
            "genero": GENERO,
            "empresa_id": ID_EMPRESA
        }

        collection_2.insert_one(data)
        conn.send("Juego insertado correctamente.\n".encode())
        collection_MDB_2(conn)

def collection_MDB_3(conn:socket.socket): # Empresa
    conn.send("== SELECCION COLECCION: EMPRESAS ==\n"\
    "¿Que quieres hacer?\n"\
    "1. Insertar Empresas\n" \
    "2. Consultar Empresas\n" \
    "3. Volver a las opciones\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")

    collection_3 = client[DB_MONGO][COLLECTION_MONGO_3]

    if msg == "1": #? Insertar - Empresas
        log_info("Seleccionada la opcion: Insertar Empresas")
        conn.send("== INSERTAR EMPRESA ==\n Introduce el NOMBRE de la empresa:".encode())
        NOMBRE = conn.recv(1024).decode().capitalize()
        log_info(f"Nombre de la empresa recibido: {NOMBRE}")
        data = {
            "id": str(collection_3.count_documents({}) + 1),  # Genera un ID unico
            "nombre": NOMBRE
        }
        collection_3.insert_one(data)
        log_info(f"Datos insertados en MongoDB: {data}")
        conn.send("Empresa insertada correctamente.".encode())
        collection_MDB_3(conn)


# TODO: METODOS DE CONSULTAS A LA BASE DE DATOS ELEGIDA

#TODO: MONGODB
def MongoDB(conn: socket.socket):
    conn.send("== SELECCION MONGODB ==\n"\
    "¿Con que coleccion quieres trabajar?\n"\
    "1. Personajes\n" \
    "2. Juegos\n" \
    "3. Empresa (SI SE VA AÑADIR UN JUEGO, NECESITA SU EMPRESA)\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MongoDB")

    if msg == "1":
        log_info("Seleccionada la coleccion: Personajes")
        collection_MDB_1(conn)
    elif msg == "2":
        log_info("Seleccionada la coleccion: Juegos")
        collection_MDB_2(conn)
    elif msg == "3":
        log_info("Seleccionada la coleccion: Empresa")
        collection_MDB_3(conn)



#TODO: MySQL
def MySQL(conn: socket.socket):
    conn.send("== SELECCION MySQL ==\n"\
    "¿Con que coleccion quieres trabajar?\n"\
    "1. Personajes\n" \
    "2. Juegos\n" \
    "3. Empresa (SI SE VA AÑADIR UN JUEGO, NECESITA SU EMPRESA)\n".encode())
    msg = conn.recv(1024).decode()
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_debug(f"Esperar {tiempo_espera}s antes de continuar con la consulta a MySQL")

    if msg == "1":
        log_info("Seleccionada la coleccion: Personajes")
        collection_MYSQL_1(conn)




















#TODO: SERVIDOR PRINCIPAL
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Configuracion del socket, puerto y host
        log_info(f"Servidor iniciado en {HOST}:{PORT}")
        s.listen(5)
        log_info(f"Servidor escuchando en {HOST}:{PORT}")
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            log_debug(f"Esperar 5s")
            time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
            with conn:
                log_info(f"Conexion establecida desde {addr}")
                print(f"Conexion establecida desde {addr}")

                conn.send("Elige una opcion: 1. MongoDB 2. MySQL 3. Salir\nEscribe un numero: ".encode())
                msg = conn.recv(1024).decode()
                
                log_debug(f"Esperar 5s")
                time.sleep(tiempo_espera)

                if msg == "1":
                    print("[Client] Opcion 1 seleccionada: MongoDB")
                    log_info("[Client] Opcion 1 seleccionada: MongoDB")
                    MongoDB(conn)

                elif msg == "2":
                    print("[Client] Opcion 2 seleccionada: MySQL")
                    log_info("[Client] Opcion 2 seleccionada: MySQL")
                    MySQL(conn)

                elif msg == "3":
                    print("[Client] Opcion 3 seleccionada: Salir")
                    log_info("[Client] Opcion 3 seleccionada: Salir")
                    conn.close()
                    break

                else:
                    print("[Client] Opcion invalida")
                    log_info("[Client] Opcion invalida")
                    conn.send(f"Opcion invalida".encode())
                    break
                


if __name__ == "__main__":
    start_server()
    log_info("Servidor iniciado correctamente.")


