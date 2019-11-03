def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

async def coro():
    print('coro')

class AContextManager():
    async def __aenter__(self):
        print('Entering')
        await coro()
        return self

    async def __aexit__(self, ty, val, tb):
        print('Exiting')
        await coro()

async def main():
    m = AContextManager()
    async with m:
        print('hello')

run(main())
