import socket

HOST = '127.0.0.1'
PORT = 8080

def handle_empresa(conn):
    conn.send("Has seleccionado la colección EMPRESAS.\\n¿Que quieres hacer?\\n1. Insertar\\n2. Buscar\\n3. Salir".encode())
    while True:
        msg = conn.recv(1024).decode()
        if msg == "1":
            conn.send("Lógica de insertar empresa (no implementada aquí)\\n".encode())
        elif msg == "2":
            conn.send("Lógica de buscar empresa (no implementada aquí)\\n".encode())
        elif msg == "3":
            conn.send("Saliendo de la colección EMPRESAS.\\n".encode())
            break
        else:
            conn.send("Opción no válida. Elige 1, 2 o 3.\\n".encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión establecida desde {addr}")
                conn.send(
                    "Bienvenido. Elige una colección:\n1. Empresas\n2. Personajes \n3. Lenguajes \nEscribe un número ".encode()
                )
                msg = conn.recv(1024).decode()
                if msg == "1":
                    handle_empresa(conn)
                elif msg == "2":
                    conn.send("Colección Personajes aún no implementada.\\n".encode())
                elif msg == "3":
                    conn.send("Colección Lenguajes aún no implementada.\\n".encode())
                else:
                    conn.send("Opción no reconocida. Cierra la conexión e inténtalo de nuevo.\\n".encode())
                print(f"Conexión con {addr} finalizada.")

if __name__ == "__main__":
    main()
