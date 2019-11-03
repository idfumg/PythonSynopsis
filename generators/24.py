from coroutine import coroutine
import time

def follow(fd, target):
    #fd.seek(0, 2)
    while True:
        line = fd.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)

@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)

@coroutine
def printer():
    while True:
        line = (yield)
        print(line)

@coroutine
def broadcast(targets):
    while True:
        data = (yield)
        for target in targets:
            target.send(data)

fd = open('/etc/passwd')
p = printer()
follow(fd,
       broadcast([grep('python', p),
                  grep('ply', p),
                  grep('swig', p),
                  grep(':', p)]))
