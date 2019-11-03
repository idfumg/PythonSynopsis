def generator():
    try:
        yield
    except RuntimeError as e:
        print(e)
    yield 'hello after first yield'

g = generator()
next(g)
result = g.throw(RuntimeError, 'Broken')
assert result == 'hello after first yield'
