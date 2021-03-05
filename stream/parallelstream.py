from itertools import tee
from multiprocessing import Process, Queue, RLock
import multiprocessing as mp
import queue

from threading import Thread
from time import sleep

from stream.stream import Stream
from stream.iterators import IteratorUtils


class ParallelUtils:

    @staticmethod
    def splitted(iterable, pre, offset):
        for i in range(pre):
            try:
                next(iterable)
            except:
                return
        while True:
            try:
                elem = next(iterable)
                yield elem
            except:
                return

            for i in range(offset - 1):
                try:
                    next(iterable)
                except:
                    return

    @staticmethod
    def _iterator(iterable):
        while True:
            try:
                yield next(iterable)
            except:
                return

    @staticmethod
    def split(iterable, count):
        return [ParallelUtils._iterator(iterable) for i in range(count)]

    @staticmethod
    def finiteSplit(iterable, count):
        elements = list(iterable)
        chunks = [[] for _ in range(count)]
        chunk_size = int(len(elements) / count)

        for index, elem in enumerate(elements):
            chunk = int(index / chunk_size)
            chunks[chunk].append(elem)

        return [Stream(chunk) for chunk in chunks]


class StreamThread(Thread):

    def __init__(self, source):
        # Call the Thread class's init function
        Thread.__init__(self)

        self._queue = queue.Queue()
        self._stream = source
        self._result = None
        self._terminate = False

    def _onThread(self, function, *args):
        self._queue.put((function, args))

    # Filter
    def _filter(self, *args):
        self._stream.filter(args[0])

    def filter(self, predicate):
        self._onThread(self._filter, predicate)

    # Map
    def _map(self, *args):
        self._stream.map(args[0])

    def map(self, mapper):
        self._onThread(self._map, mapper)

    # FlatMap
    def _flatMap(self, *args):
        self._stream.flatMap(args[0])

    def flatMap(self, flatMapper):
        self._onThread(self._flatMap, flatMapper)

    # Distinct
    def _distinct(self, *args):
        self._stream.distinct()

    def distinct(self):
        self._onThread(self._distinct, None)

    # Sorted
    def _sorted(self, *args):
        self._stream.sorted(args[0])

    def sorted(self, comparator=None):
        self._onThread(self._sorted, comparator)

    # Peek
    def _peek(self, *args):
        self._stream.peek(args[0])

    def peek(self, consumer):
        self._onThread(self._peek, consumer)

    # ForEach
    def _forEach(self, *args):
        self._stream.forEach(args[0])

    def forEach(self, function):
        self._onThread(self._forEach, function)

    def _reduce(self, *args):
        self._result = self._stream.reduce(args[0], args[1])
        self._terminate = True

    def reduce(self, accumulator, identity=None):
        self._onThread(self._reduce, *(accumulator, identity), None)

    def run(self):
        while not self._terminate:
            func, args = self._queue.get()
            if args:
                func(*args)
            else:
                func()

    def getResult(self):
        return self._result


class ParallelStream(Stream):

    PROCESS = 8

    def __init__(self, iterable):

        self.__streams = [StreamThread(Stream(iterator))
                          for iterator in ParallelUtils.split(iterable, self.PROCESS)]

        for _stream in self.__streams:
            _stream.start()

    def filter(self, predicate):
        '''
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each element as elements are consumed from the resulting stream.

        :param function predicate: predicate to apply to each element to determine if it should be included
        :return: the new stream
        '''
        for _stream in self.__streams:
            _stream.fi
        return Stream(IteratorUtils.filter(self.__iterable, predicate))

    def map(self, mapper):

        for _stream in self.__streams:
            _stream.map(mapper)

        return self

    def reduce(self, accumulator, identity=None):

        for _stream in self.__streams:
            _stream.reduce(accumulator, identity)

        for _stream in self.__streams:
            _stream.join()

        results = []

        for _stream in self.__streams:
            res = _stream.getResult()
            if res.isPresent():
                results.append(res.get())
        return Stream(results).reduce(accumulator, identity)

    def get(self):
        return self.__streams
