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
COLLECTION_MONGO_10 = "Turno"

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
TABLE_MySQL_10 = "Turno"


# TODO =============== CONEXIONES_MySQL ================

def get_MySQL_conn():
    return mysql.connector.connect(
        host = HOST_MySQL,
        user = USER_MySQL,
        password = PASSWORD_MySQL,
        database = DB_MySQL
    )





# TODO: =============== PETICIONES (TABLAS_COLECCIONES) ================

# TODO: =============== TELEOPERADOR (MySQL) ================
async def add_teleoperador(writer, reader):
    conn = get_MySQL_conn() # pilla la conexion a la base de datos
    crs = conn.cursor() # cursor para ejecutar las consultas

    while True:
        writer.write("Nombre del teleoperador".encode())
        await writer.drain()
        nombre = (await reader.read(1024)).decode().strip()
        log_info(f"Nombre recibido: {nombre}")

        writer.write("Apellido del teleoperador".encode())
        await writer.drain()
        apellido = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Apellido recibido: {apellido}")

        writer.write("Telefono del teleoperador".encode())
        await writer.drain()
        telefono = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Telefono recibido: {telefono}")

        writer.write("Email del teleoperador".encode())
        await writer.drain()
        email = (await reader.read(1024)).decode().strip()
        log_info(f"Email recibido: {email}")

        # MOSTRAR UBICACIONES DISPONIBLES
        crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_6}")
        ubicaciones = crs.fetchall()
        ub_list = "Selecciona una ubicación por su ID y nombre: \n"
        for ub in ubicaciones:
            ub_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
        writer.write(ub_list.encode())
        await writer.drain()

        writer.write("ID de la ubicación seleccionada".encode())
        await writer.drain()
        ub_id = (await reader.read(1024)).decode().strip()
        log_info(f"Ubicacion recibida: {ub_id}")

        try:
            ub_id = int(ub_id)  # Asegurarse de que el ID es un entero
        except ValueError:
            log_error("ID de ubicación no válido")
            writer.write("ID de ubicación no válido. Inténtalo de nuevo.\n".encode())
            await writer.drain()
            continue

        # INSERTAR TELEOPERADOR EN LA BASE DE DATOS
        values = (nombre, apellido, telefono, email, ub_id)
        query = f"INSERT INTO {TABLE_MySQL_8} (nombre, apellido, telefono, email, ubicacion_id) VALUES (%s, %s, %s, %s, %s)"
        crs.execute(query, values)
        conn.commit()  # Confirmar los cambios en la base de datos

        log_info(f"Teleoperador {nombre} {apellido} insertado correctamente en la base de datos.")
        writer.write(f"Teleoperador {nombre} {apellido} insertado correctamente.\n".encode())
        await writer.drain()
        Mysql_tele(writer, reader)  # Volver al menú de teleoperador



# TODO: =============== CONFIGURACION CONEXION BASES DE DATOS, SELECCION DE TABLAS ================

#TODO TELEOPERADOR
async def Mysql_tele(writer, reader):
    writer("Has seleccionado la opción de TELEOPERADOR con MySQL. Selecciona la consulta que quieras hacer: "\
        "\n"\
        "1. Insertar un nuevo teleoperador \n"\
        "2. Actualizar un teleoperador existente \n"\
        "3. Eliminar un teleoperador \n"\
        "4. Consultar teleoperadores y sus horarios \n".encode())
    await writer.drain()
    data = await reader.readline()
    message = data.decode().strip()
    log_debug(f"Mensaje recibido: {message}")
    if message == "1":
        await add_teleoperador(writer, reader)
    elif message == "2":
        # await update_teleoperador(writer, reader)
        pass
    elif message == "3":
        # await delete_teleoperador(writer, reader)
        pass
    elif message == "4":
        # await consult_teleoperadores(writer, reader)
        pass



async def MongoDB_tele(writer, reader):
    raise NotImplementedError



#TODO TECNICO
async def Mysql_tec(writer, reader):
    raise NotImplementedError

async def MongoDB_tec(writer, reader):
    raise NotImplementedError

































# TODO: =============== SERVIDOR ================

async def server(reader, writer):
    addr = writer.get_extra_info('peername')
    log_info(f"Conexión establecida desde {addr}")
    print(f"Conexión establecida desde {addr}")
    writer.write("CONECTADO CORRECTAMENTE AL SERVIDOR. \n ENTER PARA SEGUIR".encode())
    await writer.drain()

    while True:
        await asyncio.sleep(5)
        log_warning("== ESPERA AUTOMÁTICA DE 5 SEGUNDOS ==")
        writer.write("ELIGE LA OPCION DESEADA: \n 1. TELEOPERADOR \n 2. TECNICO \n 3. SALIR \n".encode())
        await writer.drain()
        message = (await reader.readline()).decode().strip()
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
                    await Mysql_tele(writer, reader)
                elif message == "2": # MongoDB
                    log_info("Seleccionado: Opción 2")
                    writer.write("Has seleccionado la opción 2. \n".encode())
                    await writer.drain()
                    await MongoDB_tele(writer, reader)
                else:
                    log_warning("Opción no válida seleccionada por TELEOPERADOR")
                    writer.write("OPCIÓN NO VÁLIDA. INTENTE DE NUEVO.\n".encode())
                    await writer.drain()
                
            else:
                log_error("Contraseña incorrecta para TELEOPERADOR")
                writer.write("CONTRASEÑA INCORRECTA. INTENTE DE NUEVO.\n".encode())
                await writer.drain()
        elif message == "2":
            log_info("Seleccionado: TECNICO")
            writer.write("TECNICO SELECCIONADO. \n ESCRIBA CONTRASEÑA: ".encode())
            await writer.drain()
            password = (await reader.readline()).decode().strip()
            log_debug(f"Contraseña recibida: {password}")

            if password == "Genio-tecnico._.2025":
                log_info("Contraseña correcta para TECNICO")
                writer.write("CONTRASEÑA CORRECTA. BIENVENIDO TECNICO.\n Escribe un numero: 1 o 2".encode())
                await writer.drain()
                data = await reader.readline()
                message = data.decode().strip()
                log_debug(f"Mensaje recibido: {message}")
                if message == "1": # MySQL
                    log_info("Seleccionado: Opción 1")
                    writer.write("Has seleccionado la opción 1. \n".encode())
                    await writer.drain()
                    await Mysql_tec(writer, reader)
                elif message == "2": # MongoDB
                    log_info("Seleccionado: Opción 2")
                    writer.write("Has seleccionado la opción 2. \n".encode())
                    await writer.drain()
                    await MongoDB_tec(writer, reader)
                else:
                    log_warning("Opción no válida seleccionada por TECNICO")
                    writer.write("OPCIÓN NO VÁLIDA. INTENTE DE NUEVO.\n".encode())
                    await writer.drain()
                
            else:
                log_error("Contraseña incorrecta para TECNICO")
                writer.write("CONTRASEÑA INCORRECTA. INTENTE DE NUEVO.\n".encode())
                await writer.drain()


async def main():
    try:
        s = await asyncio.start_server(
            server, Shost, Sport
        )
        log_info(f"Servidor escuchando en {Shost}:{Sport}")
        print(f"Servidor escuchando en {Shost}:{Sport}")
        async with s:
            await s.serve_forever()
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