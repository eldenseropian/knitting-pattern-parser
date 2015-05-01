import copy

from os.path import join
from sys import path

path.append(join('.', 'classes'))

from pattern import *

def expand(pattern):
    """Expand every reference in a pattern.

    Keyword arguments:
    pattern -- the pattern to dereference

    Returns a dereferenced version of the pattern. Does not mutate the pattern.
    """

    expanded_pattern = Pattern(pattern.title)
    for component in pattern.components:
        if component.__class__ == Reference:
            expanded_pattern += expand_reference(component)
        else:
            expanded_pattern += component
    return expanded_pattern

def expand_reference(reference):
    """Expand a Reference.

    Keyword arguments:
    reference -- the reference to expand

    References without row numbers cannot be dereferenced.

    Returns the referenced Row, or the Reference if it does not have a row number.
    """

    if reference.__class__ != Reference:
        raise TypeError('reference must be a Reference')

    if not reference.number:
        return reference

    new_row = copy.copy(reference.reference)
    new_row.number = reference.number
    return new_row