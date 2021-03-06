from threading import Thread
import queue


class StreamThread(Thread):

    def __init__(self, source):
        # Call the Thread class's init function
        Thread.__init__(self)

        self._queue = queue.Queue()
        self._stream = source
        self._result = None
        self._toTerminate = False

    def _addEvent(self, function, *args):
        self._queue.put((function, args))

    # Filter
    def _filter(self, *args):
        self._stream = self._stream.filter(args[0])

    def filter(self, predicate):
        self._addEvent(self._filter, predicate)

    # Map
    def _map(self, *args):
        self._stream = self._stream.map(args[0])

    def map(self, mapper):
        self._addEvent(self._map, mapper)

    # FlatMap
    def _flatMap(self, *args):
        self._stream = self._stream.flatMap(args[0])

    def flatMap(self, flatMapper):
        self._addEvent(self._flatMap, flatMapper)

    # Distinct
    def _distinct(self, *args):
        self._stream = self._stream.distinct()

    def distinct(self):
        self._addEvent(self._distinct, None)

    # Sorted
    def _sorted(self, *args):
        self._stream = self._stream.sorted(args[0])

    def sorted(self, comparator=None):
        self._addEvent(self._sorted, comparator)

    # Peek
    def _peek(self, *args):
        self._stream = self._stream.peek(args[0])

    def peek(self, consumer):
        self._addEvent(self._peek, consumer)

    # ForEach
    def _forEach(self, *args):
        self._stream.forEach(args[0])
        self.terminate()

    def forEach(self, function):
        self._addEvent(self._forEach, function)

    # AnyMatch
    def _anyMatch(self, *args):
        self._result = self._stream.anyMatch(args[0])
        self.terminate()

    def anyMatch(self, predicate):
        self._addEvent(self._anyMatch, predicate)

    # AllMatch
    def _allMatch(self, *args):
        self._result = self._stream.allMatch(args[0])
        self.terminate()

    def allMatch(self, predicate):
        self._addEvent(self._allMatch, predicate)

    # NoneMatch
    def _noneMatch(self, *args):
        self._anyMatch(args[0])
        self._result = not self._result
        self.terminate()

    def noneMatch(self, predicate):
        self._addEvent(self._noneMatch, predicate)

    # Find Any
    def _findAny(self, *args):
        self._result = self._stream.findAny()
        self.terminate()

    def findAny(self):
        self._addEvent(self._findAny, None)

    # Reduce
    def _reduce(self, *args):
        self._result = self._stream.reduce(args[0], args[1])
        self.terminate()

    def reduce(self, accumulator, identity=None):
        self._addEvent(self._reduce, *(accumulator, identity), None)

    # Min
    def _min(self, *args):
        self._result = self._stream.min(args[0])
        self.terminate()

    def min(self, comparator=None):
        self._addEvent(self._min, comparator)

    # Max
    def _max(self, *args):
        self._result = self._stream.max(args[0])
        self.terminate()

    def max(self, comparator=None):
        self._addEvent(self._max, comparator)

    # Sum
    def _sum(self, *args):
        self._result = self._stream.sum()
        self.terminate()

    def sum(self):
        self._addEvent(self._sum, None)

    # Count
    def _count(self, *args):
        self._result = self._stream.count()
        self.terminate()

    def count(self):
        self._addEvent(self._count, None)

    # ToList
    def _toList(self, *args):
        self._result = self._stream.toList()
        self.terminate()

    def toList(self):
        self._addEvent(self._toList, None)

    # ToSet
    def _toSet(self, *args):
        self._result = self._stream.toSet()
        self.terminate()

    def toSet(self):
        self._addEvent(self._toSet, None)

    def run(self):
        while not self._toTerminate:
            func, args = self._queue.get()
            if args:
                func(*args)
            else:
                func()

    def getResult(self):
        return self._result

    def _terminate(self, *args):
        self._toTerminate = True

    def terminate(self):
        self._addEvent(self._terminate, None)

    def __iter__(self):
        return self._stream.__iter__()
