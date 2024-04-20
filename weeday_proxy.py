import asyncio
import argparse
import ipaddress


SOCKS_REQUEST_PREFIX = 0x05
SOCKS_NO_AUTHENTICATION = bytes([0x05, 0x00])
SOCKS_IPV4_STREAM_REQUEST = bytes([0x05, 0x01, 0x00, 0x01])
SOCKS_REQUEST_GRANTED = bytes([
    0x05, 0x00, 0x00,
    0x01, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00
])
SOCKS_GENERAL_ERROR = bytes([
    0x05, 0x01, 0x00,
    0x01, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00
])


class BaseAsyncWriter:
    def __init__(self, writer):
        self.writer = writer

    async def write(self, data):
        await self.writer.write(data)

    async def close(self):
        await self.writer.close()

    def get_extra_info(self, name):
        return self.writer.get_extra_info(name)


class AsyncWriterForAsyncWriter(BaseAsyncWriter):
    pass
    

class AsyncWriterForStreamWriter(BaseAsyncWriter):
    async def write(self, data):
        self.writer.write(data)
        await self.writer.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()


class AsyncWriter(BaseAsyncWriter):
    def __init__(self, writer):
        if isinstance(writer, AsyncWriter):
            super().__init__(AsyncWriterForAsyncWriter(writer))
        else:
            super().__init__(AsyncWriterForStreamWriter(writer))


async def pipe(reader, writer):
    data = await reader.read(4096)
    while data:
        await writer.write(data)
        data = await reader.read(4096)


def as_ip(data):
    return '.'.join(str(x) for x in data)


def as_port(data):
    return int.from_bytes(data, 'big')


async def proxy(ip, port, local_reader, local_writer):
    # XXX: The most important part
    if port == 420:
        port = 443

    foreign_reader, foreign_writer = await asyncio.open_connection(ip, port)
    foreign_writer = AsyncWriter(foreign_writer)

    await asyncio.gather(
        pipe(local_reader, foreign_writer),
        pipe(foreign_reader, local_writer),
    )

    await foreign_writer.close()


async def handle_connection(reader, writer):
    writer = AsyncWriter(writer)
    data = await reader.read(100)
    addr = writer.get_extra_info('peername')
    print(f'Received {data} from {addr!r}')

    if data[0] == SOCKS_REQUEST_PREFIX:
        await writer.write(SOCKS_NO_AUTHENTICATION)
        print(f'Sent {data} to {addr!r}')
        data = await reader.read(100)
        print(f'Received {data} from {addr!r}')
        if data[0:4] == SOCKS_IPV4_STREAM_REQUEST:
            ip = as_ip(data[4:8])
            port = as_port(data[8:10])
            print(f'Stream {ip}:{port} for {addr!r}')
            await writer.write(SOCKS_REQUEST_GRANTED)
            await proxy(ip, port, reader, writer)
        else:
            await writer.write(SOCKS_GENERAL_ERROR)

    print(f'Close the connection for {addr!r}')
    await writer.close()


async def socks_server(ip, port):
    server = await asyncio.start_server(handle_connection, ip, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    print('Happy Weed Day!')

    async with server:
        await server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        description='A minimal SOCKS5 server for National Weed Day.'
    )
    parser.add_argument(
        '--ip', default='127.0.0.1',
        type=lambda ip: str(ipaddress.IPv4Address(ip)),
        help='Bind IPv4 address.'
    )
    parser.add_argument(
        '--port', default='1080', type=int,
        help='Bind port.'
    )
    
    args = parser.parse_args()
    asyncio.run(socks_server(**args.__dict__))


if __name__ == '__main__':
    main()
