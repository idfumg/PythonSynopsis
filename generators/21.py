'''
Coroutines like generators but you have to send into it some data.
The ones have to be activeted by sending send(None) or by calling next(c).
This operation go to the first operation out.
'''

def grep(pattern):
    print(f'Looking for a pattern: {pattern}')
    while True:
        line = (yield)
        if pattern in line:
            print(line)

g = grep("python")
next(g)
g.send("cython")
g.send("python")
del g # or it stays active infinitely
