'''
SERVIDOR V2 MAX
Lo mismo que el v1 pero con más cosas en la base de datos. XD  (COMPLICANDOSE LA VIDA, EN VEZ DE HACERLO MÁS FÁCIL COMO EN EL V1)

'''

#! IMPORTS
    #? SOCKETS
import socket
import time

    #? DataBase
from pymongo import MongoClient
import mysql.connector

    #? Logs
from logs.Logs_Masivo_V2 import log_info, log_error, log_warning, log_debug, log_critical



# TODO =============== CONFIGURACIONES ================
#? Configuración del servidor
Shost = "localhost"
Sport = 8083
tiempo_espera = 2  # Tiempo de espera en segundos para la conexión


#? Configuración de la base de datos MongoDB

MONGO_URI = MongoClient("mongodb://localhost:27017/")
DB_MONGO = "Max_2"
CLIENT_MDB = MONGO_URI[DB_MONGO]

COLLECTION_MONGO_1= "Empresa"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Juegos_plataformas"
COLLECTION_MONGO_4 = "Personajes"


#? Configuración de la base de datos MySQL
DB_MySQL = "db_python"
USER_MySQL = "test_pithon"
PASSWORD_MySQL = "321_atomica"
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
def collection_MDB_4(conn: socket.socket): #? Personajes
    COL_Per = CLIENT_MDB[COLLECTION_MONGO_4]
    COL_Jue = CLIENT_MDB[COLLECTION_MONGO_2]


    log_warning(f"== EN ESPERA AUTOMATICA DE 5s ==")
    print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")
    time.sleep(tiempo_espera)

    conn.send("=============== CONSULTAS PERSONAJES MySQL ==============\n" \
        "\n 1. Insertar personaje"\
        "\n 2. Ver todos los personajes"\
        "\n 3. Otras busquedas"\
        "\n 4. Salir"\
        .encode())
    
    msg = conn.recv(1024).decode()
    
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)
    log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")
    print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")

    if msg == "1":
        log_info("[CLIENT] OPCION INSERTAR PERSONAJE")
        print("[CLIENT] OPCION INSERTAR PERSONAJE")
        
        conn.send("NOMBRE".encode())
        nombre = conn.recv(1024).decode().capitalize()
        log_info(f"Nombre recibido: {nombre}")
        
        conn.send("ELEMENTO".encode())
        elemento = conn.recv(1024).decode().capitalize()
        log_info(f"Elemento recibido: {elemento}")
        
        conn.send("GENERO".encode())
        genero = conn.recv(1024).decode().capitalize()
        log_info(f"Género recibido: {genero}")

        conn.send("RAREZA (SI EL PERSONAJE NO TIENE INTRODUCE: '-')".encode())
        rareza = conn.recv(1024).decode().capitalize()
        log_info(f"Rareza recibida: {rareza}")

        conn.send("ARMA (SI EL PERSONAJE NO TIENE INTRODUCE: '-')".encode())
        arma = conn.recv(1024).decode().capitalize()
        log_info(f"Arma recibida: {arma}")

        conn.send("FACCION".encode())
        faccion = conn.recv(1024).decode().capitalize()
        log_info(f"Facción recibida: {faccion}")

        # ! SACAR LOS IDES DE LOS JUEGOS ACTUALES

        jg_list = "Lista de juegos disponibles:\n"
        R = COL_Jue.find()
        for doc in R:
            jg_list += f"ID: {doc['id']} - NOMBRE: {doc['nombre']}\n"

        conn.send(f"{jg_list}\n ENTER PARA SEGUIR".encode())
        
        conn.send("ID DEL JUEGO".encode())
        id_j = conn.recv(1024).decode()
        log_info(f"ID Juego recibido: {id_j}")

        data = {
            "id": COL_Per.count_documents({}) + 1,  # Generar un ID único
            "nombre": nombre,
            "elemento": elemento, 
            "genero": genero,
            "rareza": rareza,
            "arma": arma,
            "faccion": faccion,
            "juego_id": int(id_j)  # Convertir a entero
        }

        COL_Per.insert_one(data)
        conn.send(f"Personaje {nombre} insertado correctamente en la base de datos MongoDB.".encode())
        log_info(f"Personaje {nombre} insertado correctamente en la base de datos MongoDB.\n")

    if msg == "2":
        log_info("[CLIENT] OPCION VER TODOS LOS PERSONAJES")
        print("[CLIENT] OPCION VER TODOS LOS PERSONAJES")
        conn.send("\nENTER PARA CONTINUAR\n".encode())
        personajes_list = "Lista de personajes:\n"
        R = COL_Per.find()
        
        for doc in R:
            personajes_list += f"ID: {doc['id'] } -  NOMBRE: {doc['nombre']} - GENERO: {doc['genero']} - "\
                f"ELEMENTO: {doc['elemento']} - RAREZA: {doc['rareza']} - ARMA: {doc['arma']} - FACCION: {doc['faccion']}\n"

        conn.send(f"{personajes_list} ".encode())
        log_info(f"Personajes listados correctamente en la base de datos MongoDB.")



