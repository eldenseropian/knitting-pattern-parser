from annotation import *
from repeat import *

class Row:

    def __init__(self, components, number):
        """Create a new row.

        Keyword arguments:
        components -- a list of annotations that comprise the row
        number -- the row number (an integer)
        ref -- a row number the current row references (default None)
        """

        if type(components) is not list:
            raise Exception('Components must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        for component in components:
            if component.__class__ is not Annotation and component.__class__ is not InRowRepeat:
                raise Exception('Each component of a Row must be an Annotation or InRowRepeat.')
        if type(number) is not int:
            raise Exception('Row numbers must be integers.')

        self.components = components
        self.number = number

    def __str__(self):
        """Return an XML representation of the row."""

        return '<row number="' + str(self.number) + '">\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</row>'

    def __eq__(self, other):
        """Return whether two rows have the same properties."""

        if other.__class__ is not Row:
            return False
        if self.number != other.number:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

