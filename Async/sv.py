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


#TODO: =============== INCIDENCIAS (MySQL) ================

async def update_terminales_estado(writer, reader):
    conn = get_MySQL_conn()
    crs = conn.cursor()
    while True:
        crs.execute("SELECT * FROM terminal")
        await writer.drain()
        terminales = crs.fetchall()
        for ter in terminales:
            response = f"ID: {ter[0]} | Nombre: {ter[1]} | Estado: {ter[2]} | Ubicación ID: {ter[3]}\n"
            writer.write(response.encode())
            await writer.drain()
        menu=("¿Quieres actualizar el estado de alguna terminal? (s/n)")
        writer.write(menu.encode())
        await writer.drain()

        respuesta = (await reader.read(1024)).decode().strip().lower()
        log_info(f"Respuesta recibida: {respuesta}")

        if respuesta == "s":
            writer.write("Selecciona el ID de la terminal que quieres actualizar: ".encode())
            await writer.drain()
            terminal_id = (await reader.read(1024)).decode().strip()
            log_info(f"ID de terminal recibido: {terminal_id}")

            # Pedir el nuevo estado
            writer.write("Introduce el nuevo estado de la terminal: ".encode())
            await writer.drain()
            nuevo_estado = (await reader.read(1024)).decode().strip()
            log_info(f"Nuevo estado recibido: {nuevo_estado}")

            # UPDATE terminal
            crs.execute(
                f"UPDATE {TABLE_MySQL_1} SET estado = %s WHERE id = %s",
                (nuevo_estado, terminal_id)
            )
            conn.commit()

            writer.write(f"Estado de la terminal {terminal_id} actualizado correctamente.\n".encode())
            await writer.drain()
            add_incidencia(writer, reader)
        else:
            writer.write("No se ha actualizado ninguna terminal.\n".encode())
            await writer.drain()
            await incidencias_MySQL(writer, reader)  # Volver al menú de incidencias



async def update_incidencia(writer, reader):
    conn = get_MySQL_conn()
    crs = conn.cursor()

    # Mostrar incidencias pendientes
    while True:
        crs.execute(
            "SELECT i.id, ter.nombre, ter.estado, u.nombre, z.nombre, i.fecha_reportada, i.descripcion, tec.nombre "
            "FROM terminal ter "
            "INNER JOIN ubicacion u ON ter.ubicacion_id = u.id INNER JOIN zona z ON z.id = u.zona_id INNER JOIN incidencia i ON i.terminal_id = ter.id INNER JOIN tecnico tec ON i.tecnico_id = tec.id "
            f"WHERE (ter.estado LIKE '%averiado%' or ter.estado LIKE '%en reparación%') AND i.fecha_solucion IS NULL AND i.solucionada IS FALSE"
        )
        await writer.drain()
        incidencias = crs.fetchall()

        if not incidencias:
            writer.write("No hay incidencias pendientes de actualización.\n".encode())
            await writer.drain()
            return

        response = "Incidencias pendientes de actualización:\n"
        for row in incidencias:
            response += (
                f"ID: {row[0]} | Nombre Terminal: {row[1]} | Estado Terminal: {row[2]} | Ubicación: {row[3]} | "
                f"Zona: {row[4]} | Fecha Reportada: {row[5]} | Descripción: {row[6]} | Técnico: {row[7]}\n"
            )
        writer.write(response.encode())
        await writer.drain()

        writer.write("Selecciona el ID de la incidencia que quieres actualizar: ".encode())
        await writer.drain()
        incidencia_id = (await reader.read(1024)).decode().strip()
        log_info(f"ID de incidencia recibido: {incidencia_id}")

        # Pedir el nuevo estado solucionada
        writer.write("¿La incidencia está solucionada? (si/no): ".encode())
        await writer.drain()
        solucionada_input = (await reader.read(1024)).decode().strip().lower()
        solucionada = 1 if solucionada_input == "s" else 0

        # Fecha de solución si está solucionada
        fecha_solucion = None
        if solucionada:
            writer.write("Introduce la fecha de solución (YYYY-MM-DD HH:MM:SS): ".encode())
            await writer.drain()
            fecha_solucion = (await reader.read(1024)).decode().strip()
            log_info(f"Fecha de solución recibida: {fecha_solucion}")

            # UPDATE incidencia
            crs.execute(
                f"UPDATE {TABLE_MySQL_2} SET solucionada = %s, fecha_solucion = %s WHERE id = %s and UPPER(terminal_id) IN (SELECT UPPER(id) FROM terminal WHERE estado = 'Operativo')",
                (solucionada, fecha_solucion, incidencia_id)
            )

            conn.commit()

        writer.write(f"Incidencia {incidencia_id} actualizada correctamente.\\n".encode())
        await writer.drain()
        # Salimos del bucle tras una actualización
        break

    await incidencias_MySQL(writer, reader)




