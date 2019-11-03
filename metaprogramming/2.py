################################################################################
# Simple decorator. But it looses the function info (f.__name__ and help(f))
################################################################################

def debug_simple(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

################################################################################
# Normal decorator. Saves the function information.
################################################################################

from functools import wraps
def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

assert debug.__name__ == 'debug'
assert debug.__qualname__ == 'debug'

################################################################################
# Decorator with logging.
################################################################################

from functools import wraps
import logging

def debug(func):
    log = logging.getLogger(func.__module__)
    msg = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(msg)
        return func(*args, **kwargs)
    return wrapper

################################################################################
# Decorator with optional logging by environment variable.
################################################################################

import os

def debug(func):
    if 'DEBUG' not in os.environ:
        return func
    log = logging.getLogger(func.__module__)
    msg = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(msg)
        return func(*args, **kwargs)
    return wrapper

################################################################################
# Decorator with arguments.
################################################################################

def debug(prefix=''):
    def decorate(func):
        msg = prefix + func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

################################################################################
# Decorator with arguments (more compact style).
################################################################################

from functools import partial

def debug(func=None, *, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)

    msg = prefix + func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper

@debug(prefix='***')
def myfunc(): pass

################################################################################
# Decorator for debugging all the methods of a class
################################################################################

def debugmethods(cls):
    for key, value in vars(cls).items():
        if callable(value):
            setattr(cls, key, debug(value))
    return cls

@debugmethods
class Spam:
    def a(self):
        pass
    def b(self):
        pass

# s = Spam()
# s.a()

################################################################################
# Decorator for debugging attributes access in a class
################################################################################

def debugattr(cls):
    orig_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print('Get:', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__

    return cls

@debugattr
class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

# foo = Foo(1, 2)
# foo.a

################################################################################
# Decorator for debugging a metaclass of a class
################################################################################

class debugmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict) # create an instance
        clsobj = debugmethods(clsobj)
        return clsobj

class Base(metaclass=debugmeta):
    pass

class Foo(Base): # metaclass propogates down through the hierarchies
    pass

class Bar(Base):
    pass

class FooBar(Foo, Bar):
    pass

################################################################################
# Types of decorators and their impact:
# 1. Decorators -> functions
# 2. Class decorators -> classes
# 3. Metaclasses -> class hierarchies
################################################################################
