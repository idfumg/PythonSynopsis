def generator():
    yield 42
    return 'hello'

g = generator()
try:
    assert next(g) == 42
    next(g)
except StopIteration as e:
    assert e.value == 'hello'
