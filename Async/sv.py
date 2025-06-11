import asyncio
from Logs import log_critical, log_debug, log_error, log_info, log_warning

import mysql.connector 

Shost = "localhost"
Sport = 8083


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
        host="localhost",
        user="server_python",
        password="321_ytrewq",
        database="pithon"
    )



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
        await teleoperador_MySQL(writer, reader)  # Volver al menú de teleoperador





async def teleoperador_MySQL(writer: asyncio.StreamWriter, reader: asyncio.StreamReader):
        menu = ("Has seleccionado la opción de TELEOPERADOR con MySQL. Selecciona la consulta que quieras hacer: "\
        "\n"\
        "1. Insertar un nuevo teleoperador \n"\
        "2. Actualizar un teleoperador existente \n"\
        "3. Eliminar un teleoperador \n"\
        "4. Consultar teleoperadores y sus horarios \n")
        writer.write(menu.encode())
        await writer.drain()
        
        message = (await reader.read(1024)).decode().strip()
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
























async def server_on(reader, writer):  
    addr = writer.get_extra_info('peername')
    log_info(f"Conexión desde {addr}")
    print(f"Conexión desde {addr}")
    writer.write("CONEXIÓN ESTABLECIDA CORRECTAMENTE CON EL SERVIDOR.\n ENTER PARA CONTINUAR".encode())
    await writer.drain()

    while True:
        await asyncio.sleep(5)
        log_warning("== ESPERA AUTOMÁTICA DE 5 SEGUNDOS ==")
        await writer.drain()
        writer.write("ELIGE UNA OPCIÓN:\n1. Teleoperador\n2. Tecnico\n4. Salir".encode())
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
            log_info("Consultando datos de teleoperador...")
            writer.write("Consultando datos de teleoperador...\n".encode())
            await writer.drain()
            await teleoperador_MySQL(writer, reader)

        elif option == "2":
            log_info("Consultando datos de Tecnicos...")
            writer.write("Consultando datos de Tecnicos...\n".encode())
            await writer.drain()
            await tecnico_MySQL(writer, reader)
        elif option == "4":
            log_info("Cerrando conexión con el cliente.")
            writer.write("Cerrando conexión con el cliente.\n".encode())
            await writer.drain()
            break
        else:
            log_warning("Opción no válida, por favor intente nuevamente.")
            writer.write("Opción no válida, por favor intente nuevamente.\n".encode())
        await writer.drain()









async def main ():
    try:
            server = await asyncio.start_server(
            server_on, Shost, Sport
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