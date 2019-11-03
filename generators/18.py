'''
Just rolling up Futures until they done.
'''

import asyncio

@asyncio.coroutine
def echo_client(reader, writer):
    while True:
        line = yield from reader.readline()
        if not line:
            break
        resp = b'Got:' + line
        writer.write(resp)
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.start_server(echo_client, host='', port=25000)
)
loop.run_forever()
