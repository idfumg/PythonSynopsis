################################################################################
# Add some performance by removing __set__ methods of an every class and inspect
################################################################################

def _make_init(fields):
    code = 'def __init__(self, {}):\n'.format(', '.join(fields))
    for name in fields:
        code += '    self.{} = {}\n'.format(name, name)
    return code

def _make_setter(dcls):
    code = 'def __set__(self, instance, value):\n'
    for d in dcls.__mro__:
        if 'set_code' in d.__dict__:
            for line in d.set_code():
                code += '    ' + line + '\n'
    return code

class DescriptorMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)

        if '__set__' in clsdict:
            raise TypeError('use set_code(), not __set__()')

        code = _make_setter(self)
        exec(code, globals(), clsdict)
        setattr(self, '__set__', clsdict['__set__'])

class Descriptor(metaclass=DescriptorMeta):
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    @staticmethod
    def set_code():
        return [
            'instance.__dict__[self.name] = value'
        ]

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object

    @staticmethod
    def set_code():
        return [
            'if not isinstance(value, self.ty):',
            '    raise TypeError(f"Expected {self.ty}")'
        ]

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return [
            'if len(value) > self.maxlen:',
            '    raise ValueError("Too big")'
        ]

class String(Typed):
    ty = str

class SizedString(String, Sized):
    pass

import re

class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return [
            'if not self.pat.match(value):',
            '    raise ValueError("Invalid string")'
        ]

class SizedRegexString(SizedString, Regex):
    pass

class Positive(Descriptor):
    @staticmethod
    def set_code():
        return [
            'if value < 0:',
            '    raise ValueError("Must be >= 0")'
        ]

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

        if fields:
            init_code = _make_init(fields)
            exec(init_code, globals(), clsdict)

        clsobj = super().__new__(cls, name, bases, clsdict)
        return clsobj

class Structure(metaclass=StructMeta):
    _fields = []

class Point(Structure):
    x = Integer()
    y = PositiveInteger()
    name = SizedRegexString(pat='^[A-Z]+$', maxlen=8)

#print(_make_setter(SizedString))

p = Point(1, 2, "ABC")
p.name = "ZZZ"
print(Point.__dict__)
