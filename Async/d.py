import asyncio
from Logs import log_critical, log_debug, log_error, log_info, log_warning
import mysql.connector

# Configuración servidor
Shost = "localhost"
Sport = 8083

# Configuración MySQL
DB_MySQL = "pithon"
USER_MySQL = "server_python"
PASSWORD_MySQL = "321_ytrewq"
HOST_MySQL = "localhost"
TABLE_MySQL_6 = "Ubicacion"
TABLE_MySQL_8 = "Teleoperador"

def get_MySQL_conn():
    return mysql.connector.connect(
        host=HOST_MySQL,
        user=USER_MySQL,
        password=PASSWORD_MySQL,
        database=DB_MySQL
    )

# --- TELEOPERADOR (acciones) ---
async def add_teleoperador(writer, reader):
    conn = get_MySQL_conn()
    crs = conn.cursor()

    # Pedimos datos
    writer.write("Nombre del teleoperador: ".encode())
    await writer.drain()
    nombre = (await reader.read(1024)).decode().strip()

    writer.write("Apellido del teleoperador: ".encode())
    await writer.drain()
    apellido = (await reader.read(1024)).decode().strip().capitalize()

    writer.write("Teléfono del teleoperador: ".encode())
    await writer.drain()
    telefono = (await reader.read(1024)).decode().strip()

    writer.write("Email del teleoperador: ".encode())
    await writer.drain()
    email = (await reader.read(1024)).decode().strip()

    # Mostrar ubicaciones disponibles
    crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_6}")
    ubicaciones = crs.fetchall()
    ub_list = "Selecciona una ubicación por su ID:\\n"
    for ub in ubicaciones:
        ub_list += f"ID: {ub[0]}, Nombre: {ub[1]}\\n"
    writer.write(ub_list.encode())
    await writer.drain()

    writer.write("ID de la ubicación seleccionada: ".encode())
    await writer.drain()
    ub_id = (await reader.read(1024)).decode().strip()

    try:
        ub_id = int(ub_id)
    except ValueError:
        log_error("ID de ubicación no válido")
        writer.write("ID de ubicación no válido. Inténtalo de nuevo.\\n".encode())
        await writer.drain()
        crs.close()
        conn.close()
        return

    # Insertar teleoperador
    try:
        values = (nombre, apellido, telefono, email, ub_id)
        query = f"INSERT INTO {TABLE_MySQL_8} (nombre, apellido, telefono, email, ubicacion_id) VALUES (%s, %s, %s, %s, %s)"
        crs.execute(query, values)
        conn.commit()
        log_info(f"Teleoperador {nombre} {apellido} insertado correctamente en la base de datos.")
        writer.write(f"Teleoperador {nombre} {apellido} insertado correctamente.\\n".encode())
    except Exception as e:
        log_error(f"Error al insertar teleoperador: {e}")
        writer.write(f"Error al insertar teleoperador: {e}\\n".encode())

    await writer.drain()
    crs.close()
    conn.close()


async def Mysql_tele(writer, reader):
    while True:
        writer.write((
            "Has seleccionado la opción de TELEOPERADOR con MySQL. Selecciona la consulta que quieras hacer:\\n"
            "1. Insertar un nuevo teleoperador\\n"
            "2. Actualizar un teleoperador existente\\n"
            "3. Eliminar un teleoperador\\n"
            "4. Consultar teleoperadores y sus horarios\\n"
            "5. Volver al menú anterior\\n"
        ).encode())
        await writer.drain()
        data = await reader.readline()
        message = data.decode().strip()
        log_debug(f"Mensaje recibido: {message}")

        if message == "1":
            await add_teleoperador(writer, reader)
        elif message == "2":
            writer.write("Función no implementada.\\n".encode())
            await writer.drain()
        elif message == "3":
            writer.write("Función no implementada.\\n".encode())
            await writer.drain()
        elif message == "4":
            writer.write("Función no implementada.\\n".encode())
            await writer.drain()
        elif message == "5":
            break
        else:
            writer.write("OPCIÓN NO VÁLIDA. INTENTE DE NUEVO.\\n".encode())
            await writer.drain()


# --- MENÚ PRINCIPAL: SERVER ---
async def server(reader, writer):
    addr = writer.get_extra_info('peername')
    log_info(f"Conexión establecida desde {addr}")
    print(f"Conexión establecida desde {addr}")
    writer.write("CONECTADO CORRECTAMENTE AL SERVIDOR. \\nENTER PARA SEGUIR\\n".encode())
    await writer.drain()

    while True:
        
        writer.write(
            "ELIGE LA OPCION DESEADA:\\n1. TELEOPERADOR\\n2. TECNICO\\n3. SALIR\\n".encode())
        await writer.drain()
        message = (await reader.readline()).decode().strip()
        log_debug(f"Mensaje recibido: {message}")
        print(f"Mensaje recibido: {message}")

        if message == "1":
            log_info("Seleccionado: TELEOPERADOR")
            writer.write("TELEOPERADOR SELECCIONADO.\\nESCRIBA CONTRASEÑA: ".encode())
            await writer.drain()
            password = (await reader.readline()).decode().strip()
            log_debug(f"Contraseña recibida: {password}")

            if password == "leo-perador._.2025":
                log_info("Contraseña correcta para TELEOPERADOR")
                writer.write("CONTRASEÑA CORRECTA. BIENVENIDO TELEOPERADOR.\\nEscribe un numero: 1 (MySQL, habilitado) o 2 (MongoDB, no implementado)\\n".encode())
                await writer.drain()

                message = (await reader.readline()).decode().strip()
                log_debug(f"Mensaje recibido: {message}")

                if message == "1":
                    log_info("Seleccionado: Opción 1 (MySQL)")
                    writer.write("Has seleccionado la opción 1. \\n".encode())
                    await writer.drain()
                    await Mysql_tele(writer, reader)
                elif message == "2":
                    writer.write("Opción MongoDB todavía no implementada.\\n".encode())
                    await writer.drain()
                else:
                    writer.write("OPCIÓN NO VÁLIDA. INTENTE DE NUEVO.\\n".encode())
                    await writer.drain()
            else:
                log_error("Contraseña incorrecta para TELEOPERADOR")
                writer.write("CONTRASEÑA INCORRECTA. INTENTE DE NUEVO.\\n".encode())
                await writer.drain()

        elif message == "2":
            writer.write("Funcionalidad TECNICO no implementada aún.\\n".encode())
            await writer.drain()
        elif message == "3":
            log_info("Cliente ha salido del menú. Cerrando conexión.")
            writer.write("¡Hasta luego!\\n".encode())
            await writer.drain()
            break
        else:
            writer.write("Opción no válida. Intente de nuevo.\\n".encode())
            await writer.drain()

    writer.close()
    await writer.wait_closed()
    print(f"Conexión cerrada con {addr}")

async def main():
    try:
        s = await asyncio.start_server(server, Shost, Sport)
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
