from annotation import *

class Row:

    def __init__(self, components, number, ref=None):
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
        if type(number) is not int:
            raise Exception('Row numbers must be integers.')
        if ref and type(ref) is not int:
            raise Exception('Row references must be integers.')
        for component in components:
            if component.__class__ is not Annotation:
                raise Exception('Each component of a Row must be an Annotation.')

        self.components = components
        self.number = number
        self.ref = ref

    def __str__(self):
        """Return an XML representation of the row."""

        row_str = '<row number="' + str(self.number)
        if self.ref:
            row_str += '" ref="' + self.ref
        row_str += '">' + '\n'.join([component.__str__() for component in self.components]) + '</row>'
        return row_str

    def __eq__(self, other):
        """Return whether two rows have the same properties."""

        if other.__class__ is not Row:
            return False
        if self.number != other.number:
            return False
        if len(self.components) != len(other.components):
            return False
        if self.ref != other.ref:
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])