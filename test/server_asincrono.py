#! IMPORTS
    #? SOCKETS
import asyncio

Shost = "localhost"
Sport = 8083


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión desde {addr}")
    writer.write("Conexión establecida. Envía un mensaje.\n".encode())
    await writer.drain()
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Recibido: {message}")
        response = f"Echo: {message}"
        writer.write(response.encode())
        await writer.drain()

async def main():
    s = await asyncio.start_server(
        handle_client, Shost, Sport
    )
    print(f"Servidor escuchando en {Shost}:{Sport}")
    async with s:
        await s.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
    