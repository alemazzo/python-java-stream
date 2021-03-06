import unittest
from stream import BooleanStream


class TestBooleanStream(unittest.TestCase):

    def test_random(self):
        s = BooleanStream.random().limit(20)
        for elem in s:
            self.assertIn(elem, [True, False])

    def test_true(self):
        s = BooleanStream.true().limit(10)
        for elem in s:
            self.assertTrue(elem)

    def test_false(self):
        s = BooleanStream.false().limit(10)
        for elem in s:
            self.assertFalse(elem)

    def test_filter(self):
        s = BooleanStream.random().limit(20).filter(lambda x: x)
        for elem in s:
            self.assertTrue(elem)
