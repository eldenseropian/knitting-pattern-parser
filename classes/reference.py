from annotation import *
from repeat import *
from row import *
from section import *

class Reference:

    def __init__(self, reference):
        """Create a new reference.

        Keyword arguments:
        reference -- the object to reference
        """
        if reference.__class__ not in [Annotation, Repeat, Row, Section]:
            raise Exception('References must be to existing pattern classes.')

        self.reference = reference

    def __eq__(self, other):
        """Return whether two references point to the same object."""

        return self.reference == other.reference

    # TODO: figure out if there's any other types of refs beside row refs
    def __str__(self):
        return '<row reference="' + str(self.reference.number) + '"/>'