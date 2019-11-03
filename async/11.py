from functools import wraps
import sys

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def from_coro(n):
    return bool(sys._getframe(n).f_code.co_flags & 0x80)

def awaitable(syncfunc):
    def decorate(asyncfunc):
        @wraps(asyncfunc)
        def wrapper(*args, **kwargs):
            if from_coro(2):
                return asyncfunc(*args, **kwargs)
            else:
                return syncfunc(*args, **kwargs)
        return wrapper
    return decorate

def foo():
    print('The blue pill')

@awaitable(foo)
async def foo():
    print('The red pill')

async def main():
    await foo()

foo()
run(main())
