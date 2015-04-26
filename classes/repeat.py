from pattern import is_valid_component, is_equal_pairwise

class Repeat:
    """Represents a row or series of rows that are repeated."""

    def __init__(self, components, start, times=None):
        """Create a new repeat.

        Repeats can be definite or indefinite. Definite repeats are executed a
        specified number of times. Indefinite repeats are specified an indefinite
        number of times, such as 'Repeat until piece measures 70"' or
        'Repeat until desired length'.

        Keyword arguments:
        components -- a list of annotations, references, and/or rows that comprise the repeat
        start -- the row number of the first row in the repeat
        times -- the number of times to repeat, None indicates the repeat is indefinite
        """

        if type(start) is not int:
            raise TypeError('Start row number must be an integer.')
        if start <= 0:
            raise ValueError('Start row number must be positive.')

        if times is not None and type(times) is not int and type(times) is not str:
            raise TypeError('Number of times to repeat must be an integer or string.')
        if type(times) is int and times <= 0:
            raise ValueError('Number of times to repeat must be positive.')

        if type(components) is not list:
            raise TypeError('Components must be a list.')
        if len(components) == 0:
            raise ValueError('Components must not be empty.')
        for component in components:
            if not is_valid_component(component):
                raise TypeError('Each component of a Repeat must be an Annotation, Reference, or Row.')

        self.components = components
        self.start = start
        self.times = times

    def __str__(self):
        """Return an XML representation of the repeat."""

        repeat_str = '<repeat start="' + str(self.start)
        if self.times:
            repeat_str += '" times="' + str(self.times)
        repeat_str += '">' + ''.join([component.__str__() for component in self.components]) + '</repeat>'
        return repeat_str

    def __eq__(self, other):
        """Return whether two objects are both repeats and have the same properties."""

        if other.__class__ is not Repeat:
            return False
        if self.start != other.start:
            return False
        if self.times != other.times:
            return False
        return is_equal_pairwise(self.components, other.components)

    def __ne__(self, other):
        return not self.__eq__(other)