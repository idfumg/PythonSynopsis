import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        print(f"{label}: {time.time() - start}")

with timethis('counting'):
    n = 1000000
    while n > 0:
        n -= 1
