from Stream import *

Stream.iterate(1, lambda i: i + 1).limit(10).map(lambda x: x **
                                                 2).forEach(print)
