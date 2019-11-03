from functools import partial, wraps

def debug(func=None, *, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('called')
        return func(*args, **kwargs)
    return wrapper

def debugmethods(klass):
    print('debugmethods')
    for name, value in vars(klass).items():
        if callable(value):
            print('setattr for key: {}'.format(name))
            setattr(klass, name, debug(value))

    return klass

@debugmethods
class Spam:
    def a(self):
        print('a')

    def b(self):
        print('b')

spam = Spam()
spam.a()
spam.b()
