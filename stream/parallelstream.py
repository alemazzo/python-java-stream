from itertools import tee
from multiprocessing import Process, Queue, RLock
import multiprocessing as mp
import queue

from threading import Thread, Lock
from time import sleep

from stream.stream import Stream
from stream.util.iterators import IteratorUtils
from stream.util.optional import Optional
from stream.util.threads import StreamThread


class ParallelUtils:

    iterLock = Lock()

    @staticmethod
    def splitted(iterable, pre, offset):
        index = -1
        try:
            while True:
                index += 1
                elem = next(iterable)
                if(index < pre):
                    continue
                if(index % offset == pre):
                    yield elem
        except:
            return

    @staticmethod
    def _iterator(iterable):
        try:
            while True:
                yield next(iterable)
        except:
            return

    @staticmethod
    def sameSplit(iterable, count):
        return [ParallelUtils._iterator(iterable) for _ in range(count)]

    @staticmethod
    def split(iterable, count):
        return [ParallelUtils.splitted(it, index, count) for index, it in enumerate(tee(iterable, count))]

    @ staticmethod
    def finiteSplit(iterable, count):
        elements = list(iterable)
        chunks = [[] for _ in range(count)]
        chunk_size = int(len(elements) / count) + 1

        for index, elem in enumerate(elements):
            chunk = int(index / chunk_size)
            chunks[chunk].append(elem)

        return [Stream(chunk) for chunk in chunks]


class ParallelStream(Stream):

    PROCESS = 8

    def __init__(self, iterable_supplier):
        self.__streams = []
        for i in range(self.PROCESS):
            self.__streams.append(StreamThread(
                Stream(lambda: ParallelUtils.splitted(iterable_supplier(), i, self.PROCESS))))

        for _stream in self.__streams:
            _stream.start()

    def filter(self, predicate):
        '''
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each element as elements are consumed from the resulting stream.

        :param function predicate: predicate to apply to each element to determine if it should be included
        :return: the new stream
        '''
        for _stream in self.__streams:
            _stream.filter(predicate)

        return self

    def map(self, mapper):

        for _stream in self.__streams:
            _stream.map(mapper)

        return self

    def flatMap(self, flatMapper):

        for _stream in self.__streams:
            _stream.flatMap(flatMapper)

        return self

    def distinct(self):

        for _stream in self.__streams:
            _stream.distinct()

        return self

    def peek(self, consumer):

        for _stream in self.__streams:
            _stream.peek(consumer)

        return self

    def forEach(self, function):

        for _stream in self.__streams:
            _stream.forEach(function)

        for _stream in self.__streams:
            _stream.join()

        return self

    def anyMatch(self, predicate):

        for _stream in self.__streams:
            _stream.anyMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult()
                   for _stream in self.__streams]

        return Stream(results).anyMatch(lambda x: x)

    def allMatch(self, predicate):

        for _stream in self.__streams:
            _stream.allMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult()
                   for _stream in self.__streams]

        return Stream(results).allMatch(lambda x: x)

    def noneMatch(self, predicate):

        for _stream in self.__streams:
            _stream.noneMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult()
                   for _stream in self.__streams]

        return Stream(results).allMatch(lambda x: x)

    def findAny(self):

        for _stream in self.__streams:
            _stream.findAny()

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).findAny()

    def reduce(self, accumulator, identity=None):

        for _stream in self.__streams:
            _stream.reduce(accumulator, identity)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).reduce(accumulator, identity)

    def min(self, comparator=None):

        for _stream in self.__streams:
            _stream.min(comparator)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).min(comparator)

    def max(self, comparator=None):

        for _stream in self.__streams:
            _stream.max(comparator)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).max(comparator)

    def sum(self):

        for _stream in self.__streams:
            _stream.sum()

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).sum()

    def count(self):

        for _stream in self.__streams:
            _stream.count()

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult()
                   for _stream in self.__streams if _stream.getResult()]

        res = 0
        for r in results:
            res += r

        return res

    def toList(self):

        for _stream in self.__streams:
            _stream.toList()

        for _stream in self.__streams:
            _stream.join()

        sublists = [_stream.getResult()
                    for _stream in self.__streams]

        results = []
        for sub in sublists:
            results.extend(sub)
        return results

    def toSet(self):

        for _stream in self.__streams:
            _stream.toSet()

        for _stream in self.__streams:
            _stream.join()

        subsets = [_stream.getResult()
                   for _stream in self.__streams]

        results = set()
        for sub in subsets:
            for elem in sub:
                results.add(elem)

        return results

    def get(self):
        return self.__streams

    def terminate(self):
        for _stream in self.__streams:
            _stream.terminate()

    def __eq__(self, other):
        return self.toSet() == set(other)

    def __iter__(self):

        def _iter(iters):
            for it in iters:
                for elem in it:
                    yield elem
            self.terminate()

        return _iter(self.__streams)
