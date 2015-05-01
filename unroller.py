import copy

from os.path import join
from sys import path

path.append(join('.', 'classes'))

from pattern import *

def unroll(pattern):
    """Unroll every loop in a pattern.

    Keyword arguments:
    pattern -- the pattern to unroll

    Returns an unrolled version of the pattern. Does not mutate the pattern.
    """

    unrolled_pattern = Pattern(pattern.title)
    for component in pattern.components:
        if component.__class__ == Repeat:
            unrolled_pattern += unroll_repeat(component)
        else:
            unrolled_pattern += component
    return unrolled_pattern

def unroll_repeat(repeat):
    """Unroll a Repeat.

    Keyword arguments:
    repeat -- the repeat to unroll

    Indefinite repeats do not unroll. Returns a list containing the indefinite
    repeat.

    Returns a list of the components comprising the unrolled repeat.
    """
    if repeat.__class__ != Repeat:
        raise TypeError('repeat must be a Repeat.')

    if not repeat.times or type(repeat.times) == str:
        return [repeat]

    unrolled_components = []
    row_number = repeat.start
    last_side = None
    for i in range(repeat.times):
        # TODO: update row #s
        for component in repeat.components:
            if component.__class__ == Annotation:
                unrolled_components.append(component)
            elif component.__class__ == Row:
                new_row = copy.copy(component)
                new_row.number = row_number
                if row_number != repeat.start:
                    if last_side == 'WS':
                        new_row.side = 'RS'
                        last_side = 'RS'
                    elif last_side == 'RS':
                        new_row.side = 'WS'
                        last_side = 'WS'
                    else:
                        new_row.side = None
                elif component.side:
                    last_side = component.side
                row_number += 1
                unrolled_components.append(new_row)
            elif component.__class__ == Reference:
                new_reference = copy.deepcopy(component)
                new_reference.number = row_number
                row_number += 1
                unrolled_components.append(new_reference)
            else:
                raise RuntimeError('Repeats may only contain Annotations, References, and Rows')

    return unrolled_components

def unroll_in_row_repeat(repeat):
    """Unroll an InRowRepeat.

    Keyword arguments:
    repeat -- the repeat to unroll

    Returns a list of the components comprising the unrolled repeat.
    """

    raise NotImplementedError('This is coming in version 2.0')