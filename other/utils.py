from collections import Iterable

def unfold(lstlst):
    '''
    Способ сделать из списка списков плоский список.
    '''

    rv = []

    for lst in lstlst:
        if isinstance(lst, list):
            rv.extend(lst)
        else:
            rv.append(lst)

    return rv


def gen_unfold(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from gen_unfold(x)
        else:
            yield x


def group_by(lst, fn):
    '''
    Можно подсчитать число повторяющихся элементов,
    если группировать по значению поля (после просто взять len результата).
    Можно искать совпадения по первым буквам.
    Или группировать по параметру (например, fn = len).
    '''

    rv = defaultdict(list)

    for elem in lst:
        key = fn(elem)
        rv[key].append(elem)

    return rv
