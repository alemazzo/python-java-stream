class Optional:

    '''
    A container object which may or may not contain a non-null value. If a value is present, isPresent() returns true. If no value is present, the object is considered empty and isPresent() returns false.

    Additional methods that depend on the presence or absence of a contained value are provided, such as orElse() (returns a default value if no value is present) and ifPresent() (performs an action if a value is present). 
    '''

    '''
    STATIC METHODS
    '''

    @staticmethod
    def empty():
        '''
        Returns an empty Optional instance. No value is present for this Optional.

        :return: an empty Optional
        '''
        return Optional(None)

    @staticmethod
    def of(elem):
        '''
        Returns an Optional describing the given non-null value.

        :param T elem: the value to describe, which must be non-null
        :return: an Optional with the value present
        :raise: Exception if the value is null
        '''
        if elem is None:
            raise Exception("Optional Empty")
        return Optional(elem)

    @staticmethod
    def ofNullable(elem):
        '''
        Returns an Optional describing the given value, if non-null, otherwise returns an empty Optional.

        :param T elem: the possibly-null value to describe
        :return: an Optional with a present value if the specified value is non-null, otherwise an empty Optional
        '''
        return Optional(elem)

    '''
    NON STATIC METHODS
    '''

    def __init__(self, elem):
        self.__elem = elem

    def get(self):
        '''
        If a value is present, returns the value, otherwise raise an Exception.

        :return: the non-null value described by this Optional
        :raise: Exception if no value is present
        '''
        if self.isEmpty():
            raise Exception("Optional Empty")
        return self.__elem

    def isPresent(self):
        '''
        If a value is present, returns true, otherwise false.

        :return: true if a value is present, otherwise false
        '''
        return not self.isEmpty()

    def isEmpty(self):
        '''
        If a value is not present, returns true, otherwise false.

        :return: true if a value is not present, otherwise false
        '''
        return self.__elem is None

    def ifPresent(self, action):
        '''
        If a value is present, performs the given action with the value, otherwise does nothing.

        :param Function action: the action to be performed, if a value is present
        :raise Exception if value is present and the given action is null
        '''
        if self.isPresent():
            action(self.get())

    def ifPresentOrElse(self, action, emptyAction):
        '''
        If a value is present, performs the given action with the value, otherwise performs the given empty-based action.

        :param Function action: the action to be performed, if a value is present
        :param Function emptyAction: the empty-based action to be performed, if no value is present
        :raise Exception if a value is present and the given action is null, or no value is present and the given empty-based action is null.
        '''
        if self.isPresent():
            action(self.get())
        else:
            emptyAction()

    def filter(self, predicate):
        '''
        If a value is present, and the value matches the given predicate, returns an Optional describing the value, otherwise returns an empty Optional.

        :param Predicate predicate: the predicate to apply to a value, if present
        :return: an Optional describing the value of this Optional, if a value is present and the value matches the given predicate, otherwise an empty Optional
        '''
        if self.isPresent() and predicate(self.get()):
            return self
        else:
            return Optional.empty()

    def map(self, mapper):
        '''
        If a value is present, returns an Optional describing (as if by ofNullable(T)) the result of applying the given mapping function to the value, otherwise returns an empty Optional. 
        If the mapping function returns a null result then this method returns an empty Optional.

        :param Mapper mapper: the mapping function to apply to a value, if present
        :return: an Optional describing the result of applying a mapping function to the value of this Optional, if a value is present, otherwise an empty Optional
        '''
        if self.isPresent():
            return Optional.ofNullable(mapper(self.get()))
        else:
            return Optional.empty()
