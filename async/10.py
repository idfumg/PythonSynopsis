from functools import wraps
import sys

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def from_coro(n):
    return bool(sys._getframe(n).f_code.co_flags & 0x80)

def sync_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if from_coro(2):
            raise RuntimeError('Sorry')
        return func(*args, **kwargs)
    return wrapper

@sync_only
def foo():
    print('Hello Guido')

async def bar():
    foo()

foo()
run(bar())
