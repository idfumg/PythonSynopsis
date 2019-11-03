################################################################################
# Looses useful feautures like keyword arguments and inspect of the class
################################################################################

class Structure:
    _fields = []
    def __init__(self, *args):
        for name, value in zip(self.__class__._fields, args):
            setattr(self, name, value)

class Stock(Structure):
    _fields = ['name', 'shares', 'price']

class Point(Structure):
    _fields = ['x', 'y']

class Address(Structure):
    _fields = ['hostname', 'port']

point = Point(1, 2)
assert point.x == 1

################################################################################
# Improve previous example with inspect useful stuff with error checking
################################################################################

def make_signature(names):
    from inspect import Signature, Parameter
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)

class Structure:
    __signature__ = make_signature([])
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, value)

class Point(Structure):
    __signature__ = make_signature(['x', 'y'])

point = Point(1, 2)
assert point.x == 1

import inspect
inspect.signature(Point) # (x, y)

################################################################################
# Try to simplify and add a class decorator
################################################################################

def add_signature(*names):
    def decorate(cls):
        cls.__signature__ = make_signature(names)
        return cls
    return decorate

@add_signature('x', 'y')
class Point(Structure):
    pass

################################################################################
# Try to simplify the above example with a meta class
################################################################################

class StructMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj._fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj

class Structure(metaclass=StructMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, value)

class Point(Structure):
    _fields = ['x', 'y']

assert Point(1, 2).x == 1
assert isinstance(Point(1,1), Point)
assert isinstance(Point(1,1), Structure)
