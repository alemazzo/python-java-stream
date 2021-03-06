from stream import Stream
import random


class BooleanStream(Stream):

    @staticmethod
    def random():
        '''
        Returns an infinite stream of random booleans

        :return: a random boolean stream
        '''
        return BooleanStream(Stream.generate(lambda: random.randint(0, 1) == 1))

    @staticmethod
    def true():
        '''
        Returns an infinite stream of True

        :return: a True boolean stream
        '''
        return BooleanStream(Stream.generate(lambda: True))

    @staticmethod
    def false():
        '''
        Returns an infinite stream of False

        :return: a False boolean stream
        '''
        return BooleanStream(Stream.generate(lambda: False))

    def __init__(self, _stream):
        if isinstance(_stream, Stream):
            self.iterable = _stream.iterable
        else:
            self.iterable = _stream
