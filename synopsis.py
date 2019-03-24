#!/usr/bin/env python

# перебор элементов.
colors = ['red', 'green', 'blue', 'yellow']
for color in colors:
    print(color)


# перебор элементов в обратном порядке.
colors = ['red', 'green', 'blue', 'yellow']
for color in reversed(colors):
    print(color)


# перебор элементов с их номерами.
colors = ['red', 'green', 'blue', 'yellow']
for i, color in enumerate(colors):
    print(i, '-->', color)


# создание списка кортежей симметричных элементов из двух списков.
names = ['raymond', 'rachel', 'matthew']
colors = ['red', 'green', 'blue', 'yellow']
for name, color in zip(names, colors): # list of tuples
    print(name, '-->', color)


# список кортежей, полученных с помощью zip, можно преобразовать в словарь.
names = ['raymond', 'rachel', 'matthew']
colors = ['red', 'green', 'blue']
print(dict(zip(names, colors)))


# сортировка по ключу; ключом может быть любая функция, которую можно применить
# к элементу списка. Вернет новый список.
colors = ['red', 'green', 'blue', 'yellow']
print(sorted(colors, key = len))


# сортировка с помощью метода списка (на месте).
L = [1, 2, 6, 1, 7, 9, 2, 6]
L.sort(key = int)
print(L)


# сортировка с помощью функции (вернет новый).
L = [1, 2, 6, 1, 7, 9, 2, 6]
sorted(L, key = lambda x: int(x))


# сортировка
# itemgetter - это не медленная python функция, а нативная С-шная.
# работает быстрей.
import timeit
import random
from operator import itemgetter

lst = [{ 'id': x, 'name': 'test'+str(x) } for x in range(100)]

def with_key(lst):
    lst.sort(key=lambda x: x['id'])

def with_op(lst):
    lst.sort(key=itemgetter('id'))

random.shuffle(lst)
time1 = timeit.timeit('with_key(lst[:])', setup='from __main__ import with_key, lst', number=1000)
random.shuffle(lst)
time2 = timeit.timeit('with_op(lst[:])', setup='from __main__ import with_op, lst', number=1000)
print(time1)
print(time2)
del lst


# удаление элемента из словаря во время прохода по нему.
d = {'111': 'a', '222': 'b'}
for key in list(d.keys()):
    if key.startswith('2'):
        del d[key]
print(d)


# подсчет одинаковых элементов в списке.
# метод get позволяет вернуть значение по-умолчанию, если нет в словаре.
colors = ['red', 'green', 'red', 'blue', 'green', 'red']
d = {}
for color in colors:
    d[color] = d.get(color, 0) + 1
print(d)


# подсчет одинаковых элементов в списке.
# метод setdefault установит, если надо значение по-умолчанию.
colors = ['red', 'green', 'red', 'blue', 'green', 'red']
d = {}
for color in colors:
    d.setdefault(color, 0)
    d[color] += 1
print(d)


# подсчет одинаковых элементов в списке.
# defaultdict сам устанавливает значение по-умолчанию, если отсутсвует.
from collections import defaultdict
colors = ['red', 'green', 'red', 'blue', 'green', 'red']
d = defaultdict(int)
for color in colors:
    d[color] += 1
print(d)


# группировка элементов по заданному атрибуту.
# получилась универсальная функция. Можно даже подсчитать числа повторяющихся
# элементов, если группировать по значению поля (после просто взять len результата).
# можно искать совпадения по первым буквам.
def group_by(lst, fn):
    d = {}

    for elem in lst:
        key = fn(elem)
        d.setdefault(key, [])
        d[key].append(elem)

    return d

