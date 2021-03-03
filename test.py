import unittest
from stream import Stream


class TestStream(unittest.TestCase):

    def test_empty(self):
        s = Stream.empty()
        self.assertEqual(s.count(), 0)

    def test_of(self):
        s = Stream.of(1, 2, 3)
        self.assertEqual(s.count(), 3)
        self.assertTrue(s.findAny().isPresent())
        self.assertEqual(s.findAny().get(), 1)

    def test_sum(self):
        self.assertTrue(Stream.of(1, 2, 3, 4).sum().isPresent())
        self.assertEqual(Stream.of(1, 2, 3, 4).sum().get(), 10)

    def test_min(self):
        s = Stream.of(1, 2, 5, 4, 3)
        self.assertTrue(s.min().isPresent())
        self.assertEqual(s.min().get(), 1)

    def test_max(self):
        s = Stream.of(1, 2, 5, 4, 3)
        self.assertTrue(s.max().isPresent())
        self.assertEqual(s.max().get(), 5)

    def test_sorted(self):
        s = Stream.of(1, 2, 5, 4, 3)
        self.assertEqual(s.sorted().iterator(), [1, 2, 3, 4, 5])
        self.assertEqual(
            s.sorted(lambda x, y: y - x).iterator(), [5, 4, 3, 2, 1])


if __name__ == '__main__':
    unittest.main()
