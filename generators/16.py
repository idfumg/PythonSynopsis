'''
Make the Task as a Feature. So we can wait result on it.
'''

from concurrent.futures import ThreadPoolExecutor, Future
import time

class Task(Future):
    def __init__(self, gen):
        self._gen = gen
        if not super().set_running_or_notify_cancel():
            return

    def step(self, value=None, exc=None):
        try:
            if exc:
                fut = self._gen.throw(exc)
            else:
                fut = self._gen.send(value) # future must be returned
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            super().set_result(exc.value)

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
    return result

t = Task(do_func(2, 3))
t.step()
print(f'Got: {t.result()}')
