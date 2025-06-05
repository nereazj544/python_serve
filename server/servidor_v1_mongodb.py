
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

def COLLECTION_empresas(conn):
    
    conn.send("Has seleccionado la coleccion de empresas.".encode())
    # Aquí iría la lógica para manejar la colección de empresas
    mgs = "¿Que quieres hacer? 1. Insertar 2. Buscar 3. Salir"
    conn.send(mgs.encode())
    while True:
        msg = conn.recv(1024).decode()
        if msg == "1":
            # Lógica para insertar en la colección de empresas
            conn.send("Insertar en la colección de empresas.".encode())
            client = MongoClient("mongodb://localhost:27017/")
            db = client[DB]
            collection = db[COLLECTION_1]
            nombre = input("Ingrese el nombre de la empresa: ")
            data = {
                "id": collection.count_documents({}) + 1,
                "nombre": nombre
            }
            collection.insert_one(data)
            conn.send("Empresa insertada correctamente.".encode())
        elif msg == "2":
            # Lógica para buscar en la colección de empresas
            conn.send("Buscar en la colección de empresas.".encode())
            client = MongoClient("mongodb://localhost:27017/")
            db = client[DB]
            collection = db[COLLECTION_1]
            nombre = input("Ingrese el nombre de la empresa a buscar: ")
            empresa = collection.find_one({"nombre": nombre})
            if empresa:
                conn.send(f"Empresa encontrada: {empresa} numero de la empresa: {empresa['id']}".encode())
            else:
                conn.send("Empresa no encontrada.".encode())
        elif msg == "3":
            conn.send("Saliendo...".encode())
            break
        else:
            conn.send("Opción no válida. Intente nuevamente.".encode())

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
                COLLECTION_empresas(conn)
            elif msg == "2":
                print(f"Coleccion seleccionada: {COLLECTION_2}")
                log_info(f"Coleccion seleccionada: {COLLECTION_2}")
                # COLLECTION_personajes(conn)
            elif msg == "3":
                print(f"Coleccion seleccionada: {COLLECTION_3}")
                log_info(f"Coleccion seleccionada: {COLLECTION_3}")
                # COLLECTION_lenguajes()

    except Exception as e:
        print (f"Se ha producido un error al iniciar el servidor: {e}")
        log_error(f"Error al iniciar el servidor: {e}")

start()