async def add_incidencia(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos

    with conn.cursor() as crs, conn.cursor() as insertar, conn.cursor() as crs_2:
        while True:
            crs.execute(f"SELECT ter.id, ter.nombre, ter.estado, i.descripcion, i.fecha_reportada, tec.nombre  FROM terminal ter LEFT JOIN incidencia i ON i.terminal_id = ter.id LEFT JOIN tecnico tec ON tec.id = i.tecnico_id WHERE ter.estado = 'Operativo' OR i.id IS NOT NULL ORDER BY ter.nombre;")

            terminales = crs.fetchall()
            ter_list = "Selecciona un terminal por su ID: \n"
            for ter in terminales:
                ter_list += f"ID TERMINAL: {ter[0]} | NOMBRE TERMINAL: {ter[1]} | ESTADO: {ter[2]} | DESCRIPCIÓN: {ter[3]} | FECHA REPORTADA: {ter[4]} | TÉCNICO ASIGNADO: {ter[5]}\n"
            writer.write(ter_list.encode())
            await writer.drain()

            crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_3}")
            ubicaciones = crs.fetchall()
            tele_list = "Selecciona un ID del tecnico: \n"
        
            for ub in ubicaciones:
                tele_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
            writer.write(tele_list.encode())
            await writer.drain()

            writer.write("El ID del tecnico que quiere añadir".encode())
            await writer.drain()
            tecnico_id = (await reader.read(1024)).decode().strip()
            log_info(f"Tecnico recibido: {tecnico_id}")

            crs_2.execute(f"select * from  ubicacion u inner join terminal tr on u.id = tr.ubicacion_id where tr.estado like '%averiado%'")
            ubicaciones = crs_2.fetchall()
            terminal_list = "Selecciona un ID del terminal: \n"

            for ub in ubicaciones:
                terminal_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
            writer.write(terminal_list.encode())
            await writer.drain()

            writer.write("El ID del terminal que quiere añadir".encode())
            await writer.drain()
            terminal_id = (await reader.read(1024)).decode().strip()
            log_info(f"Terminal recibido: {terminal_id}")

            writer.write("Descripción de la incidencia".encode())
            await writer.drain()
            descripcion = (await reader.read(1024)).decode().strip()
            log_info(f"Descripción recibida: {descripcion}")

            writer.write("Fecha y hora de la incidencia (formato: YYYY-MM-DD HH:MM:SS)".encode())
            await writer.drain()
            fecha_hora = (await reader.read(1024)).decode().strip()
            log_info(f"Fecha y hora recibida: {fecha_hora}")

            # INSERTAR INCIDENCIA EN LA BASE DE DATOS
            values = (terminal_id, descripcion, fecha_hora, False, None, tecnico_id)
            query = f"INSERT INTO {TABLE_MySQL_2} (terminal_id, descripcion, fecha_reportada, solucionada, fecha_solucion, tecnico_id) VALUES (%s, %s, %s, %s, %s, %s)"
            insertar.execute(query, values)
            conn.commit()  # Confirmar los cambios en la base de datos
            log_info(f"Incidencia para tecnico {tecnico_id} y terminal {terminal_id} insertada correctamente en la base de datos.")
            writer.write(f"Incidencia para tecnico {tecnico_id} y terminal {terminal_id} insertada correctamente.\n".encode())
            await writer.drain()
            await incidencias_MySQL(writer, reader)  # Volver al menú de incidencias


