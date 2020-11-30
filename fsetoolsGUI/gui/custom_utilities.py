from PySide2 import QtCore, QtGui


class Validator:
    def __init__(self):
        """Contains a number of QtGui validators using regex for flexibility
        """
        # validator templates
        self.__unsigned_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))
        self.__signed_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\+\-]*[0-9]*\.{0,1}[0-9]*!'))

    @property
    def unsigned_float(self):
        return self.__unsigned_float

    @property
    def signed_float(self):
        return self.__signed_float


class Counter:
    def __init__(self):
        self.__v: int = 0

    def __add__(self, other):
        if isinstance(other, int):
            self.__v = self.__v + other
        elif isinstance(other, Counter):
            self.__v = self.__v + other.__v
        else:
            raise TypeError

    def __repr__(self):
        return f'{self.__v:d}'

    def add(self):
        self.__v += 1

    def reset(self, v: int = 0):
        if isinstance(v, int):
            self.__v = v
        else:
            raise TypeError

    @property
    def count(self):
        self.add()
        return self.__v - 1

    @property
    def value(self):
        return self.__v

    @value.setter
    def value(self, v: int):
        assert isinstance(v, int)
        self.__v = v


if __name__ == '__main__':
    counter = Counter()
    counter.add()
    print(counter)
    counter + 5
    print(counter)
    counter.reset(-1)
    print(counter)
