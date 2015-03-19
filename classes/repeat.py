from pattern import is_valid_component

class Repeat:

    def __init__(self, components, start, times=None):
        """Create a new repeat.

        Keyword arguments:
        components -- a list of annotations, references, and/or rows that comprise the repeat
        start -- the row number of the first row in the repeat
        times -- the number of times to repeat, None indicates the repeat is indefinite
        """

        if type(components) is not list:
            raise Exception('Components must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        if type(start) is not int:
            raise Exception('Start row number must be an integer.')
        if times is not None and type(times) is not int and type(times) is not str:
            raise Exception('Number of times to repeat must be an integer or string.')
        for component in components:
            if not is_valid_component(component):
                raise Exception('Each component of a Repeat must be an Annotation, Reference, or Row.')

        self.components = components
        self.start = start
        self.times = times

    def __str__(self):
        """Return an XML representation of the repeat."""

        repeat_str = '<repeat start="' + str(self.start)
        if self.times:
            repeat_str += '" times="' + str(self.times)
        repeat_str += '">\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</repeat>'
        return repeat_str

    def __eq__(self, other):
        """Return whether two repeats have the same properties."""

        if other.__class__ is not Repeat:
            return False
        if self.start != other.start:
            return False
        if self.times != other.times:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

class InRowRepeat:

    def __init__(self, components, until=None):
        # TODO: thorough checking
        if type(components) is not list:
            raise Exception('Components must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')

        self.components = components
        self.until = until

    def __str__(self):
        """Return an XML representation of the repeat."""

        repeat_str = '<repeat'
        if self.until:
            repeat_str += ' until="' + self.until + '"'
        repeat_str += '>\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</repeat>'
        return repeat_str

    def __eq__(self, other):
        if other.__class__ is not InRowRepeat:
            return False
        if self.until != other.until:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])