#TODO: IMPLEMENTAR AÑADIR INCIDENCIA    

async def consult_incidencias(writer, reader):
    conn = get_MySQL_conn()
    crs = conn.cursor()

    crs.execute(f"select ter.nombre , ter.estado, u.nombre, z.nombre, i.fecha_reportada, i.descripcion, tec.nombre from terminal ter inner join ubicacion u on ter.ubicacion_id = u.id inner join zona z on z.id = u.zona_id inner join incidencia i on i.terminal_id = ter.id inner join tecnico tec on i.tecnico_id = tec.id where ter.estado like '%averiado%' and i.fecha_solucion is NULL and i.solucionada is false")

    await writer.drain()
    incidencias = crs.fetchall()
    for inc in incidencias:
        response = (
            f"Nombre Terminal: {inc[0]} | Estado Terminal: {inc[1]} | Ubicación: {inc[2]} | "
            f"Zona: {inc[3]} | Fecha Reportada: {inc[4]} | Descripción: {inc[5]} | Técnico: {inc[6]}\n"
        )
        writer.write(response.encode())
        await writer.drain()
    if not incidencias:
        writer.write("No hay incidencias pendientes de actualización.\n".encode())
        await writer.drain()
        return
    await incidencias_MySQL(writer, reader)  # Volver al menú de incidencias


async def incidencias_MySQL(writer, reader):
    menu = ("Has seleccionado la opción de INCIDENCIAS con MySQL. Selecciona la consulta que quieras hacer: "\
    "\n"\
    "1. Consultar incidencias \n"\
    "2. Añadir incidencia \n"\
    "3. Actualizar incidencia \n"\
    "4. Actualizar estado de terminales \n"\
        "")
    writer.write(menu.encode())
    await writer.drain()
    
    message = (await reader.read(1024)).decode().strip()
    log_debug(f"Mensaje recibido: {message}")
    if message == "1":
        await consult_incidencias(writer, reader)
    elif message == "2":
        await add_incidencia(writer, reader)
    elif message == "3":
        await update_incidencia(writer, reader)
    elif message == "4":
        await update_terminales_estado(writer, reader)



#TODO: =============== TECNICO (MySQL) ================

async def add_horario_tecnico(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos
    crs = conn.cursor()  # cursor para ejecutar las consultas
    while True:
        crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_3}")
        ubicaciones = crs.fetchall()
        tele_list = "Selecciona un ID del tecnico: \n"
        
        for ub in ubicaciones:
            tele_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
        writer.write(tele_list.encode())
        await writer.drain()

        writer.write("El ID del tecnico que quiere añadir".encode())
        await writer.drain()
        tecnico_id = (await reader.read(1024)).decode().strip()
        log_info(f"Tecnico recibido: {tecnico_id}")

        writer.write("Semana del horario".encode())
        await writer.drain()
        semana = (await reader.read(1024)).decode().strip()
        log_info(f"Semana recibida: {semana}")

        writer.write("Hora de inicio".encode())
        await writer.drain()
        hora_inicio = (await reader.read(1024)).decode().strip()
        log_info(f"Hora de inicio recibida: {hora_inicio}")

        writer.write("Hora de fin".encode())
        await writer.drain()
        hora_fin = (await reader.read(1024)).decode().strip()
        log_info(f"Hora de fin recibida: {hora_fin}")

        writer.write("Descripción del turno".encode())
        await writer.drain()
        descripcion = (await reader.read(1024)).decode().strip()
        log_info(f"Descripción recibida: {descripcion}")

        # INSERTAR HORARIO EN LA BASE DE DATOS
        teleoperador_id = None  # Asignar None si no se usa teleoperador_id
        values = (tecnico_id, semana, hora_inicio, hora_fin, descripcion, teleoperador_id)
        query = f"INSERT INTO {TABLE_MySQL_10} (tecnico_id, semana, hora_inicio, hora_fin, descripcion, teleoperador_id) VALUES (%s, %s, %s, %s, %s, %s)"
        crs.execute(query, values)
        conn.commit()  # Confirmar los cambios en la base de datos
        log_info(f"Horario para tecnico {tecnico_id} insertado correctamente en la base de datos.")
        writer.write(f"Horario para tecnico {tecnico_id} insertado correctamente.\n".encode())
        await writer.drain()
        await tecnico_MySQL(writer, reader)  # Volver al menú de tecnico

        

