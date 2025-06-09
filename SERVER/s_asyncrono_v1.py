
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


# TODO: =============== CONFIGURACION CONEXION MySQL ================
def get_MySQL_conn():
    return mysql.connector.connect(
        host = HOST_MySQL, 
        user = USER_MySQL,
        password = PASSWORD_MySQL,
        database = DB_MySQL
    )




# TODO: =============== PETICIONES (TABLAS_COLECCIONES) ================

# TODO: =============== CONSULTAS MongoDB ================
async def collection_MDB_4(writer: asyncio.StreamWriter, reader: asyncio.StreamReader):
    #? COLECCIONES A USAR
    COL_J = CLIENT_MDB[COLLECTION_MONGO_2]
    COL_P = CLIENT_MDB[COLLECTION_MONGO_4]

    
    writer.write("Selecciona una opción:\n1. Insertar \n2. Consultar todos los elementos  \n3.Otro tipo de consulta \n4.Salir".encode())
    await writer.drain()
    msg = await reader.read(1024)
    
    if msg == "1":
        log_info(f"[CLIENT - MONGODB] INSERTAR ELEMENTO EN LA COLECCION '{COLLECTION_MONGO_4}")
        print(f"[CLIENT - MONGODB] INSERTAR ELEMENTO EN LA COLECCION '{COLLECTION_MONGO_4}")
        # TODO: CAMPOS QUE NO SON NULOS
        writer.write("NOMBRE".encode())
        await writer.drain()
        nombre = await reader.read(1024)
        nombre = nombre.capitalize()
        writer.write("GENERO".encode())
        await writer.drain()
        genero = await reader.read(1024)
        genero = genero.capitalize()
        writer.write("FACCION".encode())
        await writer.drain()
        faccion = await reader.read(1024)
        faccion = faccion.capitalize()
        jg_list = "LISTA DE JUEGOS ACTUALES: \n"
        for jg in COL_J.find():
            jg_list += f"{jg['id']} - {jg['nombre']}\n"
        writer.write(jg_list.encode())
        await writer.drain()
        writer.write("ID JUEGO".encode())
        await writer.drain()
        id = await reader.read(1024)
        writer.write("OTROS CAMPOS (opcional) \n 1.Arma, elemento y rareza 2. Elemento solo 3. Arma solo".encode())
        await writer.drain()
        msg = await reader.read(1024)
        
        if msg == "1":
            writer.write("TIPO DE ARMA".encode())
            await writer.drain()
            arma = await reader.read(1024)
            arma = arma.capitalize()
            writer.write("ELEMENTO".encode())
            await writer.drain()
            elemento = await reader.read(1024)
            elemento = elemento.capitalize()
            
            writer.write("RAREZA".encode())
            await writer.drain()
            rareza = await reader.read(1024)
            rareza = rareza.capitalize()
            #? INSERTAR EN LA COLECCION
            data = {
                "id": COL_P.count_documents({}) + 1,
                "nombre": nombre,
                "genero": genero,
                "elemento": elemento,
                "arma": arma,
                "rareza": rareza,
                "faccion": faccion,
                "id_juego": int(id)
            }
        
        if msg == "2":
            writer.write("ELEMENTO".encode())
            await writer.drain()
            elemento = await reader.read(1024)
            elemento = elemento.capitalize()
            #? INSERTAR EN LA COLECCION
            data = {
                "id": COL_P.count_documents({}) + 1,
                "nombre": nombre,
                "genero": genero,
                "elemento": elemento,
                "arma": None,
                "rareza": None,
                "faccion": faccion,
                "id_juego": int(id)
            }
        if msg == "3":
            writer.write("TIPO DE ARMA".encode())
            await writer.drain()
            arma = await reader.read(1024)
            arma = arma.capitalize()
            #? INSERTAR EN LA COLECCION
            data = {
                "id": COL_P.count_documents({}) + 1,
                "nombre": nombre,
                "genero": genero,
                "elemento": None,
                "arma": arma,
                "rareza": None,
                "faccion": faccion,
                "id_juego": int(id)
            }






# TODO: =============== CONSULTAS MySQL ================




# TODO: =============== CONFIGURACION CONEXION BASES DE DATOS, SELECCION DE TABLAS ================


async def consultas_MDB(writer: asyncio.StreamWriter, reader: asyncio.StreamReader):
    writer.write("Consultar datos en MongoDB, seleccionar la colección:\n1. Empresa\n2. Juegos\n3. Personajes(OPCION DISPONIBLE)\n4. Salir".encode())
    await writer.drain()
    
    msg = await reader.read(1024)
    if not msg:
        log_warning("Cliente desconectado.")
        print("Cliente desconectado.")
        return
    option = msg.decode().strip()
    log_debug(f"Opción seleccionada: {option}")
    print(f"Opción seleccionada: {option}")
    if option == "3":
        log_info("Consultando datos de la colección 'Personajes' en MongoDB...")
        writer.write("Consultando datos de la colección 'Personajes' en MongoDB...\n".encode())
        await writer.drain()
        await collection_MDB_4(writer, reader)









# TODO: =============== SERVIDOR ================

async def client_communication_server (reader, writer):
    addr = writer.get_extra_info('peername')
    log_info(f"Conexión desde {addr}")
    print(f"Conexión desde {addr}")
    writer.write("CONEXIÓN ESTABLECIDA CORRECTAMENTE CON EL SERVIDOR.".encode())
    await writer.drain()

    while True:
        await asyncio.sleep(5)
        log_warning("== ESPERA AUTOMÁTICA DE 5 SEGUNDOS ==")
        writer.write("En espera".encode())
        await writer.drain()
        writer.write("ELIGE UNA OPCIÓN:\n1. Consultar datos de MongoDB\n2. Consultar datos de MySQL\n4. Salir".encode())
        await writer.drain()
        msg = await reader.read(1024)
        if not msg:
            log_warning("Cliente desconectado.")
            print("Cliente desconectado.")
            break
        option = msg.decode().strip()
        log_debug(f"Opción seleccionada: {option}")
        print(f"Opción seleccionada: {option}")
        if option == "1":
            log_info("Consultando datos de MongoDB...")
            writer.write("Consultando datos de MongoDB...\n".encode())
            await writer.drain()
            await consultas_MDB(writer, reader)

        elif option == "2":
            log_info("Consultando datos de MySQL...")
            writer.write("Consultando datos de MySQL...\n".encode())
            await writer.drain()
            # consultas_MySQL(writer)
        elif option == "4":
            log_info("Cerrando conexión con el cliente.")
            writer.write("Cerrando conexión con el cliente.\n".encode())
            await writer.drain()
            break
        else:
            log_warning("Opción no válida, por favor intente nuevamente.")
            writer.write("Opción no válida, por favor intente nuevamente.\n".encode())
        await writer.drain()


async def main():
    try:
        server = await asyncio.start_server(
            client_communication_server, Shost, Sport
        )
        log_info(f"Servidor escuchando en {Shost}:{Sport}")
        print(f"Servidor escuchando en {Shost}:{Sport}")
        async with server:
            await server.serve_forever()
    except Exception as e:
        log_error(f"Error al iniciar el servidor: {e}")
        print(f"Error al iniciar el servidor: {e}")
    except KeyboardInterrupt:
        log_warning("Servidor detenido por el usuario.")
        print("Servidor detenido por el usuario.")
    finally:
        log_critical("Servidor cerrado.")
        print("Servidor cerrado.")


if __name__ == "__main__":
    asyncio.run(main())