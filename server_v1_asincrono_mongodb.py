import socket
import asyncio


# ? CONFIGURACIÓN DEL SERVIDOR
HOST = 'localhost'
PORT = 8080

# ? CONFIGURACIÓN DE LA BASE DE DATOS
DB = "ZOO"
COLLECTION_1 = "ANIMALES"


async def start_server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()
