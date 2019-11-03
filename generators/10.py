from concurrent.futures import ThreadPoolExecutor
import time

pool = ThreadPoolExecutor(8)

def func(x, y):
    time.sleep(2)
    return x + y

def handle_result(result):
    try:
        print(f'Got: {result.result()}')
    except Exception as e:
        print(f'Failed: {type(e).__name__}: {e}')

future = pool.submit(func, 2, 3) # Future with state = running
assert future.result() == 5

future = pool.submit(func, 2, 3)
future.add_done_callback(handle_result)

future = pool.submit(func, 2, 'hello')
future.add_done_callback(handle_result) # Failed!
