#!/usr/bin/env python

"""
STRONG TYPES ON PYTHON

Нужно, чтобы созданный объект оставался постоянным.
Чтобы нельзя было состояние объекта.
Вместо этого, необходимо создать новый объект на основе текущего.
Это сократит количество кода, которое способно изменять объект.
Также необходимо сделать __slots__ - невозможность добавлять
новые атрибуты объекту, кроме одного - __value.
Может быть стоит отказаться от getInt/getStr? Данные ошибки
всплывут при использовании сразу же и не смогут существовать
неявно.

(name1 = Name('123qwe')
 name2 = Name(name1))


>>> Year = VALID_INT("Year", 0, 9999)
>>> year = Year(2014)
>>> year.getInt()
2014
>>> str(year.getInt())
'2014'
>>> year = Year('2014')
Traceback (most recent call last):
...
ValidatorException: class Year: '2014' is not an int


>>> Name = VALID_STRING("Name", regex = re.compile(r"^[a-zA-Z]{0,5}$"))
>>> name = Name("Artem")
>>> name.getStr()
'Artem'
>>> name = Name("asasdasdasdasd")
Traceback (most recent call last):
...
ValidatorException: class Name: wrong value 'asasdasdasdasd'
>>> name.__value = 'asdasd'


>>> IsRequest = VALID_BOOL("IsRequest")
>>> isRequest = IsRequest(True)
>>> bool(isRequest)
True
>>> isRequest.getInt()
1
>>> isRequest = IsRequest(False)
>>> bool(isRequest)
False
>>> isRequest.getInt()
0
>>> isRequest = IsRequest(1)
>>> isRequest.getInt()
1
>>> bool(isRequest)
True


>>> stockItem = StockItem("dasd", 5, "Hardware")
>>> stockItem = StockItem("dasd", 6, "Hardware")
Traceback (most recent call last):
...
ValidatorException: class StockItem: 'number' cannot be set to '6'
>>> stockItem = StockItem("dasd", 5, "asds")
Traceback (most recent call last):
...
ValidatorException: class StockItem: 'category' cannot be set to 'asds'
"""

import re

class ValidatorException(Exception):
    def __init__(self, instance, value):
        super().__init__("class " + instance.__class__.__name__ + ": " + value)

################################################################################
# STRONG CLASSES
################################################################################

def VALID_INT(name, minimum, maximum):
    class BaseClass:
        def __init__(self, value):
            if not isinstance(value, int):
                raise ValidatorException(self, "'{0}' is not an int".format(value))
            assert minimum <= value <= maximum, "{0} <= {1} <= {3}".format(minimum, value, maximum)
            self.__value = value

        def getInt(self):
            return self.__value

    return type(name, (BaseClass,), {})

def VALID_STRING(name, empty_allowed = True, regex = None, acceptable = None):
    class BaseClass:
        def __init__(self, value):
            if not isinstance(value, str):
                raise ValidatorException(self, "'{0}' is not an str".format(value))
            if not empty_allowed and not value:
                raise ValidatorException(self, "'{0}' may not be empty".format(value))
            if ((acceptable is not None and value not in acceptable) or
                (regex is not None and not regex.match(value))):
                raise ValidatorException(self, "wrong value '{0}'".format(value))
            self.__value = value

        def getStr(self):
            return self.__value

    return type(name, (BaseClass,), {})

def VALID_BOOL(name):
    class BaseClass:
        def __init__(self, value):
            if value is None or (value not in [0, 1] and not isinstance(value, bool)):
                raise ValidatorException(self, "wrong value: {0}".format(value))
            self.__value = bool(value)

        def __bool__(self):
            return self.__value

        def getInt(self):
            return int(self.__value)
    return type(name, (BaseClass,), {})


################################################################################
# CLASS STRONG DECORATORS
################################################################################

class GenericDescriptor:
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def __get__(self, instance, owner = None):
        if instance is None:
            return self
        return self.getter(instance)

    def __set__(self, instance, value):
        return self.setter(instance, value)

def VALID_CLS_STRING(attr_name, empty_allowed = True, regex = None, acceptable = None):
    def decorator(cls):
        name = "__" + attr_name

        def getter(self):
            return getattr(self, name)

        def setter(self, value):
            assert isinstance(value, str), ("'" + attr_name + "' must be a string")
            if not empty_allowed and not value:
                raise ValidatorException(self, "'{0}' may not be empty".format(attr_name))
            if ((acceptable is not None and value not in acceptable) or
                (regex is not None and not regex.match(value))):
                raise ValidatorException(self, "'{0}' cannot be set to '{1}'".format(attr_name, value))
            setattr(self, name, value)

        setattr(cls, attr_name, GenericDescriptor(getter, setter))
        return cls
    return decorator

def VALID_CLS_NUMBER(attr_name, minimum, maximum):
    def decorator(cls):
        name = "__" + attr_name

        def getter(self):
            return getattr(self, name)

        def setter(self, value):
            assert isinstance(value, int), ("'" + attr_name + "' must be a number")
            if not minimum <= value <= maximum:
                raise ValidatorException(self, "'{0}' cannot be set to '{1}'".format(attr_name, value))
            setattr(self, name, value)

        setattr(cls, attr_name, GenericDescriptor(getter, setter))
        return cls
    return decorator

@VALID_CLS_STRING("name", empty_allowed = False)
@VALID_CLS_NUMBER("number", minimum = 1, maximum = 5)
@VALID_CLS_STRING("category", empty_allowed = False, acceptable = ("Hardware", "Media"))
class StockItem:
    def __init__(self, name, number, category):
        self.name = name
        self.number = number
        self.category = category

if __name__ == "__main__":
    import doctest
    doctest.testmod()
