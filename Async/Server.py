import asyncio
from Logs import log_critical, log_debug, log_error, log_info, log_warning

from pymongo import MongoClient
import mysql.connector 

# TODO =============== CONFIGURACIONES ================

# ? Servidor configuration
Shost = "localhost"
Sport = 8083

# ? MongoDB

M_URL = "mongodb://localhost:27017/"
M_DB = ""

# ? MySQL
DB_MySQL = "asyncro_db"
USER_MySQL = "pithon_asy"
PASSWORD_MySQL = "321_ytrewq"
HOST_MySQL = "localhost"

TABLE_MySQL_1 = "Terminal"
TABLE_MySQL_2 = "Incidencia"
TABLE_MySQL_3 = "Tecnico"
TABLE_MySQL_4 = "Inventario"
TABLE_MySQL_5 = "Zona"
TABLE_MySQL_6 = "Ubicacion"
TABLE_MySQL_7 = "Tecnico_zona"
TABLE_MySQL_8 = "Teleoperador"
TABLE_MySQL_9 = "Terminal_estado_historial"
