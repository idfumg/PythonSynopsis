from concurrent.futures import ThreadPoolExecutor
import time

class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None):
        try:
            fut = self._gen.send(value) # future must be returned
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        result = fut.result()
        self.step(result) # feedback loop (run to next yield)

pool = ThreadPoolExecutor(8)

def func(x, y):
    time.sleep(2)
    return x + y

def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print(f'Got: {result}')

g = do_func(2, 3)
task = Task(g)
task.step()
print('after')
