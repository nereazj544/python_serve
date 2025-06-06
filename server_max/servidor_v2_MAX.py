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



#* =============== CONFIGURACIONES ================
#? Configuración de la base de datos MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_MONGO = "Max_2"









