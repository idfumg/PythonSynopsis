import sys

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def from_coro(n):
    return bool(sys._getframe(n).f_code.co_flags & 0x80)

def foo():
    print(from_coro(1))

async def bar():
    print(from_coro(1))

foo()
run(bar())
