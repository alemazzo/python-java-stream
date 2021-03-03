

from StreamUtils import StreamUtils


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
        return Stream(StreamUtils.iterate(seed, operator))

    @staticmethod
    def generate(generator):
        return Stream(StreamUtils.generate(generator))

    @staticmethod
    def concat(*streams):
        return Stream(StreamUtils.concat(streams))

    """
    Normal Methods
    """

    def __init__(self, iterable):
        self.__iterable = iterable

    def filter(self, predicate):
        self.__iterable = StreamUtils.filter(self.__iterable, predicate)
        return self

    def map(self, mapper):
        self.__iterable = StreamUtils.map(self.__iterable, mapper)
        return self

    def flatMap(self, flatMapper):
        self.__iterable = StreamUtils.flatMap(self.__iterable, flatMapper)
        return self

    def distinct(self, count):
        self.__iterable = StreamUtils.distinct(self.__iterable, count)
        return self

    def limit(self, count):
        self.__iterable = StreamUtils.limit(self.__iterable, count)
        return self

    def skip(self, count):
        self.__iterable = StreamUtils.skip(self.__iterable, count)
        return self

    def takeWhile(self, predicate):
        self.__iterable = StreamUtils.takeWhile(self.__iterable, predicate)
        return self

    def dropWhile(self, predicate):
        self.__iterable = StreamUtils.dropWhile(self.__iterable, predicate)
        return self

    """
    From here this method mustn't be called on infinite stream
    """

    def sorted(self):
        self.__iterable = sorted(self.__iterable)
        return self

    def peek(self, function):
        self.__iterable = StreamUtils.peek(self.__iterable, function)
        return self

    def forEach(self, function):
        for elem in self.__iterable:
            function(elem)

    def anyMatch(self, predicate):
        for elem in self.__iterable:
            if(predicate(elem)):
                return True
        return False

    def allMatch(self, predicate):
        return all([predicate(elem) for elem in self.__iterable])

    def noneMatch(self, predicate):
        return not self.anyMatch(predicate)

    def findFirst(self):
        for elem in self.__iterable:
            return elem
        return None

    def findAny(self):
        return self.findFirst()

    def reduce(self, identity, accumulator):
        result = identity
        for elem in self.__iterable:
            result = accumulator(result, elem)
        return result

    def min(self):
        return min(self.__iterable)

    def max(self):
        return max(self.__iterable)

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
