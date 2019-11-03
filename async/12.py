def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

async def coro():
    print('coro')

class ACountdown(object):
    def __init__(self, n):
        self.n = n

    async def __aiter__(self):
        await coro()
        return self

    async def __anext__(self):
        if self.n < 1:
            raise StopAsyncIteration
        await coro()
        self.n -= 1
        return self.n + 1

async def main():
    c = ACountdown(5)
    async for x in c:
        print(x)

run(main())
