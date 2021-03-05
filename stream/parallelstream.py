from itertools import tee
from multiprocessing import Process, Queue, RLock
import multiprocessing as mp
import queue

from threading import Thread, Lock
from time import sleep

from stream.stream import Stream
from stream.iterators import IteratorUtils
from stream.optional import Optional
from stream.threads import StreamThread


class ParallelUtils:

    iterLock = Lock()

    @staticmethod
    def splitted(iterable, pre, offset):
        index = -1
        try:
            while True:
                index += 1
                with ParallelUtils.iterLock:
                    elem = next(iterable)
                if(index < pre):
                    continue
                if(index % offset == pre):
                    yield elem
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
    def cloneSplit(iterable, count):
        return [ParallelUtils._iterator(iterable) for _ in range(count)]

    @staticmethod
    def split(iterable, count):
        return [ParallelUtils.splitted(it, index, count) for index, it in enumerate(iter(tee(iterable, count)))]

    @staticmethod
    def finiteSplit(iterable, count):
        elements = list(iterable)
        chunks = [[] for _ in range(count)]
        chunk_size = int(len(elements) / count)

        for index, elem in enumerate(elements):
            chunk = int(index / chunk_size)
            chunks[chunk].append(elem)

        return [Stream(chunk) for chunk in chunks]


class ParallelStream(Stream):

    PROCESS = 8

    def __init__(self, iterable):

        self.__streams = [StreamThread(Stream(iterator))
                          for iterator in ParallelUtils.cloneSplit(iterable, self.PROCESS)]

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

        return self

    def anyMatch(self, predicate):

        for _stream in self.__streams:
            _stream.anyMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).anyMatch(lambda x: x)

    def allMatch(self, predicate):

        for _stream in self.__streams:
            _stream.allMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).allMatch(lambda x: x)

    def noneMatch(self, predicate):

        for _stream in self.__streams:
            _stream.noneMatch(predicate)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).noneMatch(lambda x: x)

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

    def sum(self, comparator=None):

        for _stream in self.__streams:
            _stream.sum(comparator)

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        return Stream(results).sum(comparator)

    def count(self):

        for _stream in self.__streams:
            _stream.count()

        for _stream in self.__streams:
            _stream.join()

        results = [_stream.getResult()
                   for _stream in self.__streams if _stream.getResult()]

        return sum(results)

    def toList(self):

        for _stream in self.__streams:
            _stream.toList()

        for _stream in self.__streams:
            _stream.join()

        sublists = [_stream.getResult().get()
                    for _stream in self.__streams if _stream.getResult().isPresent()]

        results = []
        for sub in sublists:
            results.extend(sub)
        return results

    def toSet(self):

        for _stream in self.__streams:
            _stream.toSet()

        for _stream in self.__streams:
            _stream.join()

        subsets = [_stream.getResult().get()
                   for _stream in self.__streams if _stream.getResult().isPresent()]

        results = set()
        for sub in subsets:
            for elem in sub:
                results.add(elem)

        return results

    def get(self):
        return self.__streams
