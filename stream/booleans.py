from .stream import Stream
import random


class BooleanStream(Stream):

    @staticmethod
    def booleans():
        return BooleanStream(Stream.generate(lambda: random.randint(0, 1) == 1))

    def __init__(self, _stream):
        if isinstance(_stream, Stream):
            self.iterable = _stream.__iterable
        else:
            self.iterable = _stream
