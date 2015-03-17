from annotation import *
from row import *

class Repeat:

    def __init__(self, components, start, times):
        """Create a new row.

        Keyword arguments:
        components -- a list of annotations and/or rows that comprise the repeat
        times -- the number of times to repeat
        """

        if type(components) is not list:
            raise Exception('Components must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        if type(start) is not int:
            raise Exception('Start row number must be an integer.')
        if type(times) is not int:
            raise Exception('Number of times to repeat must be an integer.')
        for component in components:
            # TODO: nested repeats
            if component.__class__ not in [Annotation, Reference, Row]:
                raise Exception('Each component of a Repeat must be an Annotation, Reference, or Row.')

        self.components = components
        self.start = start
        self.times = times

    def __str__(self):
        """Return an XML representation of the repeat."""

        return '<repeat start="' + str(self.start) + '" times="' + str(self.times) + '">\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</repeat>'

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

from reference import *