# TODO: =============== CONSULTAS MySQL ================

#? PERSONAJES
def consulta_table4_mysql(conn: socket.socket):
    cursor = get_MySQL_conn() # Conexión a la base de datos MySQL
    log_warning(f"== EN ESPERA AUTOMATICA DE 5s ==")
    print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")
    time.sleep(tiempo_espera)

    conn.send("=============== CONSULTAS PERSONAJES MySQL ==============\n" \
        "\n 1. Insertar personaje"\
        "\n 2. Ver todos los personajes"\
        "\n 3. Otras busquedas"\
        "\n 4. Salir"\
        .encode())
    
    msg = conn.recv(1024).decode()
    
    log_info(f"Mensaje recibido: {msg}")
    time.sleep(tiempo_espera)
    log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")
    print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")

    if msg == "1":
        log_info("[CLIENT] OPCION INSERTAR PERSONAJE")
        print("[CLIENT] OPCION INSERTAR PERSONAJE")
        
        conn.send("Tu personaje tiene arma y rareza? (S/N _ Y/N)".encode())
        msg = conn.recv(1024).decode()

        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)
        print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")

        if msg.lower() == "s" or msg.lower() == "y" or msg.lower() == "si" or msg.lower() == "yes":
            #? Insertar un personaje en la base de datos MySQL
            conn.send("NOMBRE ".encode())
            nombre = conn.recv(1024).decode().capitalize()
            log_info(f"Nombre recibido: {nombre}")
    
            conn.send("ELEMENTO ".encode())
            elemento = conn.recv(1024).decode().capitalize()
            log_info(f"Elemento recibido: {elemento}")
    
            conn.send("GENERO".encode())
            genero = conn.recv(1024).decode().capitalize()
            log_info(f"Género recibido: {genero}")
    
            conn.send("RAREZA".encode())
            rareza = conn.recv(1024).decode().capitalize()
            log_info(f"Rareza recibida: {rareza}")
    
            conn.send("ARMA".encode())
            arma = conn.recv(1024).decode().capitalize()
            log_info(f"Arma recibida: {arma}")
    
            conn.send("FACCION".encode())
            faccion = conn.recv(1024).decode().capitalize()
            log_info(f"Facción recibida: {faccion}")
            
            # ? PARA SACAR LOS IDES DE LOS JUEGOS ACTUALES
            query = "select id, nombre from juegos"
            c = cursor.cursor()
            c.execute(query)
            juegos_list = "Lista de juegos disponibles:\n "
            for list in c.fetchall():
                juegos_list += f"ID: {list[0]} - NOMBRE: {list[1]}\n"
    
            conn.send(f"{juegos_list} \nENTER PARA CONTINUAR".encode())
            conn.send("Escribe el ID JUEGO".encode())
            id_juego = conn.recv(1024).decode()
            log_info(f"ID Juego recibido: {id_juego}")
    
            # TODO: INSERTAR PERSONAJE EN LA BASE DE DATOS
            query = "INSERT INTO personajes (nombre, elemento, genero, rareza, arma, faccion, juego_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (nombre, elemento, genero, rareza, arma, faccion, id_juego)
            c.execute(query, values)
            cursor.commit()
    
            log_info(f"Personaje {nombre} insertado correctamente en la base de datos MySQL.")
            conn.send(f"Personaje {nombre} insertado correctamente en la base de datos MySQL.".encode())
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
        
        elif msg.lower() == "n" or msg.lower() == "no":
            #? Insertar un personaje en la base de datos MySQL
            conn.send("NOMBRE ".encode())
            nombre = conn.recv(1024).decode().capitalize
            log_info(f"Nombre recibido: {nombre}")

            conn.send("ELEMENTO ".encode())
            elemento = conn.recv(1024).decode().capitalize()
            log_info(f"Elemento recibido: {elemento}")

            conn.send("GENERO".encode())
            genero = conn.recv(1024).decode().capitalize()
            log_info(f"Género recibido: {genero}")

            conn.send("FACCION".encode())
            faccion = conn.recv(1024).decode().capitalize()
            log_info(f"Facción recibida: {faccion}")

            # ? PARA SACAR LOS IDES DE LOS JUEGOS ACTUALES
            query = "select id, nombre from juegos"
            c = cursor.cursor()
            c.execute(query)
            juegos_list = "Lista de juegos disponibles:\n "
            for list in c.fetchall():
                juegos_list += f"ID: {list[0]} - NOMBRE: {list[1]}\n"

            conn.send(f"{juegos_list} \nENTER PARA CONTINUAR".encode())
            conn.send("Escribe el ID JUEGO".encode())
            id_juego = conn.recv(1024).decode()
            log_info(f"ID Juego recibido: {id_juego}")

            # TODO: INSERTAR PERSONAJE EN LA BASE DE DATOS
            query = "INSERT INTO personajes (nombre, elemento, genero, faccion, juego_id) VALUES (%s, %s, %s, %s, %s)"
            values = (nombre, elemento, genero, faccion, id_juego)
            c.execute(query, values)
            cursor.commit()

            log_info(f"Personaje {nombre} insertado correctamente en la base de datos MySQL.")
            conn.send(f"Personaje {nombre} insertado correctamente en la base de datos MySQL.".encode())
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'

    #? Visualizar
    elif msg == "2":
        log_info("[CLIENT] OPCION VER TODOS LOS PERSONAJES")
        print("[CLIENT] OPCION VER TODOS LOS PERSONAJES")
        query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id ORDER BY j.nombre ASC"
        c = cursor.cursor()
        c.execute(query)
        personajes_list = "Lista de personajes:\n"
        for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
        conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
        log_info(f"Personajes listados correctamente en la base de datos MySQL.")
        consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
    
    #? Otras busquedas
    elif msg == "3":
        log_info("[CLIENT] OPCION OTRAS BUSQUEDAS")
        print("[CLIENT] OPCION OTRAS BUSQUEDAS")
        conn.send("=============== OTRAS BUSQUEDAS ==============\n" \
            "\n 1. Buscar por nombre" \
            "\n 2. Buscar por genero" \
            "\n 3. Buscar por elemento" \
            "\n 4. Buscar por rareza" \
            "\n 5. Buscar por faccion" \
            "\n 6. salir".encode())

        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")

        time.sleep(tiempo_espera)
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")
        print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")

        if msg == "1": # ? Nombre personaje
            log_info("[CLIENT] OPCION BUSCAR POR NOMBRE")
            print("[CLIENT] OPCION BUSCAR POR NOMBRE")
            
            conn.send("NOMBRE DEL PERSONAJE".encode())
            nombre = conn.recv(1024).decode().capitalize()

            log_info(f"Nombre recibido: {nombre}")

            query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.nombre LIKE %s "
            values = (f"%{nombre}%",)
            c = cursor.cursor()
            c.execute(query, values)
            personajes_list = "Lista de personajes:\n"
            for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
            conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
            log_info(f"Personajes filtrados por nombre correctamente en la base de datos MySQL.")
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'

        elif msg == "2": # ? Genero personaje
            log_info("[CLIENT] OPCION BUSCAR POR GENERO")
            print("[CLIENT] OPCION BUSCAR POR GENERO")
            conn.send("GENERO DEL PERSONAJE".encode())
            genero = conn.recv(1024).decode().capitalize()
            log_info(f"Género recibido: {genero}")
            query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.genero LIKE %s "
            values = (f"%{genero}%",)
            c = cursor.cursor()
            c.execute(query, values)
            personajes_list = "Lista de personajes:\n"
            for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
            conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
            log_info(f"Personajes filtrados por género correctamente en la base de datos MySQL.")
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
        
        elif msg == "3": # ? Elemento personaje
            log_info("[CLIENT] OPCION BUSCAR POR ELEMENTO")
            print("[CLIENT] OPCION BUSCAR POR ELEMENTO")
            conn.send("ELEMENTO DEL PERSONAJE".encode())
            elemento = conn.recv(1024).decode().capitalize()
            log_info(f"Elemento recibido: {elemento}")
            query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.elemento LIKE %s "
            values = (f"%{elemento}%",)
            c = cursor.cursor()
            c.execute(query, values)
            personajes_list = "Lista de personajes:\n"
            for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
            conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
            log_info(f"Personajes filtrados por elemento correctamente en la base de datos MySQL.")
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
        elif msg == "4": # ? Rareza personaje
            log_info("[CLIENT] OPCION BUSCAR POR RAREZA")
            print("[CLIENT] OPCION BUSCAR POR RAREZA")
            conn.send("RAREZA DEL PERSONAJE".encode())
            rareza = conn.recv(1024).decode().capitalize()
            log_info(f"Rareza recibida: {rareza}")
            query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.rareza LIKE %s "
            values = (f"%{rareza}%",)
            c = cursor.cursor()
            c.execute(query, values)
            personajes_list = "Lista de personajes:\n"
            for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
            conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
            log_info(f"Personajes filtrados por rareza correctamente en la base de datos MySQL.")
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
        elif msg == "5": # ? Faccion personaje
            log_info("[CLIENT] OPCION BUSCAR POR FACCION")
            print("[CLIENT] OPCION BUSCAR POR FACCION")
            conn.send("FACCION DEL PERSONAJE".encode())
            faccion = conn.recv(1024).decode().capitalize()
            log_info(f"Facción recibida: {faccion}")
            query = "SELECT j.nombre, p.* FROM personajes p INNER JOIN juegos j ON p.juego_id = j.id WHERE p.faccion LIKE %s "
            values = (f"%{faccion}%",)
            c = cursor.cursor()
            c.execute(query, values)
            personajes_list = "Lista de personajes:\n"
            for list in c.fetchall():
                personajes_list += f"NOMBRE DEL JUEGO: {list[0]} - ID PERSONAJE: {list[1]} "\
                f"- NOMBRE: {list[2]} - GENERO: {list[4]} - ELEMENTO: {list[3]} - RAREZA: {list[5]} - ARMA: {list[6]}"\
                f"- FACCION: {list[7]}\n"
            conn.send(f"{personajes_list} \nENTER PARA CONTINUAR\n".encode())
            log_info(f"Personajes filtrados por facción correctamente en la base de datos MySQL.")
            consulta_table4_mysql(conn) #esto lo que provoca es que vuelva al menu de las opciones de la tabla de 'personajes'
        elif msg == "6": # ? Salir
            log_info("[CLIENT] OPCION SALIR")
            print("[CLIENT] OPCION SALIR")
            conn.send("Saliendo...".encode())
            log_info("Saliendo...")
            conn.close()
        else:
            log_error(f"Mensaje no reconocido: {msg}")
            conn.send("Opción no válida. Inténtalo de nuevo.".encode())
            consulta_table4_mysql(conn)


    elif msg == "4": # ? Salir
        log_info("[CLIENT] OPCION SALIR")
        print("[CLIENT] OPCION SALIR")
        conn.send("Saliendo...".encode())
        log_info("Saliendo...")
        conn.close()
    else:
        log_error(f"Mensaje no reconocido: {msg}")
        conn.send("Opción no válida. Inténtalo de nuevo.".encode())
        consulta_table4_mysql(conn)









