import unittest
from stream import Stream


class TestStream(unittest.TestCase):

    def test_empty(self):
        s = Stream.empty().parallel()
        self.assertEqual(s.count(), 0)

    def test_of(self):

        s = Stream.of(1, 2, 3, 4, 5, 6, 7, 8).parallel()

        self.assertEqual(s.count(), 8)
        self.assertTrue(s.findAny().isPresent())
        self.assertEqual(s.findAny().get(), 1)

        self.assertEqual(Stream.ofNullable(None).parallel(),
                         Stream.empty().parallel())

        self.assertEqual(Stream.of().parallel(), Stream.empty().parallel())

    def test_iterate(self):
        index = 0
        s = Stream.iterate(index, lambda i: i + 1)

        for elem in s:
            self.assertEqual(elem, index)
            index += 1
            if index == 10:
                break

    def test_generate(self):
        index = 0
        s = Stream.generate(lambda: 1)

        for elem in s:
            self.assertEqual(elem, 1)
            index += 1
            if index == 10:
                break

    def test_concat(self):
        s = Stream.concat(Stream.of(1, 2, 3), Stream.of(
            4, 5, 6)).toList()
        self.assertEqual(s, [1, 2, 3, 4, 5, 6])

    def test_filter(self):
        s = Stream.of(1, 2, 3, 4).filter(lambda x: x % 2 == 0).toList()
        self.assertEqual(s, [2, 4])

    def test_map(self):
        s = Stream.of(1, 2, 3).map(lambda x: x**2).toList()
        self.assertEqual(s, [1, 4, 9])

    def test_flatMap(self):
        s = Stream.of(1, 2, 3).flatMap(lambda x: Stream.of(x, x)).toList()
        self.assertEqual(s, [1, 1, 2, 2, 3, 3])

    def test_distinct(self):
        s = Stream.of(1, 1, 2, 2, 3, 4)
        self.assertEqual(s.distinct().toList(), [1, 2, 3, 4])

    def test_limit(self):
        s = Stream.iterate(0, lambda i: i + 1).limit(5).toList()
        self.assertEqual(s, [0, 1, 2, 3, 4])

    def test_skip(self):
        s = Stream.of(1, 2, 3, 4, 5, 6).skip(3).toList()
        self.assertEqual(s, [4, 5, 6])

    def test_takeWhile(self):
        s = Stream.of(1, 2, 3, 4, 5, 6).takeWhile(lambda x: x != 4).toList()
        self.assertEqual(s, [1, 2, 3])

    def test_dropWhile(self):
        s = Stream.of(1, 2, 3, 4, 5, 6).dropWhile(lambda x: x != 4).toList()
        self.assertEqual(s, [4, 5, 6])

    def test_sorted(self):
        s = Stream.of(1, 2, 5, 4, 3).sorted().toList()
        s2 = Stream.of(1, 2, 3, 4, 5).sorted(lambda x, y: y-x).toList()

        self.assertEqual(s, [1, 2, 3, 4, 5])
        self.assertEqual(
            s2, [5, 4, 3, 2, 1])

    def test_peek(self):
        self.count = 0

        def inc(*args):
            self.count += 1

        s = Stream.of(1, 2, 3).peek(inc)
        self.assertEqual(self.count, 0)

        s = s.toList()
        self.assertEqual(self.count, 3)

    def test_forEach(self):
        self.count = 0

        def inc(*args):
            self.count += 1

        s = Stream.of(1, 2, 3).forEach(inc)
        self.assertEqual(self.count, 3)

    def test_anyMatch(self):
        self.assertTrue(Stream.of(1, 2, 3).anyMatch(lambda x: x % 2 == 0))
        self.assertFalse(
            Stream.of(1, 3, 5, 7).anyMatch(lambda x: x % 2 == 0))

    def test_allMatch(self):
        self.assertTrue(Stream.of(2, 4, 6, 8).allMatch(lambda x: x % 2 == 0))
        self.assertFalse(Stream.of(1, 2, 3, 4, 5).allMatch(lambda x: x < 5))

    def test_noneMatch(self):
        self.assertTrue(Stream.of(1, 2, 3, 4).noneMatch(lambda x: x > 4))
        self.assertFalse(Stream.of(1, 2, 3, 4, 5).noneMatch(lambda x: x > 4))

    def test_findFirst(self):
        elem = Stream.of(1, 2, 3, 4, 5).findFirst()
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), 1)

    def test_findAny(self):
        elem = Stream.of(1, 2, 3, 4, 5).findAny()
        self.assertTrue(elem.isPresent())
        self.assertIn(elem.get(), [1, 2, 3, 4, 5])

    def test_reduce(self):
        elem = Stream.of(1, 2, 3).reduce(lambda x, y: x - y)
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), -4)

        elem = Stream.of(1, 2, 3).reduce(lambda x, y: x - y, 0)
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), -6)

    def test_min(self):
        s = Stream.of(1, 2, 5, 4, 3)
        self.assertTrue(s.min().isPresent())
        self.assertEqual(s.min().get(), 1)

    def test_max(self):
        s = Stream.of(1, 2, 5, 4, 3)
        self.assertTrue(s.max().isPresent())
        self.assertEqual(s.max().get(), 5)

    def test_sum(self):
        self.assertTrue(Stream.of(1, 2, 3, 4).sum().isPresent())
        self.assertEqual(Stream.of(1, 2, 3, 4).sum().get(), 10)

    def test_count(self):
        self.assertEqual(Stream.of(1, 2, 3, 4).count(), 4)
        self.assertEqual(Stream.empty().count(), 0)
        self.assertEqual(Stream.generate(lambda: 1).limit(10).count(), 10)

    def test_iter(self):
        index = 1
        s = Stream.of(1, 2, 3)
        for elem in s:
            self.assertEqual(elem, index)
            index += 1


if __name__ == '__main__':
    unittest.main()
