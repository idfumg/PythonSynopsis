################################################################################
# Try to more simplify the above example with a meta class
################################################################################

class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object
    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError(f'Expected {self.ty}')
        super().__set__(instance, value) # Not always a parent class

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)

class String(Typed):
    ty = str

class SizedString(String, Sized):
    pass

import re

class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance, value)

class SizedRegexString(SizedString, Regex):
    pass

class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Must be >= 0')
        super().__set__(instance, value)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

from collections import OrderedDict

class StructMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, clsdict):
        fields = [key for key, value in clsdict.items() if isinstance(value, Descriptor)]
        for name in fields:
            clsdict[name].name = name

        clsobj = super().__new__(cls, name, bases, dict(clsdict))
        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj

class Structure(metaclass=StructMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, value)

class Point(Structure):
    x = Integer()
    y = PositiveInteger()
    name = SizedRegexString(pat='^[A-Z]+$', maxlen=8)

p = Point(1, 2, name="ASD")
p.name = "ZZZADA"

print(PositiveInteger.__mro__)
