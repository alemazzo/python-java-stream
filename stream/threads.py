from threading import Thread
import queue


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
        self._result = 0

    def forEach(self, function):
        self._onThread(self._forEach, function)

    # AnyMatch
    def _anyMatch(self, *args):
        self._result = any([args[0](elem) for elem in self._stream])

    def anyMatch(self, predicate):
        self._onThread(self._anyMatch, predicate)

    # AllMatch
    def _allMatch(self, *args):
        self._result = all([args[0](elem) for elem in self._stream])

    def allMatch(self, predicate):
        self._onThread(self._allMatch, predicate)

    # NoneMatch
    def _noneMatch(self, *args):
        self._result = len(
            self._stream.toList()) == 0 or not self._anyMatch(args[0])

    def noneMatch(self, predicate):
        self._onThread(self._noneMatch, predicate)

    # Find Any
    def _findAny(self, *args):
        self._result = self._stream.findAny()

    def findAny(self):
        self._onThread(self._findAny, None)

    # Reduce
    def _reduce(self, *args):
        self._result = self._stream.reduce(args[0], args[1])
        self._terminate = True

    def reduce(self, accumulator, identity=None):
        self._onThread(self._reduce, *(accumulator, identity), None)

    # Min
    def _min(self, *args):
        self._result = self._stream.min(args[0])

    def min(self, comparator=None):
        self._onThread(self._min, comparator)

    # Max
    def _max(self, *args):
        self._result = self._stream.max(args[0])

    def max(self, comparator=None):
        self._onThread(self._max, comparator)

    # Sum
    def _sum(self, *args):
        self._result = self._stream.sum()

    def sum(self):
        self._onThread(self._sum, None)

    # Count
    def _count(self, *args):
        self._result = self._stream.count()

    def count(self):
        self._onThread(self._count, None)

    # ToList
    def _toList(self, *args):
        self._result = self._stream.toList()

    def toList(self):
        self._onThread(self._toList, None)

    # ToSet
    def _toSet(self, *args):
        self._result = self._stream.toSet()

    def toSet(self):
        self._onThread(self._toSet, None)

    def run(self):
        while self._result is None:
            func, args = self._queue.get()
            if args:
                func(*args)
            else:
                func()

    def getResult(self):
        return self._result
