from row import *
from annotation import *

class Section:
    def __init__(self, components):
        if type(components) is not list:
            raise Exception('Patterns must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        for component in components:
            if component.__class__ is not Row and component.__class__ is not Annotation:
                raise Exception('Each component of a Section must be a Row or Annotation.')
        self.components = components
    
    def __str__(self):
        return '\n'.join([component.__str__() for component in self.components])

    def __eq__(self, other):
        if other.__class__ is not Section:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])