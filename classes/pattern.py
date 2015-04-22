class Pattern:
    """AST that represents a knitting pattern.

    Composed of Annotations, Rows, References, and Repeats.
    """
    def __init__(self, title):
        """Create a new Pattern.

        Patterns must have titles, and are initialized with an empty set of components.

        Keyword arguments:
        title -- the title of the pattern (a string)

        Properties:
        title -- the title of the pattern (a string)
        components -- the list of Annotations, Rows, References, and Repeats that compose the pattern
        rows -- a dictionary of rows in the pattern, indexed by row number, used for References
        next_row_number -- the number to give the next parsed row
        """

        if type(title) is not str:
            raise TypeError('Title must be a non-empty string.')
        if not title.strip():
            raise ValueError('Title must be a non-empty string.')

        self.title = title
        self.components = []
        self._rows = {}
        self.next_row_number = 1
    
    def __iadd__(self, other):
        """Add a component or components to the pattern (overrides +=).

        Keyword arguments:
        other -- the component or list of components to add. Limited to Annotations, Rows, References, Repeats, or a flat list thereof.
        """

        if type(other) is list:
            for component in other:
                self._add_component(component)
        else:
            self._add_component(other)
        return self

    def __str__(self):
        """Return an XML representation of the pattern."""

        pattern_str = '<pattern title="' + self.title + '">'
        pattern_str += ''.join([component.__str__() for component in self.components])
        pattern_str += '</pattern>'
        return pattern_str

    def __eq__(self, other):
        """Return whether two objects are both Patterns and have the same components."""

        if other.__class__ is not Pattern:
            return False
        return is_equal_pairwise(self.components, other.components)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_row(self, number):
        """Return the Row or list of Rows with the given number.

        Raises a KeyError if the requested row is non-existent.

        Keyword arguments:
        number -- the number of the row(s) to retrieve (int)
        """

        # TODO: figure out best way to handle problem of multiple rows with same number
        def get_single_row(row):
            if type(row) == list:
                return row[-1]
            return row

        row_to_get = None

        if 'odd' in self._rows and number % 2 == 1:
            row_to_get = 1
        if 'even' in self._rows and number % 2 == 0:
            row_to_get = 2

        if row_to_get is not None:
            return get_single_row(self._rows[row_to_get])

        if number not in self._rows:
            raise ValueError('Row number ' + str(number) + ' does not exist.')

        return get_single_row(self._rows[number])

    def _add_row(self, row):
        """Add a row to the pattern, indexed by row number.

        If there is already a row with that number in the pattern, add the new row to a list at that index.

        Keyword arguments:
        row -- the Row to add
        """

        if row.number in self._rows:
            if type(self._rows[row.number]) == list:
                self._rows[row.number].append(row)
            else:
                self._rows[row.number] = [self._rows[row.number], row]
        else:
            self._rows[row.number] = row

    def _add_component(self, component):
        """Add a component to the pattern.

        Updates the row dictionary and next_row_number.

        Keyword arguments:
        component -- the component to add. Must be an Annotation, Reference, Repeat, or Row.
        """

        if not is_valid_component(component):
            raise Exception('Each component of a pattern must be an Annotation, Reference, Repeat, or Row.')

        self.components.append(component)

        if component.__class__ in [Row, InRowRepeat, Reference]:
            self._add_row(component)
            self.next_row_number = component.number + 1

        elif is_and_all_repeat(component):
            if 'even' in self._rows:
                del self._rows['even']
            if 'odd' in self._rows:
                del self._rows['odd']
            self._rows[component.times] = True # indicate that all even or all odd rows are the same
            self._add_row(component.components[0])
            self.next_row_number = component.components[0].number + 1

        elif component.__class__ == Repeat:
            if component.times is not None and type(component.times) is int:
                self.next_row_number = component.start + len(component.components) * component.times
            else: # restart row count after undefined repeat
                self.next_row_number = 1

def is_valid_component(component):
    """Return whether a component can be in a Pattern."""

    return component.__class__ in [Annotation, Reference, Repeat, Row]

def is_valid_row_component(component):
    """Return whether a component can be in a Row."""

    return component.__class__ in [Annotation, InRowRepeat]

def is_and_all_repeat(component):
    """Return whether a component is a Repeat with an instruction to repeat for all even or odd rows."""

    return component.__class__ == Repeat and (component.times == 'even' or component.times == 'odd')

def is_annotation(instance):
    """Return whether a component is an Annotation."""

    return instance.__class__ == Annotation

def is_equal_pairwise(components1, components2):
    """Return whether two lists of components are the same via pairwise comparison."""

    if type(components1) != list or type(components2) != list:
        raise TypeError('Components must be lists.')

    if len(components1) != len(components2):
        return False

    if len(components1) == 0:
        return True

    return reduce(lambda x, y: x and y, [components1[i] == components2[i] for i in range(len(components1))])

from annotation import *
from in_row_repeat import *
from reference import *
from repeat import *
from row import *