async def consult_tecnicos_incidencias(writer, reader):
    conn = get_MySQL_conn()
    crs = conn.cursor()
    query = (
        "SELECT t.id, t.nombre, t.apellido, COUNT(i.id) as total_incidencias "
        f"FROM {TABLE_MySQL_3} t "
        f"LEFT JOIN {TABLE_MySQL_2} i ON t.id = i.tecnico_id "
        "GROUP BY t.id, t.nombre, t.apellido "
        "ORDER BY t.id"
    )
    crs.execute(query)
    tecnicos = crs.fetchall()
    if not tecnicos:
        writer.write("No hay técnicos con incidencias registradas.\\n".encode())
        await writer.drain()
        return
    response = "Listado de técnicos y nº de incidencias asignadas:\\n"
    for row in tecnicos:
        response += f"ID: {row[0]} | Nombre: {row[1]} {row[2]} | Incidencias: {row[3]}\\n"
    writer.write(response.encode())
    await writer.drain()
    # Vuelve al menú principal de técnicos
    await tecnico_MySQL(writer, reader)




async def consult_tecnicos_horarios(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos
    crs = conn.cursor()  # cursor para ejecutar las consultas
    while True:
        writer.write("Consultando tecnicos y sus horarios...\n".encode())
        await writer.drain()
        # CONSULTAR TECNICOS Y SUS HORARIOS
        query = ( "SELECT te.id, te.nombre, te.apellido, te.telefono, z.nombre AS zona, h.semana, h.hora_inicio, h.hora_fin, h.descripcion FROM tecnico te JOIN tecnico_zona tz ON te.id = tz.tecnico_id JOIN zona z ON tz.zona_id = z.id LEFT JOIN turno h ON te.id = h.tecnico_id" )
        crs.execute(query)
        results = crs.fetchall()
        if not results:
            writer.write("No hay tecnicos registrados.\n".encode())
            await writer.drain()
            continue
        response = "Tecnicos y sus horarios:\n"
        for row in results:
            response += f"ID: {row[0]} | Nombre: {row[1]} {row[2]} | Teléfono: {row[3]} |  "\
                        f"Ubicación: {row[4]} | Semana: {row[5]} | Inicio: {row[6]} | Fin: {row[7]} | Descripción: {row[8]}\n"
        writer.write(response.encode())
        await writer.drain()
        
        

        await asyncio.sleep(5)  # Espera de 5 segundos antes de volver al menú
        log_warning("== ESPERA AUTOMÁTICA DE 5 SEGUNDOS ==")
        await tecnico_MySQL(writer, reader)  # Volver al menú de tecnico

async def delete_tecnico(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos
    crs = conn.cursor()  # cursor para ejecutar las consultas
    while True:
        crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_3}")
        ubicaciones = crs.fetchall()
        tele_list = "Selecciona un tecnico por su ID: \n"
        
        for ub in ubicaciones:
            tele_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
        writer.write(tele_list.encode())
        await writer.drain()

        writer.write("El ID del tecnico que quiere borrar".encode())
        await writer.drain()
        tele_id = (await reader.read(1024)).decode().strip()
        log_info(f"Tecnico recibido: {tele_id}")

        try:
            tele_id = int(tele_id)  # Asegurarse de que el ID es un entero
        except ValueError:
            log_error("ID de tecnico no válido")
            writer.write("ID de tecnico no válido. Inténtalo de nuevo.\n".encode())
            await writer.drain()
            continue

        # ELIMINAR TECNICO DE LA BASE DE DATOS
        query = f"DELETE FROM {TABLE_MySQL_3} WHERE id = %s"
        crs.execute(query, (tele_id,))
        conn.commit()
        log_info(f"Tecnico con ID {tele_id} eliminado correctamente de la base de datos.")
        await tecnico_MySQL(writer, reader)  # Volver al menú de tecnico

async def add_tecnico(writer, reader):
    conn = get_MySQL_conn() # pilla la conexion a la base de datos
    crs = conn.cursor() # cursor para ejecutar las consultas
    while True:
        writer.write("Nombre del tecnico".encode())
        await writer.drain()
        nombre = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Nombre recibido: {nombre}")

        writer.write("Apellido del tecnico".encode())
        await writer.drain()
        apellido = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Apellido recibido: {apellido}")

        writer.write("Telefono del tecnico".encode())
        await writer.drain()
        telefono = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Telefono recibido: {telefono}")

        writer.write("Email del tecnico".encode())
        await writer.drain()
        email = (await reader.read(1024)).decode().strip()
        log_info(f"Email recibido: {email}")


        # INSERTAR TECNICO EN LA BASE DE DATOS
        values = (nombre, apellido, telefono, email)
        query = f"INSERT INTO {TABLE_MySQL_3} (nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s)"
        crs.execute(query, values)
        conn.commit()  # Confirmar los cambios en la base de datos

        log_info(f"Tecnico {nombre} {apellido} insertado correctamente en la base de datos.")
        writer.write(f"Tecnico {nombre} {apellido} insertado correctamente.\n".encode())
        await writer.drain()
        writer.write("¿Desea añadir una zona al tecnico? (s/n)".encode())
        await writer.drain()
        respuesta = (await reader.read(1024)).decode().strip().lower()
        log_info(f"Respuesta recibida: {respuesta}")

        if respuesta == "si":
            log_info("Añadiendo zona al tecnico...")
            writer.write("Selecciona una zona por su ID: \n".encode())
            await writer.drain()
            crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_5}")
            zonas = crs.fetchall()
            zona_list = ""
            
            for zona in zonas:
                zona_list += f"ID: {zona[0]}, Nombre: {zona[1]}\n"
            writer.write(zona_list.encode())
            await writer.drain()
            writer.write("El ID de la zona que quiere añadir".encode())
            await writer.drain()
            
            zona_id = (await reader.read(1024)).decode().strip()
            log_info(f"Zona recibida: {zona_id}")
            
            writer.write("Selecciona un tencico por su ID: \n".encode())


        else:
            writer.write("No se ha añadido ninguna zona al tecnico.\n".encode())
            await writer.drain()
            await tecnico_MySQL(writer, reader)  # Volver al menú de tecnico



        await tecnico_MySQL(writer, reader)  # Volver al menú de tecnico



