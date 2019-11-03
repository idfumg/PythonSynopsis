'''
We can throw an exception from the coroutine.
'''

from coroutine import coroutine

@coroutine
def grep(pattern):
    print(f'Looking for a pattern: {pattern}')
    try:
        while True:
            line = (yield)
            if pattern in line:
                print(line)
    except GeneratorExit:
        print('Goodbye')

g = grep("python")
g.send("cython")
g.send("python")
g.throw(RuntimeError, 'Some exceptional error')
