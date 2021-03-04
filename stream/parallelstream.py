
from stream import Stream
from stream.iterators import IteratorUtils


class ParallelUtils:

    @staticmethod
    def splitted(iterable, pre, offset):
        for i in range(pre):
            if next(iterable) is None:
                return
        while True:
            elem = next(iterable)
            if elem is None:
                return
            yield elem
            for i in range(offset - 1):
                if next(iterable) is None:
                    return

    @staticmethod
    def split(iterable, count):
        iters = []
        for i in range(count):
            iters.append(ParallelUtils.splitted(iterable, i, count))
        return iters


class ParallelStream(Stream):

    PROCESS = 4

    def __init__(self, iterable):
        self.__iterables = ParallelUtils.split(iterable, self.PROCESS)

    def get(self):
        return self.__iterables[0]
