import unittest
from stream import Stream
from time import sleep


class TestParallelStream(unittest.TestCase):

    def test_empty(self):
        s = Stream.empty().parallel()
        self.assertEqual(s.count(), 0)

    def test_of(self):

        self.assertEqual(Stream.of(1, 2, 3, 4).parallel().count(), 4)

        self.assertTrue(Stream.of(1, 2, 3, 4).parallel().findAny().isPresent())

        self.assertIn(Stream.of(1, 2, 3, 4).parallel(
        ).findAny().get(), [1, 2, 3, 4])

        self.assertEqual(Stream.ofNullable(None).parallel(),
                         Stream.empty().parallel())

        self.assertEqual(Stream.of().parallel(), Stream.empty().parallel())

    def test_iter(self):
        index = 1
        s = Stream.of(1, 2, 3).parallel()
        for elem in s:
            self.assertEqual(elem, index)
            index += 1

    def test_infinite_iterate(self):
        index = 0
        s = Stream.iterate(index, lambda i: i +
                           1).parallel()
        for elem in s:
            self.assertEqual(elem, index)
            index += 1
            if index == 10:
                break

        s.terminate()

    def test_generate(self):
        index = 0
        s = Stream.generate(lambda: 1).parallel()

        for elem in s:
            self.assertEqual(elem, 1)
            index += 1
            if index == 10:
                break
        s.terminate()

    def test_concat(self):
        s = Stream.concat(Stream.of(1, 2, 3).parallel(), Stream.of(
            4, 5, 6).parallel()).parallel()

        self.assertEqual(s, [1, 2, 3, 4, 5, 6])

    def test_filter(self):
        s = Stream.of(1, 2, 3, 4).parallel().filter(
            lambda x: x % 2 == 0).toList()
        self.assertEqual(s, [2, 4])

    def test_map(self):
        s = Stream.of(1, 2, 3).parallel().map(lambda x: x**2).toList()
        self.assertEqual(s, [1, 4, 9])

    def test_distinct(self):
        s = Stream.of(1, 1, 2, 2, 3, 4).parallel()
        self.assertEqual(s.distinct().toList(), [1, 2, 3, 4])

    def test_flatMap(self):
        s = Stream.of(1, 2, 3).parallel().flatMap(
            lambda x: Stream.of(x, x)).toList()
        self.assertEqual(s, [1, 1, 2, 2, 3, 3])

    def test_peek(self):
        self.count = 0

        def inc(*args):
            self.count += 1

        s = Stream.of(1, 2, 3).parallel().peek(inc)
        self.assertEqual(self.count, 0)

        s = s.toList()
        self.assertEqual(self.count, 3)

    def test_forEach(self):
        self.count = 0

        def inc(*args):
            self.count += 1

        s = Stream.of(1, 2, 3).parallel().forEach(inc)

        self.assertEqual(self.count, 3)

    def test_anyMatch(self):
        self.assertTrue(
            Stream.of(1, 2, 3).parallel().anyMatch(lambda x: x % 2 == 0))
        self.assertFalse(
            Stream.of(1, 3, 5, 7).parallel().anyMatch(lambda x: x % 2 == 0))

    def test_allMatch(self):
        self.assertTrue(
            Stream.of(2, 4, 6, 8).parallel().allMatch(lambda x: x % 2 == 0))
        self.assertFalse(
            Stream.of(1, 2, 3, 4, 5).parallel().allMatch(lambda x: x < 5))

    def test_noneMatch(self):
        self.assertTrue(
            Stream.of(1, 2, 3, 4).parallel().noneMatch(lambda x: x > 4))
        self.assertFalse(
            Stream.of(1, 2, 3, 4, 5).parallel().noneMatch(lambda x: x > 4))

    def test_findAny(self):
        elem = Stream.of(1, 2, 3, 4, 5).parallel().findAny()
        self.assertTrue(elem.isPresent())
        self.assertIn(elem.get(), [1, 2, 3, 4, 5])

    def test_min(self):
        s = Stream.of(1, 2, 5, 4, 3).parallel().min()
        self.assertTrue(s.isPresent())
        self.assertEqual(s.get(), 1)

    def test_max(self):
        s = Stream.of(1, 2, 5, 4, 3).parallel().max()
        self.assertTrue(s.isPresent())
        self.assertEqual(s.get(), 5)

    def test_sum(self):
        self.assertTrue(Stream.of(1, 2, 3, 4).parallel().sum().isPresent())
        self.assertEqual(Stream.of(1, 2, 3, 4).parallel().sum().get(), 10)

    def test_count(self):
        self.assertEqual(Stream.of(1, 2, 3, 4).parallel().count(), 4)
        self.assertEqual(Stream.empty().parallel().count(), 0)
        self.assertEqual(Stream.generate(
            lambda: 1).limit(10).parallel().count(), 10)


"""
    def test_limit(self):
        s = Stream.iterate(0, lambda i: i + 1).parallel().limit(5).toList()
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
    
    def test_findFirst(self):
        # TODO: Implements
        elem = Stream.of(1, 2, 3, 4, 5).parallel().findFirst()
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), 1)

    def test_reduce(self):
        # TODO: Reduce is unstable
        elem = Stream.of(1, 2, 3).parallel().reduce(lambda x, y: x - y)
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), -4)

        elem = Stream.of(1, 2, 3).parallel().reduce(lambda x, y: x - y, 0)
        self.assertTrue(elem.isPresent())
        self.assertEqual(elem.get(), -6)
"""

if __name__ == '__main__':
    unittest.main()
