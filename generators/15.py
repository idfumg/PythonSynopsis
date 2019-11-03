from concurrent.futures import ThreadPoolExecutor, Future
import time

class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None, exc=None):
        try:
            if exc:
                fut = self._gen.throw(exc)
            else:
                fut = self._gen.send(value) # future must be returned
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        try:
            result = fut.result()
            self.step(result) # feedback loop (run to next yield)
        except Exception as exc:
            self.step(None, exc)

pool = ThreadPoolExecutor(8)

def func(x, y):
    time.sleep(1)
    return x + y

def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print(f'Got: {result}')

def patch_future(cls):
    def __iter__(self):
        if not self.done():
            yield self
        return self.result()
    cls.__iter__ = __iter__

def after(delay, gen):
    patch_future(Future) # Future object is not iterable exception fix
    yield from pool.submit(time.sleep, delay)
    yield from gen

Task(after(1, do_func(2, 3))).step()
