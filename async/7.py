async def greeting(name):
    return 'Hello ' + name

async def main():
    print(await greeting('Guido')))

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

run(main()) # Hello Guido