async def tecnico_MySQL(writer, reader):
    menu = ("Has seleccionado la opción de TECNICO con MySQL. Selecciona la consulta que quieras hacer: "\
    "\n"\
    "1. Insertar un nuevo técnico \n"\
    "2. Consultar técnicos y sus horarios \n"\
    "3. Eliminar un técnico \n"\
    "4. Consultar técnicos y sus incidencias" \
    "5. Insertar un nuevo horario de técnico \n"\
    )
    writer.write(menu.encode())
    await writer.drain()
    
    message = (await reader.read(1024)).decode().strip()
    log_debug(f"Mensaje recibido: {message}")
    if message == "1":
        await add_tecnico(writer, reader)
    elif message == "2":
        await consult_tecnicos_horarios(writer, reader)
    elif message == "3":
        await delete_tecnico(writer, reader)
    elif message == "4":
        await consult_tecnicos_incidencias(writer, reader)
    elif message == "5":
        await add_horario_tecnico(writer, reader)




# TODO: =============== TELEOPERADOR (MySQL) ================

async def consult_teleoperadores(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos
    crs = conn.cursor()  # cursor para ejecutar las consultas
    while True:
        writer.write("Consultando teleoperadores y sus horarios...\n".encode())
        await writer.drain()

        # CONSULTAR TELEOPERADORES Y SUS HORARIOS
        query = f"""
        SELECT t.id, t.nombre, t.apellido, t.telefono, t.email, u.nombre AS ubicacion, h.semana, h.hora_inicio, h.hora_fin, h.descripcion
        FROM {TABLE_MySQL_8} AS t
        JOIN {TABLE_MySQL_6} AS u ON t.ubicacion_id = u.id
        LEFT JOIN {TABLE_MySQL_10} AS h ON t.id = h.teleoperador_id
        """
        crs.execute(query)
        results = crs.fetchall()

        if not results:
            writer.write("No hay teleoperadores registrados.\n".encode())
            await writer.drain()
            continue

        response = "Teleoperadores y sus horarios:\n"
        for row in results:
            response += f"ID: {row[0]}, Nombre: {row[1]} {row[2]}, Teléfono: {row[3]}, Email: {row[4]}, "\
                        f"Ubicación: {row[5]}, Semana: {row[6]}, Inicio: {row[7]}, Fin: {row[8]}, Descripción: {row[9]}\n"
        
        writer.write(response.encode())
        await writer.drain()
        
        writer.write("Presiona ENTER para continuar.".encode())
        await writer.drain()
        await teleoperador_MySQL(writer, reader)  # Volver al menú de teleoperador
        

async def delete_teleoperador(writer, reader):
    conn = get_MySQL_conn()  # pilla la conexion a la base de datos
    crs = conn.cursor()  # cursor para ejecutar las consultas
    while True:
        crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_8}")
        ubicaciones = crs.fetchall()
        tele_list = "Selecciona un teleoperador por su ID: \n"
        
        for ub in ubicaciones:
            tele_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
        writer.write(tele_list.encode())
        await writer.drain()

        writer.write("El ID del teleoperador que quiere borrar".encode())
        await writer.drain()
        tele_id = (await reader.read(1024)).decode().strip()
        log_info(f"Teleoperador recibido: {tele_id}")

        try:
            tele_id = int(tele_id)  # Asegurarse de que el ID es un entero
        except ValueError:
            log_error("ID de teleoperador no válido")
            writer.write("ID de teleoperador no válido. Inténtalo de nuevo.\n".encode())
            await writer.drain()
            continue

        # ELIMINAR TELEOPERADOR DE LA BASE DE DATOS
        query = f"DELETE FROM {TABLE_MySQL_8} WHERE id = %s"
        crs.execute(query, (tele_id,))
        conn.commit()
        log_info(f"Teleoperador con ID {tele_id} eliminado correctamente de la base de datos.")


