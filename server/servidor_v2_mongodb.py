
# ! librerias
import socket # Configuracion del servidor y cliente
import time # Para manejar tiempos de espera y pausas
from pymongo import MongoClient

from Logs import log_info, log_error, log_warning, log_debug, log_critical

# Configuraciones de conexión - MongoDB
HOST = "localhost"
PORT = 8080
tiempo_espera = 5  # Tiempo de espera en segundos



DB_name = "ZOO"
COLLECTION_1 = "ANIMALES"


client = MongoClient("mongodb://localhost:27017/")



def collection_animales(conn: socket.socket):
    log_info(f"Seleccionada la colección: {COLLECTION_1}")
    time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar
    conn.send("\n¿Qué quieres hacer? 1. Insertar 2. Buscar 3. Borrar Animal 4. Salir".encode())
    while True:
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        if msg == "1":
            collection = client[DB_name][COLLECTION_1]
            conn.send("\nIngrese el NOMBRE del animal a AÑADIR: ".encode())
            nombre = conn.recv(1024).decode().capitalize()
            data = {
                "id": collection.count_documents({}) + 1,
                "nombre": nombre
            }
            collection.insert_one(data)
            conn.send("Animal insertado correctamente. PARA CONTINUAR 'ENTER'".encode())
            log_info(f"Animal insertado: {data}")
            collection_animales(conn) #Reinicia la funcion para que se pueda hacer otra operacion
        elif msg == "2":
            collection = client[DB_name][COLLECTION_1]
            conn.send("\nIngrese el NOMBRE del animal a BUSCAR: ".encode())
            nombre = conn.recv(1024).decode()
            animal = collection.find_one({"nombre": nombre.capitalize()})
            if animal:
                conn.send(f"Animal encontrado: {nombre} número del animal: {animal['id']}\nPARA CONTINUAR 'ENTER' ".encode())
            else:
                conn.send("Animal no encontrado.".encode())
            collection_animales(conn) # Reinicia la funcion para que se pueda hacer otra operacion
        elif msg == "3":
            collection = client[DB_name][COLLECTION_1]
            conn.send("\nIngrese el NOMBRE del animal a BORRAR: ".encode())
            nombre = conn.recv(1024).decode()
            result = collection.delete_one({"nombre": nombre.capitalize()})
            if result.deleted_count > 0:
                conn.send(f"Animal {nombre} borrado correctamente.\nPARA CONTINUAR 'ENTER' ".encode())
                log_info(f"Animal {nombre} borrado correctamente.")
            else:
                conn.send(f"Animal {nombre} no encontrado.\nPARA CONTINUAR 'ENTER' ".encode())
                log_warning(f"Animal {nombre} no encontrado.")
            #TODO: Implementar la opcion de salir





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

                conn.send("Elige una coleccion:\n1. Animales 2. Salir\nEscribe un número: ".encode())
                msg = conn.recv(1024).decode()
                print(f"Mensaje recibido: {msg}")
                log_info(f"Mensaje recibido: {msg}")
                time.sleep(tiempo_espera)  # Espera de 5 segundos antes de continuar

                #TODO: OPCIONES DE USO EN LA COLECCION
                if msg == "1":
                    print(f"Coleccion seleccionada: {COLLECTION_1}")
                    log_info(f"Coleccion seleccionada: {COLLECTION_1}")
                    collection_animales(conn)
                    time.sleep(tiempo_espera)

                elif msg == "2":
                    print("Saliendo del servidor...")
                    log_info("Saliendo del servidor...")
                    conn.send("Saliendo del servidor...".encode())
                    break





if __name__ == "__main__":
    start_server()