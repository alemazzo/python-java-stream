import math
import random

from .stream import Stream


class NumberStream(Stream):

    @staticmethod
    def integers():
        '''
        Returns an infinite stream of integer from 0 to infinity

        :return: the infinite stream
        '''
        return NumberStream(Stream.iterate(0, lambda i: i + 1))

    @staticmethod
    def odds():
        '''
        Returns an infinite stream of odds number from 0 to infinity

        :return: the infinite stream
        '''
        return NumberStream(Stream.iterate(1, lambda i: i + 2))

    @staticmethod
    def evens():
        '''
        Returns an infinite stream of evens number from 0 to infinity

        :return: the infinite stream
        '''
        return NumberStream(Stream.iterate(0, lambda i: i + 2))

    @staticmethod
    def primes():
        '''
        Returns an infinite stream of primes number from 2 to infinity

        :return: the infinite stream
        '''
        def prime_generator():
            yield 2
            primes = [2]
            actual = 1
            while True:
                actual += 2
                for prime in primes:
                    if actual % prime == 0:
                        break
                else:
                    primes.append(actual)
                    yield actual

        return NumberStream(prime_generator())

    @staticmethod
    def randint(lower, upper):
        '''
        Returns an infinite stream of random integer in range [a, b], including both end points.

        :param int lower: min value for random numbers
        :param int upper: max value for random numbers
        :return: the infinite random stream
        '''
        return NumberStream(Stream.generate(lambda: random.randint(lower, upper)))

    @staticmethod
    def random():
        '''
        Returns an infinite stream of random numbers in range [0, 1], including both end points.

        :param int lower: min value for random numbers
        :param int upper: max value for random numbers
        :return: the infinite random stream
        '''
        return NumberStream(Stream.generate(random.random))

    @staticmethod
    def range(start, end, step=1):
        '''
        Returns a stream of numbers from start to end with specified step.

        :param int start: the start value
        :param int end: the max value
        :param int step: the step
        :return: the new stream
        '''
        return NumberStream(Stream.iterate(start, lambda i: i + step).takeWhile(lambda x: x <= end))

    @staticmethod
    def pi():
        '''
        Returns a stream with the digits of PI.

        :return: the PI's digits stream
        '''
        def pi_digits():
            "Generate n digits of Pi."
            k, a, b, a1, b1 = 2, 4, 1, 12, 4
            while True:
                p, q, k = k * k, 2 * k + 1, k + 1
                a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
                d, d1 = a / b, a1 / b1
                while d == d1:
                    yield int(d)
                    a, a1 = 10 * (a % b), 10 * (a1 % b1)
                    d, d1 = a / b, a1 / b1

        return NumberStream(Stream(pi_digits()))

    def __init__(self, _stream):
        if isinstance(_stream, Stream):
            self.iterable = _stream.iterable
        else:
            self.iterable = _stream

    def average(self):
        '''
        Get the average value of the element of the stream.

        :return: the average value
        '''
        _sum = 0
        _count = 0
        for elem in self:
            _sum += elem
            _count += 1
        return _sum / _count

    def takeWhileSmallerThan(self, maximum):
        return self.takeWhile(lambda x: x < maximum)

    def takeWhileSmallerOrEqualThan(self, maximum):
        return self.takeWhile(lambda x: x <= maximum)

    def takeWhileGreaterThan(self, minimum):
        return self.takeWhile(lambda x: x > minimum)

    def takeWhileGreaterOrEqualThan(self, minimum):
        return self.takeWhile(lambda x: x >= minimum)

    def smallerThan(self, maximum):
        return self.filter(lambda x: x < maximum)

    def smallerOrEqualThan(self, maximum):
        return self.filter(lambda x: x <= maximum)

    def greaterThan(self, minimum):
        return self.filter(lambda x: x > minimum)

    def greaterOrEqualThan(self, minimum):
        return self.filter(lambda x: x >= minimum)

    def multipleOf(self, number):
        return self.filter(lambda x: x % number == 0)

    def square(self):
        return self.pow(2)

    def cube(self):
        return self.pow(3)

    def pow(self, power):
        return self.map(lambda x: x ** power)

    def sqrt(self):
        return self.map(math.sqrt)

    def log(self):
        return self.map(math.log)

    def sin(self):
        return self.map(math.sin)

    def cos(self):
        return self.map(math.cos)
