import unittest
from stream import BooleanStream


class TestBooleanStream(unittest.TestCase):

    def test_true(self):
        s = BooleanStream.true().limit(10)
        for elem in s:
            self.assertTrue(elem)

    def test_false(self):
        s = BooleanStream.false().limit(10)
        for elem in s:
            self.assertFalse(elem)
