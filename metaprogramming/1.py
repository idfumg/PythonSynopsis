################################################################################
# Function arguments
################################################################################

def func(*args, **kwargs):
    return args, kwargs

args = (1, 2)
kwargs = { 'x': 3, 'y': 4 }

assert func(*args, **kwargs) == func(1, 2, x=3, y=4)

################################################################################
# Function arguments as only kewords, not a positional ones
################################################################################

def keywords_only(size, *, block=True):
    pass

keywords_only(8192, block=True)

################################################################################
# Function closures in python
################################################################################

def make_adder(x, y):
    def add():
        return x + y
    return add

adder = make_adder(1, 2)
assert adder() == 3

################################################################################
# Class variables and methods
################################################################################

class Spam:
    a = 1

    def __init__(self, b):
        self.b = b

    def imethod(self):
        pass

    @classmethod
    def cmethod(cls):
        pass

    @staticmethod
    def smethod():
        pass

Spam.a # Class variable
s = Spam(2)
s.b # Instance variable
s.imethod() # Instance method
Spam.cmethod() # Class method
Spam.smethod() # Class static function

################################################################################
# Class inheritance
################################################################################

class Base:
    def spam(self):
        pass

class Foo(Base):
    def spam(self): # Customize Base class method
        r = super().spam() # Call method in Base class

################################################################################
# Every class built on top of dictionary
################################################################################

class MyClass:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def foo(self):
        pass

s = MyClass(1, 2)
assert s.__dict__ == {'x': 1, 'y': 2}
assert callable(MyClass.__dict__['foo'])
