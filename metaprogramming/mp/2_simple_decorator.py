from functools import wraps, partial

def debug(func=None, *, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(prefix + func.__name__)
        return func(*args, **kwargs)
    return wrapper

@debug
def add(x, y):
    return x + y

@debug(prefix="***")
def sub(x, y):
    return x - y

print(add(1, 2))
print(sub(3, 2))