names = ['raymond', 'rachel', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie', 'charlie']
print(group_by(names, len))
print(group_by(names, lambda x: x[0])) # по первой.
print(group_by(names, lambda x: x[0:2])) # по двум первым.
print(group_by(names, lambda x: x)) # чтобы подсчитать.
print('charlies:', len(group_by(names, lambda x: x)['charlie']))


# создание словаря.
dict(a=1, b=2, c=3)
{ 'a': 1, 'b': 2, 'c': 3 }


# вернуть список ключ-значение.
print(dict(a=1, b=2, c=3).items())


# правильный способ узнать, есть ли ключ в словаре.
d = { '1': 'a', '2': 'b' }
if '1' in d:
    print('1 in d')


# возвращает новый подкласс кортежа с именованными полями.
# может удобно использоваться как структура в c/c++.
from collections import namedtuple
Point = namedtuple('Point', 'x, y')
print(Point.__doc__)
p = Point(11, y = 2)
print(p)
x, y = p
d = p._asdict()
point = Point(x = 22, y = 2)
point = point._replace(x=100)


# читаем scv и подсчитываем сумму значений quantity (количество).
# f = open('filename.scv')
# field_names = f.readline().strip().split(',')
# records = [dict(zip(field_names, line.strip().split(','))) for line in f]
# print(records)
# print(sum(int(record['quantity']) for record in records))


# получить имя файла и расширение правильным путем (os.path).
import os
(name, ext) = os.path.splitext('filename.scv')
print(name, ext)


# конкатенация элементов пути в фс правильным путем.
import os
print(os.path.join('/', '/home'))


# возможности оператора for ... in ... else.
res = [x**2 for x in range (1, 25, 2) if x % 3 != 0]
print(res)


# сохраняет память.
total = sum(i * i for i in range(1, 101))


# объявление класса с property. 1 способ.
class Foo(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, x):
        self._x = x

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")


# объявление класса с property. 2 способ. более явный.
class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


# Разбивание текста на несколько строк.
"""Triple
double
quotes"""


# Разбивание текста на несколько строк.
'''\
Triple
double
quotes\
'''


# Разбивание текста на несколько строк. предпочтительный вариант.
('Long strings can be made up '
 'of several shorter strings.')


# обмен значениями между двумя переменными с помощью распаковки.
# в данном случае будет создан кортеж.
a, b = 1, 2
a, b = b, a


# join более эффективная операция для конкатенации строк, чем +/+=.
# судя по всему, из-за перераспределении памяти при +/+=.
colors = ['red', 'blue', 'green', 'yellow']
print(' '.join(color.upper() for color in colors))


# функция len вызывает метод __len__, определенный в классе.
class MyContainer(object):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

my_container = MyContainer([1, 2, 3])
print(len(my_container))


# приведение типа к bool осуществляется благодаря __bool__.
# __nonzero__ - deprecated.
class MyContainer(object):
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return bool(self.value)

    __nonzero__ = __bool__

my_container = MyContainer(1)
if my_container:
    print('my_container is non zero')


# выдает все определенные локальные переменные модуля или функции (текущий словарь).
locals()


# печатает в удобном виде объекты python.
from pprint import pprint
#pprint(locals())


# проверка, принадлежит ли объект данному классу.
print(isinstance('asd', str))


# При ошибке в работе с типами кидается TypeError.
try:
    print(str(MyContainer()))
except TypeError as e:
    print("print(str(x)) type error: " + str(e))


# встроенный счетчик для итерируемого объекта.
from collections import Counter
print(Counter("asdqweasd")['a'])
print(Counter([1, 2, 3, 2, 2])[2])


# подобный сишному тернарный оператор.
y = 1
x = 3 if y == 1 else 2
print(x)


# операция скобочки реализуется с помощью __getitem__.
# с помощью Ellipsis можно узнать если передали в скобочках '...'.
class MyClass(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __getitem__(self, item):
        if item is Ellipsis:
            return [self.a, self.b]
        else:
            return getattr(self, item)

x = MyClass('asdqwe213', 12354)
print(x['a'])
print(x[...])


# python использует замыкание. запоминает значение локальных переменных.
def get_adder(x):
    def adder(y):
        return x + y

    return adder

adder = get_adder(1)
print(adder(2))


# конструкция with, для чтения файла построчно и закрытия его.
# with open("hello.txt") as hello_file:
#     for line in hello_file:
#         print line


# конструкция with, для чтения страницы построчно и закрытия его.
# with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
#     for line in front_page:
#         print line


# встроенное средство проверки на вхождение в интервал.
print(1 < 5 < 10)


# средство для выравнивания строк по заданному количеству символов.
import textwrap
s = "Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs."
print(textwrap.fill(s, 60))


# применяется для свертывания списка с помощью выбранной функции.
from functools import *
lst = [1, 2, 3, 4, 5]
print(reduce(lambda x, y: x * y, lst, 2))


# получение копии списка или частей списка с помощью среза.
s = [1, 2, 3, 4, 5, 6]
print(s[:]) # list copy
print(s[1:]) # all without first
print(s[-3:]) # last three
print(s[2:-2]) # without first two and last two
print(s[::2]) # odd elements
print(s[1::2]) # even elements
print('Hello, Dolly!'[::-1]) # reverse string


# удаление части списка.
s = [1, 2, 3, 4, 5, 6]
del s[2:-2]
print(s)


# вставка в тело списка.
s = [1, 2, 3, 4, 5, 6]
s[2:-2] = [9, 9, 9, 9]
print(s)


# вставка в начало списка.
s = [1, 2, 3, 4, 5, 6]
s[0:0] = [0, 0, 0]
assert s == [0, 0, 0, 1, 2, 3, 4, 5, 6]


# метод __new__ создает сам объект.
# метод __init__ его инициализирует.
# объект, созданный в __new__, затем передается методу __init__ (self).
class A(object):
    def __new__(klass):
        print('__new__: klass =', klass)
        obj = super(A, klass).__new__(klass)
        print('__new__: created object: {}'.format(obj))
        return obj

    def __init__(self):
        print('__init__: initiating object: {}'.format(self))
A()


# реализация singleton с помощью метода __new__.
# при создании объекта Singleton, пройдет проверка на то,
# создан ли уже в классе объект. Если нет, то с помощью
# super & __new__ он создается и сохраняется.
# т.о. всегда будет возвращен один и тот же объект.
# данное поведение будет распространяться и на классы, которые
# наследуются от данного класса - они будут возвращать все
# тот же объект 'Singleton.instance'.
class Singleton(object):

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls)

        return cls.instance

assert Singleton() is Singleton()
Singleton().x = 1

x = Singleton()
y = Singleton()

assert x is y
assert x.x == y.x

x.x = 2

assert x is y
assert x.x == y.x

assert isinstance(x, Singleton)
assert isinstance(y, Singleton)

class M(Singleton):
    pass

assert M() is M()
assert M() is x
assert M() is y


# Другой тип singleton'а.
# В данном случае объявляется метакласс.
# При объявлении пользовательского класса, при указании на метакласс,
# он будет использоваться для порождения новых объектов нового класса.
# В итоге, в каждом новом классе, при его объявлении, будет
# немедленно создан объект instance - для каждого свой.
class SingletonMeta(type):

    def __init__(cls, *args, **kw):
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(SingletonMeta, cls).__call__(*args, **kw)

        return cls.instance

C = SingletonMeta('C', (object,), {})
D = SingletonMeta('D', (object,), {})

assert C is not D
assert C() is not D()
assert C() is C()
assert D() is D()

class E(metaclass = SingletonMeta):
    def __init__(self):
        pass

assert C is not E
assert D is not E
assert C() is not E()
assert E() is E()


# type - это просто класс, экземплярами которого являются другие
# классы (метакласс). А сами классы можно считать расширением простых,
# обычных объектов.
# Поведение object - создавать обычные объекты.
# Поведение type - создавать классы (метакласс).
# Чтобы просто определить класс необходимо наледовать его от object.
# Чтобы определить метакласс - наследуем его от type.

# metaclasses
# XClass = XMetaClass(name, bases, attrs)
# Тогда, сразу после создания
# XClass.__name__ равно name,
# XClass.__bases__ равен bases,
# XClass.__dict__ равен attrs, а
# XClass.__class__ равен XMetaClass


# создание класса А.
class A(object):
    pass


# создание класса А с помощью метакласса type.
# Имя его будет А.
# Базовым классом у него будет object.
# Его словарь будет пустым.
print(type('A', (object,), {}))


# создание класса B.
class B(A):
    def foo(self):
        return 42


# создание класса B с помощью метакласса type.
print(type('B', (A,), {'foo': lambda self: 42}))

# создание объекта класса B с помощью метакласса type.
# обратить внимание на скобочки.
b = type('B', (A,), {'foo': lambda self: 42})()
print(b.foo())


# определение метакласса.
# Это равносильно:
# A = type('A', (type,), {})
# A стал метаклассом, предназначенным для создания других классов.
# Производные классы, также будут наследовать и его __dict__ (say).
# self - not an instance of class, but class object itself.
class A(type):
    def say(self):
        print('SAY SAY SAY')

BB = A('BB', (object,), {})
BB.say()

print('A.__bases__ = ', A.__bases__)
print('BB.__dict__ = ', BB.__dict__)

assert isinstance(object, object)
assert isinstance(type, object)
assert isinstance(object, type)

assert isinstance(BB, object)
assert isinstance(BB, type)
assert isinstance(A, object)
assert isinstance(A, type)

assert not isinstance(int(1), type)
assert isinstance(int, type)
assert isinstance(int(1), object)
assert isinstance(int(1), int)

assert issubclass(type, object)
assert not issubclass(object, type)
assert issubclass(A, type)
assert not issubclass(BB, type)


# Все, что определяется в метаклассе, доступно для класса, но не
# доступно для экземпляров класса - обычных объектов, т.к. поиск
# атрибутов в обычном объекте ведется только по __dict__
# словарям класса.

class Meta(type):
    pass

Meta('A', (object,), {})

# В начале метакласс Meta ищет метод __new__ у себя в словаре __dict__,
# не находит его там и начинает искать в __dict__ своих
# родительских классов (т.е. метаклассах, в данном случае type), т.е.
# происходит обычный поиск атрибута в классе.
# В результате исполнения __new__ с соответствующими параметрами
# получает новый класс, который потом инициализируется вызовом __init__
# метода метакласса.

# В развернутом виде:
cls = type.__dict__['__new__'](Meta, 'A', (object,), {})
type.__dict__['__init__'](cls, 'A', (object,), {})

# Или с помощью super:
cls = super(Meta, Meta).__new__(Meta, 'A', (object,), {})
super(Meta, Meta).__init__(cls, 'A', (object,), {})


# Создание абстрактного класса.
# Использование метаклассов хорошо тем, что при создании абстрактного
# класса, выкинется исключение (а не при вызове метода).

from abc import ABCMeta, abstractmethod, abstractproperty

class Movable(metaclass = ABCMeta):

#    __metaclass__ = ABCMeta

    @abstractmethod
    def move():
        """Move object"""

    @abstractproperty
    def speed():
        """Object speed"""


class Car(Movable):
    def __init__(self):
        self._speed = 10
        self.x = 0

    def move(self):
        print('car moving')

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @speed.deleter
    def speed(self):
        del self._speed


try:
    m = Movable()
except TypeError as e:
    assert(e)

assert issubclass(Car, Movable)
assert isinstance(Car(), Movable)
assert isinstance(Car(), Car)
assert isinstance(Car, object)
assert isinstance(Car, type)

car = Car()
assert car.speed == 10
car.speed = 20
assert car.speed == 20
del car.speed


# читаем порциями из файла.
from functools import partial
RECORD_SIZE = 32
with open('synopsis.py', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for record in records:
        pass

# mmap
size = 1000000
with open('data', 'wb') as f:
    f.seek(size - 1)
    f.write(b'\x00')

import mmap
def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

m = memory_map('data')
print(len(m))
print(m[0:10])
print(m[0])
m.close()
print(m.closed)

# zip file.
import zipfile
file = zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED)
file.write("synopsis.py")
file.close()

# unzip file.
import zipfile
with zipfile.ZipFile("archive.zip", "r") as zfile:
    for filename in zfile.namelist():
        with open(filename, "w+b") as file:
            file.write(zfile.read(filename))

# list files in dir
files = []
for name in os.listdir('.'):
    files.append(os.path.join('./', name))

# walk by folders and files.
import os
for root, dirs, files in os.walk('.'):
    pass

# expand relation path
os.path.expanduser("~")

# using unix mask filenames
import glob
for filename in glob.glob(r"*.*"):
    print(filename)

# get total file sizes
from operator import add
files = ["/etc/group", "/etc/passwd", "synopsis.py"]
print(reduce(add, map(os.path.getsize,
                      filter(lambda x: x.endswith(".py"), files)), 0))


# Coroutines
# Выполняются совместно в одном потоке.
# Выполнение может прерываться в ожидании какого-либо события.
# Выполнение может возобновиться после получения ожидаемого события.
# Может вернуть результат по завершению.
# Не подходит для задач, которые производят долгие расчеты.
# Подходит для I/O: сетевой сервер, пользовательский интерфейс и т.д.
from functools import wraps
def coroutine(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None) # initialize generator
        return gen

    return wrap

@coroutine
def calc():
    history = []

    while True:
        x, y = (yield)

        if x == 'h':
            print(history)
            continue
        else:
            result = x + y
            print(result)
            history.append(result)

c = calc()
c.send((1, 2))
c.send((4, 12))
c.send(('h', 0))
c.close()



# Descriptors.

# Применяется для создания свойства.
# Позволяет контролировать доступ к атрибутам экземпляра класса.
class Descriptor(object):

    def __get__(self, obj, objtype):
        print('getter used')

    def __set__(self, obj, value):
        print('setter used')

    def __delete__(self, obj):
        print('deleter used')


class MyClass(object):

    prop = Descriptor()


# Точно такое же поведение можно реализовать через property.
# Захламляет класс, но не надо определять дополнительный класс.
# Если свойств много, класс будет содержать множество похожих методов.
# Удобнее определить дескриптор, когда возникнет необходимость
# в контроле поведения атрибута.
class MyClass(object):

    def _getter(self):
        print('getter used')

    def _setter(self, value):
        print('setter used')

    def _deleter(self):
        print('deleter used')

    prop = property(_getter, _setter, _deleter, 'doc string')


# К встроенным дескрипторам также относится staticmethod.
# Это то же, что функция вне класса, в нее не передается экземпляр.
# Хорошими кандидатами для статических методов являются методы,
# которым не нужна ссылка на self, самостоятельным методам.

# К встроенным дескрипторам также относится classmethod.
# Это то же, что и метод класса, только в качестве первого аргумента
# передается класс экземпляра.
# Это поведение удобно, когда методу всегда нужна ссылка на класс,
# и ей не нужны данные класса.
# Один из способов использования - создание альтернативных конструкторов
# (dict.fromkeys('abracadabra')).
# Этот classmethod знает, какого типа объект создать.
class StaticAndClassMethodHolder(object):

    def _method(*args):
        print('_method called with ', *args)

    static = staticmethod(_method)
    cls = classmethod(_method)

s = StaticAndClassMethodHolder()
s._method()
s.static()
s.cls()


# Можно задать жестко, какие атрибуты может иметь класс с помощью
# __slots__.
# При его использовании также не будет создан __dict__.
# Это может уменьшить количество используемой памяти при создании
# множества небольших объектов.
# Также, это защищает экземпляр класса от случайного создания в нем
# незапланированных атрибутов (опечатка).
class Slotter(object):
    __slots__ = ['a', 'b']

s = Slotter()
s.a = 1
s.b = 1
try:
    s.c = 1
except AttributeError:
    pass


# Переопределение __getattribute__ может прекратить автоматический
# вызов дескрипторов.
# Необходимо для того, чтобы отловить обращение к атрибутам объекта.


# Реализация встроенного property. Только судя по всему, необходима подмена имени.
class Property(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if self.fget is None:
            raise AttributeError("nonread attribute")

        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("nonset attribute")

        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("nondel attribute")

        self.fdel(obj)

    def setter(self, setter_):
        self.fset = setter_

        return self.fset

    def deleter(self, deleter_):
        self.fdel = deleter_

        return self.fdel

# Реализация с помощью протокола дескриптора не данных staticmethod.
# Дескрипторы не данных могут перезаписаться вручную в программе.
# Дескрипторы данных имеют больший приоритет и их перезаписать так нельзя.
# Поскольку статический метод является дескриптором, то он не является
# аналогом статического метода в c++/java и будет работать намного
# медленней. В таком ракурсе лучше использовать функцию.
class StaticMethod(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, klass=None):
        return self.f(obj)

# Реализация с помощью протокола дескриптора не данных classmethod.
class ClassMethod(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)

        def newfunc(*args):
            return self.f(klass, *args)

        return newfunc


# Context managers

# Чтобы класс стал контекстым менеджером, необходимо включить в него два
# метода: __enter__ и __exit__.
# Возврат текущего экземпляра класса self необходимо для того, чтобы
# к объекту можно было обратиться через конструкцию as.
# Если было исключение, то его можно падавить, вернув True.

class Foo(object):
    def __enter__(self):
        print('Enter to a block')
        return self

    def __exit__(self, exp_type, exp_value, exp_tr):
        if exp_type is IOError:
            return True
        print('Leave from a block')

    def __del__(self):
        print('Destructor')

    def say(self):
        print('say say ^_)')

with Foo() as foo:
    print('Inside the block')
    foo.say()


# Используя декоратор contextmanager(), можно из обычной функции
# сделать контекстный менеджер.

import contextlib

@contextlib.contextmanager
def context():
    print('Enter block')
    try:
        yield "hahahahhahahahahha"
    except RuntimeError as err:
        print('Error:', err)
    finally:
        print('Exit block')

with context() as fp:
    print('Block section', fp)

@contextlib.contextmanager
def bold_text():
    print('<b>')
    yield
    print('</b>')

with bold_text():
    print('Hello, world!')

@contextlib.contextmanager
def context(name):
    print('Enter context', name)
    yield name
    print('Leave context', name)

with context('first') as first, context('second') as second:
    print('In block: {} {}'.format(first, second))



# Позволяет избежать считывания всего файла целиком, сохраняя память.
def read_file_line_by_line(filename):
    with open(filename, 'r') as fd:
        for line in fd:
            yield line


# Интераторы - специальные объекты, предоставляющие последовательный
# доступ к данным из контейнера. Немаловажную роль играет то, что
# память фактически не тратится, т.к. промежуточные данные выдаются по
# мере необходимости при запросе.

from itertools import chain
from itertools import takewhile
from itertools import dropwhile

testIt = iter([1, 2, 3, 4, 5])
print([x for x in testIt])

def getSimple(state=[]):
    print(state.__sizeof__())
    if len(state) < 4:
        state.append(' ')
        return ' '
    return None

testIt2 = iter(getSimple, None)
print([x for x in testIt2])

it1 = iter([1, 2, 3])
it2 = iter([4, 5, 6])
for i in chain(it1, it2):
    print(i)

print()

print('takewhile')
for i in takewhile(lambda x: x > 0, [1, -2, -3, -4, 5]):
    print(i)

print()

print('dropwhile')
for i in dropwhile(lambda x: x > 0, [1, -2, -3, -4, 5]):
    print(i)

print()

[print(i) for i in [1, -2, -3, -4, 5] if i > 0]

print()

# Использование итераторов для генерации чисел фибоначчи.
class Fibonacci(object):

    def __init__(self, N):
        self.a = 0
        self.b = 1
        self.n = N

    def __iter__(self):
        return self

    def __next__(self): # next(self) in python2.
        if self.a < self.n:
            a = self.a
            self.a, self.b = self.b, a + self.b

            return a
        else:
            raise StopIteration

for i in Fibonacci(100):
    print(i)

print()

# Использование генератора для генерации чисел фибоначчи.
def Fibonacci(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

for i in Fibonacci(100):
    print(i)



# Memoization - свойство функций сохранять (кэшировать) результаты
# вычислений.
# Позволяет достичь прироста скорости работы за счет памяти.

import pickle

def memoized(fn):
    memory = {}

    def memo(*args, **kwargs):
        hash = pickle.dumps((args, sorted(kwargs.iteritems())))
        if hash not in memory:
            memory[hash] = fn(*args, **kwargs)
        return memory[hash]

    return memo








# remove temporary created data
import os
os.remove('archive.zip')
os.remove('data')




# it is are hits only for type checkers
from typing import List

def greeting(names: List[str]) -> str:
    return "";
    # return 'Hello, {}'.format(', '.join(names))

greeting(['jane', 'john', 'judy'])
