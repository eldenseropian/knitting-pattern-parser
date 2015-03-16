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
            if ref is None or components is not None:
                raise Exception('Components must be a list, or None if ref is specified.')
        if components is not None:
            if len(components) == 0:
                raise Exception('Components must not be empty.')
            for component in components:
                if component.__class__ is not Annotation:
                    raise Exception('Each component of a Row must be an Annotation.')
        if type(number) is not int:
            raise Exception('Row numbers must be integers.')
        if ref is not None and type(ref) is not int:
            raise Exception('Row references must be integers.')

        self.components = components
        self.number = number
        self.ref = ref

    def __str__(self):
        """Return an XML representation of the row."""

        row_str = '<row number="' + str(self.number)
        if self.ref is not None:
            row_str += '" ref="' + str(self.ref)
        row_str += '">'
        if self.components is not None:
            row_str += '\n'.join([component.__str__() for component in self.components])
        row_str += '</row>'
        return row_str

    def __eq__(self, other):
        """Return whether two rows have the same properties."""

        if other.__class__ is not Row:
            return False
        if self.number != other.number:
            return False
        if self.ref != other.ref:
            return False
        if self.components is not None:
            if other.components is None or len(self.components) != len(other.components):
                return False
            return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])
        elif other.components is not None:
            return False
        return True

