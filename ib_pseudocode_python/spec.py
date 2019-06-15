"""
Implement the IB Specification
https://computersciencewiki.org/images/c/c6/IB-Pseudocode-rules.pdf
"""

import random


def output(*args):
    """ Convert arguments to strings and print to stdout """
    print("".join([str(a) for a in args]))


class List:
    """
    IB Pseudocode list class seems to be the same as Python list, except you can add items
    to the list at any indice (whereas Python requires you to append)
    LIST[0] = 'first item'  # Pseudocode: legal syntax
                            # Python: IndexError
    """

    def __init__(self, max=1000):
        self._list = [None] * max
        self._upperboundary = 0

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        if index > self._upperboundary:
            self._upperboundary = index
        self._list[index] = value

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return repr(self._list[:self._upperboundary])


class Collection:

    def __init__(self, arr=[]):
        self._list = arr
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
        return self._list[self._index]

    def __getitem__(self, index):
        return self._list[index]

    @classmethod
    def from_file(cls, path):
        ret = None
        with open(path) as file:
            ret = cls.from_array([l.strip() for l in file if l.strip()])
        return ret

    @classmethod
    def from_array(cls, arr):
        return cls(arr)

    @classmethod
    def from_file(cls, name):
        me = cls()
        with open(name) as f:
            for line in [l.strip() for l in f.readlines()]:
                if line.isdigit():
                    me.addItem(int(line))
                else:
                    me.addItem(line)
        return me

    @classmethod
    def from_x_integers(cls, how_many, min=1, max=1000):
        me = cls()
        for _ in range(how_many):
            me.addItem(random.randint(min, max))
        return me
