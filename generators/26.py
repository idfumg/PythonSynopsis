from coroutine import coroutine
from cPickle import pickle

@coroutine
def sendto(f):
    try:
        while True:
            item = (yield)
            pickle.dump(item ,f)
            f.flush()
    except StopIteration:
        f.close()

def recvfrom(f, target):
    try:
        while True:
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()
