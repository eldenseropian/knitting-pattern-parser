from annotation import *

class Row:
    def __init__(self, components, number):
        if type(components) is not list:
            raise Exception('Components must be a list.')
        if len(components) == 0:
            raise Exception('Components must not be empty.')
        if type(number) is not int:
            raise Exception('Number must be an integer.')
        for component in components:
            if component.__class__ is not Annotation:
                raise Exception('Each component of a Row must be an Annotation.')

        self.components = components
        self.number = number

    def __str__(self):
        return '<row number="' + str(self.number) + '">' + '\n'.join([component.__str__() for component in self.components]) + '</row>'

    def __eq__(self, other):
        if other.__class__ is not Row:
            return False
        if self.number != other.number:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])