async def add_horario_teleoperador(writer, reader):
    conn = get_MySQL_conn() # pilla la conexion a la base de datos
    crs = conn.cursor() # cursor para ejecutar las consultas
    while True:
        crs.execute(f"SELECT id, nombre FROM {TABLE_MySQL_8}")
        ubicaciones = crs.fetchall()
        tele_list = "Selecciona una ubicación por su ID y nombre: \n"
        
        for ub in ubicaciones:
            tele_list += f"ID: {ub[0]}, Nombre: {ub[1]}\n"
        writer.write(tele_list.encode())
        await writer.drain()

        writer.write("El ID del teleoperador que quiere añadir".encode())
        await writer.drain()
        tele_id = (await reader.read(1024)).decode().strip()
        log_info(f"Teleoperador recibido: {tele_id}")

        try:
            tele_id = int(tele_id)  # Asegurarse de que el ID es un entero
        except ValueError:
            log_error("ID de teleoperador no válido")
            writer.write("ID de teleoperador no válido. Inténtalo de nuevo.\n".encode())
            await writer.drain()
            continue
    
        writer.write("Introduce la semana del teleoperador (formato: Semana [numero] de [mes])".encode())
        await writer.drain()
        semana = (await reader.read(1024)).decode().strip().capitalize()
        log_info(f"Semana recibida: {semana}")


        writer.write("Introduce el horario de INICIO DE JORNADA del teleoperador (formato: HH:MM:SS)".encode())
        await writer.drain()
        inicio_jornada = (await reader.read(1024)).decode().strip()
        log_info(f"Inicio de jornada recibido: {inicio_jornada}")


        writer.write("Introduce el horario de FIN DE JORNADA del teleoperador (formato: HH:MM:SS)".encode())
        await writer.drain()
        fin_jornada = (await reader.read(1024)).decode().strip()
        log_info(f"Fin de jornada recibido: {fin_jornada}")

        writer.write("Introduce una descripción del horario del teleoperador".encode())
        await writer.drain()
        descripcion = (await reader.read(1024)).decode().strip()
        log_info(f"Descripción recibida: {descripcion}")
        

        # INSERTAR HORARIO DEL TELEOPERADOR EN LA BASE DE DATOS
        tecnico_id = None
        query = f"INSERT INTO {TABLE_MySQL_10} (semana, hora_inicio, hora_fin, tecnico_id, teleoperador_id, descripcion)"\
        "VALUES (%s, %s, %s, %s, %s, %s)"
        values = (semana, inicio_jornada, fin_jornada, tele_id, tecnico_id, descripcion)
        crs.execute(query, values)
        conn.commit()
        log_info(f"Horario del teleoperador con ID {tele_id} insertado correctamente en la base de datos.")
        writer.write(f"Horario del teleoperador con ID {tele_id} insertado correctamente.\n".encode())

        await writer.drain()
        await teleoperador_MySQL(writer, reader)  # Volver al menú de teleoperador


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
        writer.write("El ID de la ubicacion que quiere añadir".encode())
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



async def teleoperador_MySQL(writer, reader):
        menu = ("Has seleccionado la opción de TELEOPERADOR con MySQL. Selecciona la consulta que quieras hacer: "\
        "\n"\
        "1. Insertar un nuevo teleoperador \n"\
        "2. Insertar el horario del teleoperador \n"\
        "3. Eliminar un teleoperador \n"\
        "4. Consultar teleoperadores y sus horarios \n")
        writer.write(menu.encode())
        await writer.drain()
        
        message = (await reader.read(1024)).decode().strip()
        log_debug(f"Mensaje recibido: {message}")
        if message == "1":
            await add_teleoperador(writer, reader)
        elif message == "2":
            await add_horario_teleoperador(writer, reader)
        elif message == "3":
            await delete_teleoperador(writer, reader)
        elif message == "4":
            await consult_teleoperadores(writer, reader)




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
        writer.write("ELIGE UNA OPCIÓN:\n1. Teleoperador\n2. Tecnico\n3. Incidencias\n4. Salir".encode())
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

        elif option == "3":
            log_info("Consultando datos de Incidencias...")
            writer.write("Consultando datos de Incidencias...\n".encode())
            await writer.drain()
            await incidencias_MySQL(writer, reader)  # Placeholder para la función de incidencias
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