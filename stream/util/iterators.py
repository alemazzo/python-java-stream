
class IteratorUtils:

    """
    Iterator Utils
    """

    """
    Methods for Static Method of Stream
    """
    @staticmethod
    def iterate(seed, operator):
        while(True):
            yield seed
            seed = operator(seed)

    @staticmethod
    def generate(generator):
        while(True):
            yield generator()

    @staticmethod
    def concat(*iterables):
        for iterable in iterables:
            for elem in iterable:
                yield elem

    """
    Methods for Normal Method of Stream
    """
    @staticmethod
    def filter(iterable, predicate):
        for elem in iterable:
            if(predicate(elem)):
                yield elem

    @staticmethod
    def map(iterable, mapper):
        for elem in iterable:
            yield mapper(elem)

    @staticmethod
    def flatMap(iterable, mapper):
        for elem in iterable:
            for internal in mapper(elem):
                yield internal

    @staticmethod
    def distinct(iterable):
        elements = set()
        for elem in iterable:
            if elem not in elements:
                elements.add(elem)
                yield elem

    @staticmethod
    def peek(iterable, function):
        for elem in iterable:
            function(elem)
            yield elem

    @staticmethod
    def takeWhile(iterable, predicate):
        for elem in iterable:
            if(predicate(elem)):
                yield elem
            else:
                break

    @staticmethod
    def dropWhile(iterable, predicate):
        toDrop = True
        for elem in iterable:
            if(not predicate(elem) and toDrop):
                toDrop = False
            if(not toDrop):
                yield elem

    @staticmethod
    def skip(iterable, count):
        index = 0
        for elem in iterable:
            index += 1
            if(index > count):
                yield elem

    @staticmethod
    def limit(iterable, count):
        index = 0
        for elem in iterable:
            index += 1
            if(index <= count):
                yield elem
            else:
                break
