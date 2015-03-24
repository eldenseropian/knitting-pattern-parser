from pattern import is_annotation

class InRowRepeat:
    """Represents a series of stitches that are repeated within a single row."""

    def __init__(self, annotation, until=None):
        """Create a new InRowRepeat.

        Keyword Arguments:
        annotation -- an Annotation instance that is to be repeated
        until -- instruction as to when to stop repeating (string or None)
        """

        if not is_annotation(annotation):
            raise Exception('Repeated sections within Rows must be Annotations.')
        if until is not None and type(until) != str:
            raise Exception('Until must be a string.')

        self.annotation = annotation
        self.until = until

    def __str__(self):
        """Return an XML representation of the in-row repeat."""

        repeat_str = '<repeat'
        if self.until:
            repeat_str += ' until="' + self.until + '"'
        repeat_str += '>\n' + self.annotation.__str__() + '\n</repeat>'
        return repeat_str

    def __eq__(self, other):
        """Return whether two objects are both InRowRepeats and have the same components."""

        if other.__class__ is not InRowRepeat:
            return False
        if self.annotation != other.annotation:
            return False
        return self.until == other.until

    def __ne__(self, other):
        return not self.__eq__(other)