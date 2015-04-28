from pattern import is_valid_row_component
from pattern import is_equal_pairwise

class InRowRepeat:
    """Represents a series of stitches that are repeated within a single row."""

    def __init__(self, components, until=None):
        """Create a new InRowRepeat.

        Keyword Arguments:
        components -- a list of annotations that comprise the repeat
        until -- instruction as to when to stop repeating (string or None)
        """

        if type(components) is not list:
            raise TypeError('Components must be a list.')
        if len(components) == 0:
            raise ValueError('Components must not be empty.')
        for component in components:
            if not is_valid_row_component(component):
                raise TypeError('Each component of an InRowRepeat must be an Annotation or InRowRepeat.')
        if until is not None and type(until) != str:
            raise TypeError('Until must be a non-empty string.')
        if until is not None and not until.strip():
            raise ValueError('Until must be a non-empty string.')

        self.components = components
        self.until = until

    def __str__(self):
        """Return an XML representation of the in-row repeat."""

        repeat_str = '<repeat'
        if self.until:
            repeat_str += ' until="' + self.until + '"'
        repeat_str += '>' + ''.join([component.__str__() for component in self.components]) + '</repeat>'
        return repeat_str

    def __eq__(self, other):
        """Return whether two objects are both InRowRepeats and have the same components."""

        if other.__class__ is not InRowRepeat:
            return False
        if self.until != other.until:
            return False
        return is_equal_pairwise(self.components, other.components)

    def __ne__(self, other):
        return not self.__eq__(other)