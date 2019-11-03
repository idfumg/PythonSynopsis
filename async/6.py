async def greeting(name):
    return 'Hello ' + name

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

run(greeting('Guido')) # Hello Guido
