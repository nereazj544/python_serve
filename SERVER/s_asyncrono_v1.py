
# ! IMPORTS
import asyncio

# ? LOGS
from Logs.Logs import log_info, log_error, log_warning, log_debug, log_critical

# ? DataBase
from pymongo import MongoClient
import mysql.connector 


# TODO =============== CONFIGURACIONES ================
# ? Configuración del servidor
Shost = "localhost"
Sport = 8083



# ? Configuración de la base de datos MongoDB

MONGO_URI = MongoClient("mongodb://localhost:27017/")
DB_MONGO = "asyncro_db"
CLIENT_MDB = MONGO_URI[DB_MONGO]

COLLECTION_MONGO_1= "Empresa"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Juegos_plataformas"
COLLECTION_MONGO_4 = "Personajes"


# ? Configuración de la base de datos MySQL
DB_MySQL = "asyncro_db"
USER_MySQL = "pithon_asy"
PASSWORD_MySQL = "321_ytrewq"
HOST_MySQL = "localhost"

TABLE_MySQL_1 = "Empresa"
TABLE_MySQL_2 = "Juegos"
TABLE_MySQL_3 = "Juegos_plataformas"
TABLE_MySQL_4 = "Personajes"


