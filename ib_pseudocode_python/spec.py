"""
Implement the IB Specification
https://computersciencewiki.org/images/c/c6/IB-Pseudocode-rules.pdf
"""

import random
import collections
import inspect
import click

def output(*args, **kwargs):
    """ Convert arguments to strings and print to stdout """
    print("".join([str(a) for a in args]), **kwargs)


class DataAssist:
    def from_file(self, name, obj, attr, convert_ints=True, convert_floats=True):
        func = getattr(obj, attr)
        with open(name) as f:
            for line in [l.strip() for l in f.readlines()]:
                if convert_ints and line.isdigit():
                    func(int(line))
                elif convert_floats and line.count('.') == 1 and line.replace('.', '').isdigit():
                    func(float(line))
                else:
                    func(line)
        return obj

    def from_x_integers(self, obj, attr, num, min=1, max=1000):
        func = getattr(obj, attr)
        for _ in range(num):
            func(random.randint(min, max))
        return obj

    def from_x_characters(self, obj, attr, num, min='A', max='Z'):
        func = getattr(obj, attr)
        for _ in range(num):
            func(chr(random.randint(ord(min), ord(max))))
        return obj

data_assist = DataAssist()


class Array:
    """
    IB Pseudocode list class seems to be the same as Python list, except you can add items
    to the list at any indice (whereas Python requires you to append)
    LIST[0] = 'first item'  # Pseudocode: legal syntax
                            # Python: IndexError
    We compensate by extending the list as it grows
    """

    def __init__(self, list_=None):
        self._list = list_ or []

    def __getitem__(self, index):
        try:
            value = self._list[index]
        except IndexError as err:
            value = None
        return value

    def __setitem__(self, index, value):
        diff = index - len(self._list)
        if diff == 0:
            # trying to set item at end of list, just append
            self._list.append(value)
        elif diff > 0:
            # trying to set item at index further than end of list, create items
            self._list.extend( [None] * (diff + 1) )
        else:
            pass  # nothing needed
        self._list[index] = value

    @classmethod
    def from_list(cls, arr):
        me = cls(arr)
        return me

    @classmethod
    def from_file(cls, name):
        me = cls()
        me._list = data_assist.from_file(name, me._list, 'append')
        return me

    @classmethod
    def from_x_integers(cls, how_many, min=1, max=1000):
        me = cls()
        me._list = data_assist.from_x_integers(me._list, 'append', how_many, min=min, max=max)
        return me

    def __repr__(self):
        return "Array.from_list(" + repr(self._list) + ")"


class Collection:

    def __init__(self, arr=None):
        self._list = arr or []
        self.resetNext()

    def hasNext(self):
        return (self._index + 1) < len(self._list)

    def resetNext(self):
        self._index = -1

    def addItem(self, item):
        self._list.append(item)

    def isEmpty(self):
        return len(self._list) == 0

    def getNext(self):
        self._index += 1
        try:
            value = self._list[self._index]
        except IndexError:
            value = None
        return value

    def __getitem__(self, index):
        return self._list[index]

    @classmethod
    def from_list(cls, arr):
        return cls(arr=arr)

    @classmethod
    def from_file(cls, name):
        me = cls()
        return data_assist.from_file(name, me, 'addItem')

    @classmethod
    def from_x_integers(cls, how_many, min=1, max=1000):
        me = cls()
        return data_assist.from_x_integers(me, 'addItem', how_many, min=min, max=max)

    def __repr__(self):
        return "Collection.from_list(" + repr(self._list) + ")"


class Stack(list):
    """ Stacks are just lists with special methods """
    def push(self, item):
        self.append(item)

    def pop(self):
        """ call super with no arguments """
        return super().pop()

    def isEmpty(self):
        return len(self) == 0

    @classmethod
    def from_list(cls, arr):
        return cls(arr)

    @classmethod
    def from_file(cls, name):
        me = cls()
        return data_assist.from_file(name, me, 'push')

    @classmethod
    def from_x_integers(cls, how_many, min=1, max=1000):
        me = cls()
        return data_assist.from_x_integers(me, 'push', how_many, min=min, max=max)

    def __repr__(self):
        return "Stack.from_list(" + super().__repr__() + ")"


class Queue(collections.deque):
    def enqueue(self, item):
        self.append(item)

    def dequeue(self):
        return self.popleft()

    def isEmpty(self):
        return len(self) == 0

    @classmethod
    def from_list(cls, array):
        return cls(array)

    @classmethod
    def from_file(cls, name):
        me = cls()
        return data_assist.from_file(name, me, 'enqueue')

    @classmethod
    def from_x_integers(cls, how_many, min=1, max=1000):
        me = cls()
        return data_assist.from_x_integers(me, 'enqueue', how_many, min=min, max=max)

    @classmethod
    def from_x_characters(cls, how_many, min='A', max='Z'):
        me = cls()
        return data_assist.from_x_characters(me, 'enqueue', how_many, min=min, max=max)