# TODO: =============== CONFIGURACION CONEXION BASES DE DATOS, SELECCION DE TABLAS ================

#TODO: CONFIGURACION DE MONGO DB
def consultas_MongoDB(conn: socket.socket):
    while True:
        conn.send("=============== CONSULTAS MONGO DB ==============\n" \
            "\n 1. Personajes" \
            "\n 2. Empresas" \
            "\n 3. Juegos (ANTES DE METER EL JUEGO, SE NECESITA SU NUMERO DE EMPRESA)" \
            "\n 4. Salir" \
        "".encode())
        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")
        print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")

        if msg == "1":
            log_info("[CLIENT] OPCION PERSONAJES")
            print("[CLIENT] OPCION PERSONAJES")
            collection_MDB_4(conn)
        elif msg == "2":
            log_info("[CLIENT] OPCION EMPRESAS")
            print("[CLIENT] OPCION EMPRESAS")
            conn.send("SIN CONFIGURAR".encode())
            # collection_MDB_1(conn)
        elif msg == "3":
            log_info("[CLIENT] OPCION JUEGOS")
            print("[CLIENT] OPCION JUEGOS")
            conn.send("SIN CONFIGURAR".encode())
            # collection_MDB_2(conn)
        elif msg == "4":
            log_info("[CLIENT] OPCION SALIR")
            print("[CLIENT] OPCION SALIR")
            conn.send("Saliendo...".encode())
            log_info("Saliendo...")
            conn.close()
        else: 
            log_error(f"Mensaje no reconocido: {msg}")
            conn.send("Opción no válida. Inténtalo de nuevo.".encode())
            consultas_MongoDB(conn)




