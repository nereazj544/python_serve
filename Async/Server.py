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
M_DB = "tech_multiverso"

COLLECTION_MONGO_1 = "Terminal"
COLLECTION_MONGO_2 = "Incidencia"
COLLECTION_MONGO_3 = "Tecnico"
COLLECTION_MONGO_4 = "Inventario"
COLLECTION_MONGO_5 = "Zona"
COLLECTION_MONGO_6 = "Ubicacion"
COLLECTION_MONGO_7 = "Tecnico_zona"
COLLECTION_MONGO_8 = "Teleoperador"
COLLECTION_MONGO_9 = "Terminal_estado_historial"
COLLECTION_MONGO_10 = "Turnos"

# ? MySQL
DB_MySQL = "pithon"
USER_MySQL = "server_python"
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
TABLE_MySQL_10 = "Turnos"


# TODO =============== CONEXIONES_MySQL ================

def get_MySQL_conn():
    return mysql.connector.connect(
        host = HOST_MySQL,
        user = USER_MySQL,
        password = PASSWORD_MySQL,
        database = DB_MySQL
    )



# TODO: =============== PETICIONES (TABLAS_COLECCIONES) ================


# TODO: =============== CONFIGURACION CONEXION BASES DE DATOS, SELECCION DE TABLAS ================






































# TODO: =============== SERVIDOR ================

async def server(reader, writer):
    addr = writer.get_extra_info('peername')
    log_info(f"Conexión establecida desde {addr}")
    print(f"Conexión establecida desde {addr}")
    writer.write("CONECTADO CORRECTAMENTE AL SERVIDOR. \n ENTER PARA SEGUIR".encode())
    await writer.drain()

    while True:
        await asyncio.sleep(0.1)
        log_warning("== ESPERA AUTOMÁTICA DE O.1 SEGUNDOS ==")
        writer.write("ELIGE LA OPCION DESEADA: \n 1. TELEOPERADOR \n 2. TECNICO \n 3. SALIR \n".encode())
        await writer.drain()
        data = await reader.readline()
        message = data.decode().strip()
        log_debug(f"Mensaje recibido: {message}")
        print(f"Mensaje recibido: {message}")

        if message == "1":
            log_info("Seleccionado: TELEOPERADOR")
            writer.write("TELEOPERADOR SELECCIONADO. \n ESCRIBA CONTRASEÑA: ".encode())
            await writer.drain()
            password = (await reader.readline()).decode().strip()
            log_debug(f"Contraseña recibida: {password}")
            if password == "leo-perador._.2025":
                log_info("Contraseña correcta para TELEOPERADOR")
                writer.write("CONTRASEÑA CORRECTA. BIENVENIDO TELEOPERADOR.\n Escribe un numero: 1 o 2".encode())
                await writer.drain()
                data = await reader.readline()
                message = data.decode().strip()
                log_debug(f"Mensaje recibido: {message}")
                if message == "1": # MySQL
                    log_info("Seleccionado: Opción 1")
                    writer.write("Has seleccionado la opción 1. \n".encode())
                    await writer.drain()
                    # Aquí puedes agregar la lógica para la opción 1
                elif message == "2": # MongoDB
                    log_info("Seleccionado: Opción 2")
                    writer.write("Has seleccionado la opción 2. \n".encode())
                    await writer.drain()
                    # Aquí puedes agregar la lógica para la opción 2
                else:
                    log_warning("Opción no válida seleccionada por TELEOPERADOR")
                    writer.write("OPCIÓN NO VÁLIDA. INTENTE DE NUEVO.\n".encode())
                    await writer.drain()
                
            else:
                log_error("Contraseña incorrecta para TELEOPERADOR")
                writer.write("CONTRASEÑA INCORRECTA. INTENTE DE NUEVO.\n".encode())
                await writer.drain()