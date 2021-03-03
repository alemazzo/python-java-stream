from IteratorUtils import IteratorUtils
from functools import cmp_to_key
from Optional import Optional


class Stream():

    """
    Python Stream Class
    """

    """
    Static Methods
    """

    @staticmethod
    def empty():
        return Stream([])

    @staticmethod
    def of(elem):
        return Stream([elem])

    @staticmethod
    def of(*elements):
        return Stream(list(elements))

    @staticmethod
    def ofNullable(elem):
        return Stream.of(elem) if elem is not None else Stream.empty()

    @staticmethod
    def iterate(seed, operator):
        return Stream(IteratorUtils.iterate(seed, operator))

    @staticmethod
    def generate(generator):
        return Stream(IteratorUtils.generate(generator))

    @staticmethod
    def concat(*streams):
        return Stream(IteratorUtils.concat(streams))

    """
    Normal Methods
    """

    def __init__(self, iterable):
        self.__iterable = iterable

    def filter(self, predicate):
        self.__iterable = IteratorUtils.filter(self.__iterable, predicate)
        return self

    def map(self, mapper):
        self.__iterable = IteratorUtils.map(self.__iterable, mapper)
        return self

    def flatMap(self, flatMapper):
        self.__iterable = IteratorUtils.flatMap(self.__iterable, flatMapper)
        return self

    def distinct(self, count):
        self.__iterable = IteratorUtils.distinct(self.__iterable, count)
        return self

    def limit(self, count):
        self.__iterable = IteratorUtils.limit(self.__iterable, count)
        return self

    def skip(self, count):
        self.__iterable = IteratorUtils.skip(self.__iterable, count)
        return self

    def takeWhile(self, predicate):
        self.__iterable = IteratorUtils.takeWhile(self.__iterable, predicate)
        return self

    def dropWhile(self, predicate):
        self.__iterable = IteratorUtils.dropWhile(self.__iterable, predicate)
        return self

    """
    From here this method mustn't be called on infinite stream
    """

    def sorted(self, comparator=None):
        self.__iterable = sorted(
            self.__iterable, key=cmp_to_key(comparator)) if comparator else sorted(self.__iterable)
        return self

    def peek(self, function):
        self.__iterable = IteratorUtils.peek(self.__iterable, function)
        return self

    def forEach(self, function):
        for elem in self.__iterable:
            function(elem)

    def anyMatch(self, predicate):
        return any([predicate(elem) for elem in self.__iterable])

    def allMatch(self, predicate):
        return all([predicate(elem) for elem in self.__iterable])

    def noneMatch(self, predicate):
        return not self.anyMatch(predicate)

    def findFirst(self):
        for elem in self.__iterable:
            return Optional.of(elem)
        return Optional.ofNullable(None)

    def findAny(self):
        return self.findFirst()

    def reduce(self, accumulator, identity=None):
        result = identity
        for elem in self.__iterable:
            if(result is None):
                result = elem
            else:
                result = accumulator(result, elem)
        return Optional.ofNullable(result)

    def min(self):
        return Optional.ofNullable(min(self.__iterable))

    def max(self):
        return Optional.ofNullable(max(self.__iterable))

    def count(self):
        return len(self.__iterable)

    def toList(self):
        return list(self.__iterable)

    def toSet(self):
        return set(self.__iterable)

    def iterator(self):
        return self.__iterable


def stream(iterable):
    return Stream(iterable)
