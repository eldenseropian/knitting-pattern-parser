class Annotation:
    """Annotations represent any natural language found in the pattern."""

    def __init__(self, text):
        """Create a new annotation.

        Keyword arguments:
        text -- the text of the annotation (a string). Will be stripped of whitespace. Must not be empty.
        """

        text = text.strip()
        if not text:
            raise Exception('Empty Annotation.')
        if type(text) != str:
            raise Exception('Annotations must be strings.')

        self.text = text
    
    def __str__(self):
        """Return an XML representation of the annotation."""

        return '<annotation>' + self.text + '</annotation>'

    def __eq__(self, other):
        """Return whether two objects are annotations and have the same text."""

        return other.__class__ is Annotation and self.text == other.text

    def __ne__(self, other):
        return not self.__eq__(other)