def generator():
    yield 1
    yield 2
    yield 3
    yield 4
    return 42

def foo():
    print('start foo')
    result = yield from generator()
    print(result)

f = foo()
assert f.send(None) == 1
assert f.send(None) == 2
assert f.send(None) == 3
assert f.send(None) == 4
f.send(None) # Exception would be thrown
