
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
async def collection_MDB_4(writer, reader):
    COL_J = CLIENT_MDB[COLLECTION_MONGO_2]
    COL_P = CLIENT_MDB[COLLECTION_MONGO_4]
    while True:
        menu = (
            "Selecciona una opción:\n"
            "1. Insertar\n"
            "2. Consultar todos los elementos\n"
            "3. Otro tipo de consulta\n"
            "4. Salir\n"
        )
        writer.write(menu.encode())
        await writer.drain()
        msg = (await reader.read(1024)).decode().strip()

        if msg == "1":
            #! --- Datos obligatorios ---
            writer.write("NOMBRE: ".encode())
            await writer.drain()
            nombre = (await reader.read(1024)).decode().strip().capitalize()

            writer.write("GENERO: ".encode())
            await writer.drain()
            genero = (await reader.read(1024)).decode().strip().capitalize()

            writer.write("FACCION: ".encode())
            await writer.drain()
            faccion = (await reader.read(1024)).decode().strip().capitalize()

            #! --- Mostrar juegos disponibles ---
            juegos = list(COL_J.find())
            jg_list = "LISTA DE JUEGOS ACTUALES:\n"
            for jg in juegos:
                jg_list += f"{jg.get('id')} - {jg.get('nombre')}\n"
            writer.write(jg_list.encode())
            await writer.drain()

            writer.write("ID JUEGO: ".encode())
            await writer.drain()
            id_juego = (await reader.read(1024)).decode().strip()
            try:
                id_juego = int(id_juego)
            except ValueError:
                writer.write("ID de juego inválido. Cancelando.\n".encode())
                await writer.drain()
                continue

            # --- Menú de campos opcionales ---
            opciones = (
                "Indica campos extra:\n"
                "1. Arma, elemento y rareza\n"
                "2. Solo elemento\n"
                "3. Solo arma\n"
                "4. Ninguno (dejar en blanco)\n"

            )
            writer.write(opciones.encode())
            await writer.drain()
            opcion = (await reader.read(1024)).decode().strip()

            arma = None
            elemento = None
            rareza = None

            if opcion == "1":
                writer.write("TIPO DE ARMA: ".encode())
                await writer.drain()
                arma = (await reader.read(1024)).decode().strip().capitalize()

                writer.write("ELEMENTO: ".encode())
                await writer.drain()
                elemento = (await reader.read(1024)).decode().strip().capitalize()

                writer.write("RAREZA (puede ser: 'rango S', 'Rango A', '4', '5', etc): ".encode())
                await writer.drain()
                rareza = (await reader.read(1024)).decode().strip().title()
            elif opcion == "2":
                writer.write("ELEMENTO: ".encode())
                await writer.drain()
                elemento = (await reader.read(1024)).decode().strip().capitalize()
            elif opcion == "3":
                writer.write("TIPO DE ARMA: ".encode())
                await writer.drain()
                arma = (await reader.read(1024)).decode().strip().capitalize()
            # Si la opción es "4" o cualquier otra, se dejan los campos en None

            # --- Montar documento y guardar ---
            data = {
                "id": COL_P.count_documents({}) + 1,
                "nombre": nombre,
                "genero": genero,
                "elemento": elemento,
                "arma": arma,
                "rareza": rareza,
                "faccion": faccion,
                "id_juego": id_juego
            }
            try:
                COL_P.insert_one(data)
                writer.write("Personaje insertado correctamente en la colección.\\n".encode())
                await writer.drain()
                log_info(f"Insertado personaje: {data['nombre']} en MongoDB.")
            except Exception as e:
                writer.write(f"Error insertando personaje: {e}".encode())
                await writer.drain()
                log_error(f"Error insertando personaje: {e}")

        elif msg == "2":
            # Consultar todos los personajes
            all_chars = list(COL_P.find())
            if not all_chars:
                writer.write("No hay personajes en la colección.\n".encode())
            else:
                lista = "=== PERSONAJES ===\n"
                for char in all_chars:
                    lista += f"ID: {char.get('id','')} | Nombre: {char.get('nombre','')} | Rareza: {char.get('rareza','-')} | Juego: {char.get('id_juego','')}\n"
                writer.write(lista.encode())
            await writer.drain()

        elif msg == "3":
            writer.write("Funcionalidad no implementada aún.\n".encode())
            await writer.drain()

        elif msg == "4":
            writer.write("Saliendo del menú de personajes.\n".encode())
            await writer.drain()
            break

        else:
            writer.write("Opción no válida. Intenta de nuevo.\\n".encode())
            await writer.drain()




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