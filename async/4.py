import asyncio

class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data):
        self.transport.write(data)

def main(port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(EchoProtocol, '', port)
    srv = loop.run_until_complete(coro)
    loop.run_forever()
