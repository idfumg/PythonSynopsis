def chain(x, y):
    yield from x
    yield from y

a = [1,2,3]
b = [4,5,6]

for n in chain(a, b):
    print(n, end=' ') # 1 2 3 4 5 6

print()

def chain2(x, y):
    yield x
    yield y

for n in chain2(a, b):
    print(n, end=' ') # [1, 2, 3] [4, 5, 6]

print()
