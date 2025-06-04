
# ! librerias
import socket # Configuracion del servidor y cliente
import time # Para manejar tiempos de espera y pausas
from pymongo import MongoClient

from Logs import log_info, log_error, log_warning, log_debug, log_critical

# Configuraciones de conexión - MongoDB
HOST = "localhost"
PORT = 8080

DB = "test_python_db"
COLLECTION_1 = "empresas"
COLLECTION_2 = "personajes"
COLLECTION_3 = "Lenguajes"
tiempo_espera = 5  # Tiempo de espera en segundos
client = MongoClient("mongodb://localhost:27017/")

def collection_empresas(conn: socket.socket):
    
    
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    log_info(f"Seleccionada la colección: {COLLECTION_1}")
    conn.send("\n¿Qué quieres hacer? 1. Insertar 2. Buscar 3. Salir".encode())
    while True:
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        if msg == "1":
            collection = client[DB][COLLECTION_1]
            conn.send("\nIngrese el NOMBRE de la empresa: ".encode())
            nombre = conn.recv(1024).decode()
            data = {
                "id": collection.count_documents({}) + 1,
                "nombre": nombre
            }
            collection.insert_one(data)
            conn.send("Empresa insertada correctamente. PARA CONTINUAR 'ENTER'".encode())
            log_info(f"Empresa insertada: {data}")
            collection_empresas(conn)  # Reinicia la función para permitir más acciones
        elif msg == "2":
            collection = client[DB][COLLECTION_1]
            conn.send("\nIngrese el NOMBRE de la empresa a buscar: ".encode())
            nombre = conn.recv(1024).decode()
            empresa = collection.find_one({"nombre": nombre})
            if empresa:
                conn.send(f"Empresa encontrada: {nombre} número de la empresa: {empresa['id']}\nPARA CONTINUAR 'ENTER' ".encode())
            else:
                conn.send("Empresa no encontrada.".encode())
            collection_empresas(conn)  # Reinicia la función para permitir más acciones
        elif msg == "3":
            conn.send('Saliendo...'.encode())
            log_info("Saliendo de la colección de empresas.")
            break







# TODO: START SERVER
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        log_info(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print (f"Conexion establecida desde {addr}")
                log_info(f"Conexión establecida desde {addr}")

                conn.send("Elige una coleccion:\n1. Empresas \n2. Personajes \n3. Lenguajes \nEscribe un número: ".encode())
                msg = conn.recv(1024).decode()
                print(f"Mensaje recibido: {msg}")
                log_info(f"Mensaje recibido: {msg}")
                time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
                if msg == "1":
                    print(f"Coleccion seleccionada: {COLLECTION_1}")
                    conn.send(f"Coleccion seleccionada: {COLLECTION_1}\n ENTER".encode())
                    
                    log_info(f"Coleccion seleccionada: {COLLECTION_1}")

                    time.sleep(tiempo_espera)
                    collection_empresas(conn)
                elif msg == "2":
                    print(f"Coleccion seleccionada: {COLLECTION_2}")
                    log_info(f"Coleccion seleccionada: {COLLECTION_2}")
                    # collection_personajes(conn)


if __name__ == "__main__":
    start_server()