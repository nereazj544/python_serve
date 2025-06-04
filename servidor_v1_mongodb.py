
#! LIBRERIAS 
from pymongo import MongoClient
import socket
from Logs import log_info, log_error, log_warning, log_debug, log_critical



# TODO: CONFIGURACIONES DE CONEXION - MONGODB
HOST = "localhost"
PORT = 8080

DB = "test_python_db"
COLLECTION_1 = "empresas"
COLLECTION_2 = "personajes"
COLLECTION_3 = "Lenguajes"

def COLLECTION_empresas():
    
    raise NotImplementedError

def COLLECTION_personajes():
    raise NotImplementedError

def COLLECTION_lenguajes():
    raise NotImplementedError


#! SERVIDOR

def start():
    print(". . . SERVER ON . . .")
    log_info("Servidor iniciado correctamente.")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        log_info(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Conexión establecida desde {addr}")
            log_info(f"Conexión establecida desde {addr}")
            msg = conn.recv(1024).decode()
            print(f"Mensaje recibido: {msg}")
            log_info(f"Mensaje recibido: {msg}")

            if msg == "1":
                print(f"Coleccion seleccionada: {COLLECTION_1}")
                log_info(f"Coleccion seleccionada: {COLLECTION_1}")
                COLLECTION_empresas()
            elif msg == "2":
                print(f"Coleccion seleccionada: {COLLECTION_2}")
                log_info(f"Coleccion seleccionada: {COLLECTION_2}")
                COLLECTION_personajes()
            elif msg == "3":
                print(f"Coleccion seleccionada: {COLLECTION_3}")
                log_info(f"Coleccion seleccionada: {COLLECTION_3}")
                COLLECTION_lenguajes()

    except Exception as e:
        print (f"Se ha producido un error al iniciar el servidor: {e}")
        log_error(f"Error al iniciar el servidor: {e}")
    




start()