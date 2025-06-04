
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



    except Exception as e:
        print (f"Se ha producido un error al iniciar el servidor: {e}")
        log_error(f"Error al iniciar el servidor: {e}")
    




start()