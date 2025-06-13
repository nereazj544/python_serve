import asyncio
import aiomysql
from Logs import log_critical, log_info, log_error, log_warning, log_debug
from aiomysql import create_pool

Shost = 'localhost'  # Dirección del servidor
Sport = 8083  # Puerto del servidor

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





async def animales_mysql(reader, writer):
    conn = await connect()
    cursor = await conn.cursor()

    log_info("Conexión establecida con la base de datos MySQL para Animales.")
    print("Conexión establecida con la base de datos MySQL para Animales.")
    writer.write("Conexión establecida con la base de datos MySQL para Animales.\n".encode())
    await writer.drain()

    while True:
        menu = ("1. Ver todos los animales\n"
        "2. Filtar animales por especie\n"
        "3. Insertar un nuevo animal\n"
        "4. Salir")
        writer.write(menu.encode())
        await writer.drain()
        data = await reader.read(1024)
        msg = data.decode().strip()
        log_debug(f"Opción seleccionada: {msg}")
        if msg == '1':
            log_info("Opción Ver todos los animales seleccionada.")
            writer.write("Has seleccionado la opción Ver todos los animales.\n".encode())
            await writer.drain()
            await cursor.execute("SELECT * FROM animales")
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    writer.write(f"\nID: {row[0]}, Nombre: {row[1]}, Especie: {row[2]}\n".encode())
            await writer.drain()
        elif msg == '2':
            log_info("Opción Filtrar animales por especie seleccionada.")
            print("Opción Filtrar animales por especie seleccionada.")
            writer.write("Has seleccionado la opción Filtrar animales por especie.\n".encode())
            await writer.drain()
            writer.write("Introduce la especie a filtrar: ".encode())
            await writer.drain()
            data = await reader.read(1024)
            especie = data.decode().strip()
            if not especie:
                log_warning("Especie no válida.")
                print("Especie no válida.")
                writer.write("Especie no válida.\n".encode())
                await writer.drain()
                continue
            log_debug(f"Especie a filtrar: {especie}")


            lista_especie = 'LISTA DE ANIMALES FILTRADOS POR ESPECIE:\n'
            await cursor.execute(f"select a.nombre, a.especie, rc.nombre, rc.id from animales a inner join numero_recinto nr on a.id = nr.animal_id inner join recintos rc on nr.recinto_id = rc.id where a.especie like '%{especie}%'")
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    lista_especie +=(f"Nombre: {row[0]} | Especie: {row[1]} | Recinto: {row[2]} | Numero recinto: {row[3]} \n")
                writer.write(lista_especie.encode())
            await writer.drain()
            await server_on(reader, writer)  # Volver al menú principal
        elif msg == '3':
            log_info("Opción Insertar un nuevo animal seleccionada.")
            print("Opción Insertar un nuevo animal seleccionada.")
            writer.write("Has seleccionado la opción Insertar un nuevo animal.\n".encode())
            await writer.drain()
            writer.write("Introduce el nombre del animal: ".encode())
            await writer.drain()
            data = await reader.read(1024)
            nombre = data.decode().strip()
            if not nombre:
                log_warning("Nombre no válido.")
                print("Nombre no válido.")
                writer.write("Nombre no válido.\n".encode())
                await writer.drain()
                continue
            log_debug(f"Nombre del animal: {nombre}")

            writer.write("Introduce la especie del animal: ".encode())
            await writer.drain()
            data = await reader.read(1024)
            especie = data.decode().strip()
            if not especie:
                log_warning("Especie no válida.")
                print("Especie no válida.")
                writer.write("Especie no válida.\n".encode())
                await writer.drain()
                continue
            log_debug(f"Especie del animal: {especie}")

            try:
                await cursor.execute("INSERT INTO animales (nombre, especie) VALUES (%s, %s)", (nombre, especie))
                await conn.commit()
                log_info(f"Animal {nombre} de especie {especie} insertado correctamente.")
                print(f"Animal {nombre} de especie {especie} insertado correctamente.")
                writer.write(f"Animal {nombre} de especie {especie} insertado correctamente.\n".encode())

                
            except Exception as e:
                log_error(f"Error al insertar el animal: {e}")
                print(f"Error al insertar el animal: {e}")
                writer.write(f"Error al insertar el animal: {e}\n".encode())
        
        
        elif msg == '4':
            log_info("Opción Salir seleccionada.")
            print("Opción Salir seleccionada.")
            writer.write("Saliendo del módulo de Animales...\n".encode())
            conn.close()
            await cursor.close()
            await writer.drain()
            break




async def recintos_mysql(reader, writer):
    log_info("Conexión establecida con la base de datos MySQL para Recintos.")
    print("Conexión establecida con la base de datos MySQL para Recintos.")
    writer.write("Conexión establecida con la base de datos MySQL para Recintos.\n".encode())
    await writer.drain()
    while True:
        menu = ("1. Ver todos los recintos\n"
        "2. Filtrar recintos por nombre\n"
        "3. salir")
        writer.write(menu.encode())
        await writer.drain()
        data = await reader.read(1024)
        msg = data.decode().strip()







async def cuidador_mysql(reader, writer):
    log_info("Conexión establecida con la base de datos MySQL para Cuidadores.")
    print("Conexión establecida con la base de datos MySQL para Cuidadores.")
    writer.write("Conexión establecida con la base de datos MySQL para Cuidadores.\n".encode())
    await writer.drain()





















































# TODO: ============== SERVIDOR ==============

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
        writer.write("ELIGE UNA OPCIÓN:\n" \
        "1. Animales\n" \
        "2. Recintos\n" \
        "3. Cuidador\n" \
        "4. Salir".encode())
        await writer.drain()
        msg = await reader.read(1024)
        if not msg:
            log_warning("Cliente desconectado.")
            print("Cliente desconectado.")
            break
        option = msg.decode().strip()
        log_debug(f"Opción seleccionada: {option}")
        print(f"Opción seleccionada: {option}")
        
        if option == '1':
            log_info("Opción Teleoperador seleccionada.")
            writer.write("Has seleccionado la opción Animales.\n".encode())
            await writer.drain()
            await animales_mysql(reader, writer)
        elif option == '2':
            log_info("Opción Recintos seleccionada.")
            writer.write("Has seleccionado la opción Recintos.\n".encode())
            await writer.drain()
            await recintos_mysql(reader, writer)
        elif option == '3':
            log_info("Opción Cuidador seleccionada.")
            writer.write("Has seleccionado la opción Cuidador.\n".encode())
            await writer.drain()
            await cuidador_mysql(reader, writer)
        elif option == '4':
            log_info("Opción Salir seleccionada.")
            writer.write("Saliendo del servidor...\n".encode())
            await writer.drain()
            log_critical("Servidor cerrado por el usuario.")
            print("Servidor cerrado por el usuario.")
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

