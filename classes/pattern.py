class Pattern:
    def __init__(self, title, components):
        if type(title) is not str:
            raise Exception('Title must be a string.')
        if type(components) is not list:
            raise Exception('Patterns must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        for component in components:
            if component.__class__ not in [Annotation, Reference, Repeat, Row]:
                raise Exception('Each component of a pattern must be an Annotation, Reference, Repeat, or Row.')
        self.title = title
        self.components = components
    
    def __str__(self):
        return '<pattern>\n<title>' + self.title + '</title>\n' + '\n'.join([component.__str__() for component in self.components]) + '\n</pattern>'

    def __eq__(self, other):
        if other.__class__ is not Pattern:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

def is_valid_component(component):
    return component.__class__ in [Annotation, Reference, Repeat, Row]

def is_valid_row_component(component):
    return component.__class__ in [Annotation, InRowRepeat]

from annotation import *
from reference import *
from repeat import *
from row import *