#TODO: CONFIGURACION DE MySQL
def consultas_MySQL(conn: socket.socket):
    while True:
        conn.send("=============== CONSULTAS MySQL ==============\n" \
            "\n 1. Personajes" \
            "\n 2. Empresas" \
            "\n 3. Juegos (ANTES DE METER EL JUEGO, SE NECESITA SU NUMERO DE EMPRESA)" \
            "\n 4. Salir" \
        "".encode())

        msg = conn.recv(1024).decode()
        log_info(f"Mensaje recibido: {msg}")
        time.sleep(tiempo_espera)
        log_warning(f"== EN ESPERA AUTOMATICA DE {tiempo_espera}s ==")
        print("[TIME SLEEP] Esperando 5 segundos antes de continuar...")

        if msg == "1":
            log_info("[CLIENT] OPCION PERSONAJES")
            print("[CLIENT] OPCION PERSONAJES")
            consulta_table4_mysql(conn)
        elif msg == "2":
            log_info("[CLIENT] OPCION EMPRESAS")
            print("[CLIENT] OPCION EMPRESAS")
            conn.send("SIN CONFIGURAR".encode())
            # consulta_table1_mysql(conn)
        elif msg == "3":
            log_info("[CLIENT] OPCION JUEGOS")
            print("[CLIENT] OPCION JUEGOS")
            conn.send("SIN CONFIGURAR".encode())
            # consulta_table2_mysql(conn)
        elif msg == "4":
            log_info("[CLIENT] OPCION SALIR")
            print("[CLIENT] OPCION SALIR")
            conn.send("Saliendo...".encode())
            log_info("Saliendo...")
            conn.close()
        else: 
            log_error(f"Mensaje no reconocido: {msg}")
            conn.send("Opción no válida. Inténtalo de nuevo.".encode())
            consultas_MongoDB(conn)




