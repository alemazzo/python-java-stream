from Stream import *

res = Stream.iterate(0, lambda x: x + 2).limit(10).sorted().findFirst()
print(res)

lista = Stream([1, 2, 3]).forEach(print)
