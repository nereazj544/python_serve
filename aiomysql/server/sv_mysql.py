import asyncio
import aiomysql
from Logs import log_critical, log_info, log_error, log_warning, log_debug
from aiomysql import create_pool



#todo: configuracion de la base de datos
MySQL_HOST = 'localhost'
MySQL_USER = 'api_python'
MySQL_PASSWORD = '321_ytrewq'
MySQL_DB = 'zoo'

async def connect():
    conn = await aiomysql.connect(
        host=MySQL_HOST,
        user=MySQL_USER,
        password=MySQL_PASSWORD,
        db=MySQL_DB
    )
    return conn
