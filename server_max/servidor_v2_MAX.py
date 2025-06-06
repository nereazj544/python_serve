'''
SERVIDOR V2 MAX
Lo mismo que el v1 pero con más cosas en la base de datos. XD  (COMPLICANDOSE LA VIDA, EN VEZ DE HACERLO MÁS FÁCIL COMO EN EL V1)

'''

#! IMPORTS
    #? SOCKETS
import socket
import time

    #? DataBase
from pymongo import MongoClient
import mysql.connector

    #? Logs
from logs.Logs_Masivo_V2 import log_info, log_error, log_warning, log_debug, log_critical



# TODO =============== CONFIGURACIONES ================
#? Configuración del servidor
Shost = "localhost"
Sport = 8083
tiempo_espera = 5  # Tiempo de espera en segundos para la conexión


#? Configuración de la base de datos MongoDB

MONGO_URI = MongoClient("mongodb://localhost:27017/")
DB_MONGO = "Max_2"
COLLECTION_MONGO_1= "Empresa"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Juegos_plataformas"
COLLECTION_MONGO_4 = "Personajes"


#? Configuración de la base de datos MySQL
DB_MySQL = "db_python"
USER_MySQL = "test_pithon"
PASSWORD_MySQL = "321_atomica"
HOST_MySQL = "localhost"

TABLE_MySQL_1 = "Empresa"
TABLE_MySQL_2 = "Juegos"
TABLE_MySQL_3 = "Juegos_plataformas"
TABLE_MySQL_4 = "Personajes"



# TODO: =============== CONFIGURACION CONEXION MySQL ================
def get_MySQL_conn():
    return mysql.connector.connect(
        host = HOST_MySQL, 
        user = USER_MySQL,
        password = PASSWORD_MySQL,
        database = DB_MySQL
    )

# TODO: =============== PETICIONES (TABLAS_COLECCIONES) ================

# TODO: =============== CONSULTAS MongoDB ================


# TODO: =============== CONSULTAS MySQL ================

#? PERSONAJES
def consulta_table4_mysql(conn: socket.socket):
    get_MySQL_conn() # Conexión a la base de datos MySQL
    log_warning(f"== EN ESPERA AUTOMATICA DE 5s ==")
    time.sleep(tiempo_espera)

    conn.send("=============== CONSULTAS PERSONAJES MySQL ==============\n" \
        "\n 1. Insertar personaje"\
        "\n 2. Ver todos los personajes"\
        "\n 3. Otras busquedas"\
        "\n 4."\
        .encode)
    
    msg = conn.recv(1024).decode()
    
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)
    log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")

    if msg == "1":
        log_info("[CLIENT] OPCION INSERTAR PERSONAJE")
        
        #? 





# TODO: =============== CONFIGURACION CONEXION BASES DE DATOS, SELECCION DE TABLAS ================

#TODO: CONFIGURACION DE MONGO DB
def consultas_MongoDB(conn: socket.socket):
    while True:
        conn.send("=============== CONSULTAS MONGO DB ==============\n" \
            "\n 1. Personajes" \
            "\n 2. Empresas" \
            "\n 3. Juegos (ANTES DE METER EL JUEGO, SE NECESITA SU NUMERO DE EMPRESA)" \
            "\n 4. Salir" \
        "".encode())
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")

        if msg == "1":
            log_info("[CLIENT] OPCION PERSONAJES")
            # collection_MDB_4(conn)
        elif msg == "2":
            log_info("[CLIENT] OPCION EMPRESAS")
            conn.send("SIN CONFIGURAR".encode())
            # collection_MDB_1(conn)
        elif msg == "3":
            log_info("[CLIENT] OPCION JUEGOS")
            conn.send("SIN CONFIGURAR".encode())
            # collection_MDB_2(conn)
        elif msg == "4":
            log_info("[CLIENT] OPCION SALIR")
            conn.send("Saliendo de MongoDB...".encode())
            conn.close()
        else: 
            log_error(f"Mensaje no reconocido: {msg}")
            conn.send("Opción no válida. Inténtalo de nuevo.".encode())
            consultas_MongoDB(conn)




#TODO: CONFIGURACION DE MySQL
def consultas_MySQL(conn: socket.socket):
    while True:
        conn.send("=============== CONSULTAS MySQL ==============\n" \
            "\n 1. Personajes" \
            "\n 2. Empresas" \
            "\n 3. Juegos (ANTES DE METER EL JUEGO, SE NECESITA SU NUMERO DE EMPRESA)" \
            "\n 4. Salir" \
        "".encode())

        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")

        if msg == "1":
            log_info("[CLIENT] OPCION PERSONAJES")
            consulta_table4_mysql(conn)
        elif msg == "2":
            log_info("[CLIENT] OPCION EMPRESAS")
            conn.send("SIN CONFIGURAR".encode())
            # consulta_table1_mysql(conn)
        elif msg == "3":
            log_info("[CLIENT] OPCION JUEGOS")
            conn.send("SIN CONFIGURAR".encode())
            # consulta_table2_mysql(conn)
        elif msg == "4":
            log_info("[CLIENT] OPCION SALIR")
            conn.send("Saliendo de MongoDB...".encode())
            conn.close()
        else: 
            log_error(f"Mensaje no reconocido: {msg}")
            conn.send("Opción no válida. Inténtalo de nuevo.".encode())
            consultas_MongoDB(conn)




# TODO: =============== SERVIDOR ================

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        log_info(f"Servidor iniciado en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            log_warning(f"== EN ESPERA AUTOMATICA DE 5s ==")
            time.sleep(tiempo_espera)
            log_info(f"Conexión aceptada de {addr}")

            with conn:
                log_info(f"Conexión establecida con {addr}")
                print(f"Conexión establecida con {addr}")

                conn.send("Bienvenido al servidor masivo v2. " \
                "\n Elige una opcion:"
                "\n 1. MongoDB"
                "\n 2. MySQL"
                "\n Escribe un numero: ".encode())

                msg = conn.recv(1024).decode()
                log_info(f"Mensaje recibido: {msg}")
                
                if msg == "1":
                    log_info("[CLIENT] OPCION MONNGODB")
                    conn.send("SELECCION MONGODB, ENTER PARA CONTINUAR".encode())
                    consultas_MongoDB(conn)
                elif msg == "2":
                    log_info("[CLIENT] OPCION MYSQL")
                    conn.send("SELECCION MYSQL, ENTER PARA CONTINUAR".encode())
                    consultas_MySQL(conn)
                else: 
                    log_error(f"Mensaje no reconocido: {msg}")
                    conn.send("Opción no válida. Inténtalo de nuevo.".encode())
                    continue



if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        log_error(f"Error al iniciar el servidor: {e}")
    finally:
        log_info("Servidor detenido.")
