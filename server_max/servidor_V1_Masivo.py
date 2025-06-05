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

# TODO: METODOS DE CONSULTAS A LA BASE DE DATOS ELEGIDA




















#TODO: SERVIDOR PRINCIPAL
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Configuracion del socket, puerto y host
        log_info(f"Servidor iniciado en {HOST}:{PORT}")
        s.listen(5)
        log_info(f"Servidor escuchando en {HOST}:{PORT}")
        print(f"Servidor escuchando en {HOST}:{PORT}")





if __name__ == "__main__":
    start_server()
    log_info("Servidor iniciado correctamente.")


