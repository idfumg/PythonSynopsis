'''
We can catch generator exit exceptions when we are calling .close() method.
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
g.close()
