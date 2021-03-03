class Optional:

    @staticmethod
    def of(elem):
        if elem is None:
            raise Exception("Optional Empty")
        return Optional(elem)

    @staticmethod
    def ofNullable(elem):
        return Optional(elem)

    def __init__(self, elem):
        self.__elem = elem

    def isPresent(self):
        return not self.isEmpty()

    def isEmpty(self):
        return self.__elem is None

    def get(self):
        if self.isEmpty():
            raise Exception("Optional Empty")
        return self.__elem
