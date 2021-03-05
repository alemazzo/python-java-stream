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
    def _split(iterable):
        while True:
            try:
                elem = next(iterable)
                yield elem
            except:
                return

    @staticmethod
    def split(iterable, count):
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
        self.lock = RLock()

    def _onThread(self, function, *args, **kwargs):
        self._queue.put((function, args, kwargs))

    def _map(self, *args):
        self._stream.map(args[0])

    def map(self, mapper):
        self._onThread(self._map, mapper, None)

    def _reduce(self, *args):
        self._result = self._stream.reduce(args[0], args[1])
        self._terminate = True

    def reduce(self, accumulator, identity=None):
        self._onThread(self._reduce, *(accumulator, identity), None)

    def run(self):
        while not self._terminate:
            func, args, kwargs = self._queue.get()
            if args:
                if kwargs:
                    func(*args, **kwargs)
                else:
                    func(*args)
            else:
                func()

    def getResult(self):
        return self._result


class ParallelStream(Stream):

    PROCESS = 8

    def __init__(self, iterable):
        self.__streams = [StreamThread(
            _stream) for _stream in ParallelUtils.split(iterable, self.PROCESS)]

        for _stream in self.__streams:
            _stream.start()

    def map(self, mapper):

        for _stream in self.__streams:
            _stream.map(mapper)

        return self

    def reduce(self, accumulator, identity=None):

        for _stream in self.__streams:
            _stream.reduce(accumulator, identity)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get() for _stream in self.__streams]
        return Stream(results).reduce(accumulator, identity)

    def get(self):
        return self.__streams
