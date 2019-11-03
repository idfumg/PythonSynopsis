async def fib(n):
    if n < 2:
        return 1
    return await fib(n-1) + await fib(n-2)

async def main():
    for n in range(20):
        print(await fib(n))

async def list_comprehension():
    nums = [1,2,3,4,5]
    fibs = [await fib(n) for n in nums]
    print(fibs)

def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

run(main())
run(list_comprehension())
