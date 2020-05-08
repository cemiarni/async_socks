import uasyncio as asyncio


def as_ip(data):
    return '.'.join(str(x) for x in data)


def as_port(data):
    return int.from_bytes(data, 'big')


async def pipe(reader, writer):
    data = await reader.read(100)
    while data:
        await writer.awrite(data)
        data = await reader.read(100)


async def proxy(ip, port, local_reader, local_writer):
    foreign_reader, foreign_writer = await asyncio.open_connection(ip, port)

    loop = asyncio.get_event_loop()
    p1 = pipe(local_reader, foreign_writer)
    p2 = pipe(foreign_reader, local_writer)
    loop.create_task(p2)

    await asyncio.wait_for(p1, 60)

    await foreign_writer.aclose()


async def handle_accept(reader, writer):
    data = await reader.read(100)
    addr = writer.get_extra_info('peername')

    print("Received {} from {}".format(data, repr(addr)))
    if data[0] == 0x05:
        data = bytes([0x05, 0x00])
        await writer.awrite(data)  # no authentication
        print('Sent {} to {}'.format(data, repr(addr)))
        data = await reader.read(100)
        print("Received {} from {}".format(data, repr(addr)))
        if data[0:4] == bytes([0x05, 0x01, 0x00, 0x01]):  # IPv4 bind request
            ip = as_ip(data[4:8])
            port = as_port(data[8:10])
            print('{}:{} for {}'.format(ip, port, repr(addr)))
            # Response ACK
            await writer.awrite(bytes([
                0x05, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00
            ]))
            await proxy(ip, port, reader, writer)
        #else:
        #    writer.write(bytes([
        #        0x05, 0x01, 0x00,
        #        0x01, 0x00, 0x00, 0x00, 0x00,
        #        0x00, 0x00
        #    ]))
        #    await writer.drain()
        #    data = await reader.read(100)
        #    print(f"Received {data} from {addr!r}")


    print("Close the connection")
    await writer.aclose()

async def main():
    server = await asyncio.start_server(
        handle_accept, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print('Serving on {}'.format(addr))

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
