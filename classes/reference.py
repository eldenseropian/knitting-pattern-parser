from pattern import is_valid_component

class Reference:
    """References a part of the pattern that has already been parsed.

    Currently only supports references to previous rows: future versions may
    support references to custom-defined stitches or sections. Will never support
    references to things that occur later in the pattern.
    """

    def __init__(self, reference, number=None):
        """Create a new reference.

        Keyword arguments:
        reference -- the object to reference
        number -- the row number of the reference row
        """

        if not is_valid_component(reference):
            raise Exception('References must be to existing Annotations, References, Repeats, or Rows.')
        if number is not None and type(number) is not int:
            raise Exception('Row numbers must be integers.')

        self.reference = reference
        self.number = number

    def __str__(self):
        """Return an XML representation of the Reference.

        As only Row references are currently supported, this returns a string
        similar to the Row XML, but with a reference attribute specified that
        points to the row number of the referenced row.
        """

        row_str = '<row '
        if self.number:
            row_str += 'number="' + str(self.number) + '" '
        row_str += 'reference="' + str(self.reference.number) + '"/>'
        return row_str

    def __eq__(self, other):
        """Return whether two references point to the same object."""

        return self.reference == other.reference

    def __ne__(self, other):
        return not self.__eq__(other)