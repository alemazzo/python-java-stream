from Stream import Stream

res = Stream.iterate(0, lambda x: x + 2).limit(10).sorted().findFirst()
print(res)
