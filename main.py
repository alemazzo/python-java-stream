from Stream import *

Stream.iterate(1, lambda i: i + 1).limit(10).map(lambda x: x **
                                                 2).forEach(print)
lista = list()
Stream.iterate(1.0, lambda i: i +
               0.5).limit(10).map(float.is_integer).forEach(print)
