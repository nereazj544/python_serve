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
from Logs import log_info, log_error, log_warning, log_debug, log_critical  # Para manejar los logs


# * ==========================================================


