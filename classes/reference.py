from pattern import is_valid_component

class Reference:

    def __init__(self, reference, number=None):
        """Create a new reference.

        Keyword arguments:
        reference -- the object to reference
        """
        if not is_valid_component(reference):
            raise Exception('References must be to existing pattern classes.')
        if number is not None and type(number) is not int:
            raise Exception('Row numbers must be integers')

        self.reference = reference
        self.number = number

    def __eq__(self, other):
        """Return whether two references point to the same object."""

        return self.reference == other.reference

    # TODO: figure out if there's any other types of refs beside row refs
    def __str__(self):
        row_str = '<row '
        if self.number:
            row_str += 'number="' + str(self.number) + '" '
        row_str += 'reference="' + str(self.reference.number) + '"/>'
        return row_str