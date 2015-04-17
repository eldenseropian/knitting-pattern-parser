from pattern import is_valid_row_component, is_equal_pairwise

class Row:
    """A Row is the most common unit of organization in a pattern.

    For this implementation, rows are considered synonymous with rounds.
    """

    def __init__(self, components, number, side=None):
        """Create a new row.

        Keyword arguments:
        components -- a list of annotations that comprise the row
        number -- the row number (an integer)
        side -- either 'RS' or 'WS' (right side/wrong side)
        """

        if type(components) is not list:
            raise TypeError('Components must be a list.')
        if len(components) == 0:
            raise ValueError('Components must not be empty.')
        for component in components:
            if not is_valid_row_component(component):
                raise TypeError('Each component of a Row must be an Annotation or InRowRepeat.')

        if type(number) is not int:
            raise TypeError('Row numbers must be integers.')

        if side is not None and side != 'RS' and side != 'WS':
            raise ValueError('Side must be \'RS\' or \'WS\'.')

        self.components = components
        self.number = number
        self.side = side

    def __str__(self):
        """Return an XML representation of the row."""

        row_str = '<row number="' + str(self.number)
        if self.side:
            row_str += '" side="' + self.side
        row_str += '">\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</row>'
        return row_str

    def __eq__(self, other):
        """Return whether two rows have the same properties (components, number, and side)."""

        if other.__class__ is not Row:
            return False
        if self.number != other.number:
            return False
        if self.side != other.side:
            return False
        return is_equal_pairwise(self.components, other.components)

    def __ne__(self, other):
        return not self.__eq__(other)