# TODO: =============== SERVIDOR ================

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Shost, Sport))
        s.listen(5)
        log_info(f"Servidor iniciado en {Shost}:{Sport}")

        while True:
            conn, addr = s.accept()
            log_warning(f"== EN ESPERA AUTOMATICA DE 5s ==")
            print("[TIME SLEEP] Esperando 5 segundos antes de aceptar la conexión...")
            time.sleep(tiempo_espera)
            log_info(f"Conexión aceptada de {addr}")

            with conn:
                log_info(f"Conexión establecida con {addr}")
                print(f"Conexión establecida con {addr}")

                conn.send("Bienvenido al servidor masivo v2. " \
                "\n Elige una opcion:"
                "\n 1. MongoDB"
                "\n 2. MySQL"
                "\n Escribe un numero: ".encode())

                msg = conn.recv(1024).decode()
                log_info(f"Mensaje recibido: {msg}")
                
                if msg == "1":
                    log_info("[CLIENT] OPCION MONNGODB")
                    print("[CLIENT] OPCION MONGODB")
                    conn.send("SELECCION MONGODB, ENTER PARA CONTINUAR".encode())
                    consultas_MongoDB(conn)
                elif msg == "2":
                    log_info("[CLIENT] OPCION MYSQL")
                    print("[CLIENT] OPCION MYSQL")
                    conn.send("SELECCION MYSQL, ENTER PARA CONTINUAR".encode())
                    consultas_MySQL(conn)
                else: 
                    log_error(f"Mensaje no reconocido: {msg}")
                    conn.send("Opción no válida. Inténtalo de nuevo.".encode())
                    continue


if __name__ == "__main__":
    start_server()
    log_info("Servidor iniciado correctamente.")
    log_warning("Servidor en espera de conexiones...")
