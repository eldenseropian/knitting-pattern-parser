class Pattern:
    def __init__(self, title):
        if type(title) is not str:
            raise Exception('Title must be a string.')
        self.title = title

        self.components = []
        self.rows = {}
        self.next_row_number = 1
    
    def __iadd__(self, other):
        if type(other) is list:
            for component in other:
                self.add_component(component)
        else:
            self.add_component(other)
        return self

    def __str__(self):
        pattern_str = '<pattern>\n<title>' + self.title + '</title>'
        if len(self.components) > 0:
            pattern_str += '\n' + '\n'.join([component.__str__() for component in self.components])
        pattern_str += '\n</pattern>'
        return pattern_str

    def __eq__(self, other):
        if other.__class__ is not Pattern:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

    def add_component(self, component):
        if not is_valid_component(component):
            raise Exception('Each component of a pattern must be an Annotation, Reference, Repeat, or Row.')
        self.components.append(component)
        if component.__class__ in [Row, InRowRepeat, Reference]:
            self.rows[component.number] = component
            if component.number < self.next_row_number: # restarted row counting - row 1 gets redefined etc
                self.rows = {}
            self.next_row_number = component.number + 1
        elif is_and_all_repeat(component):
            if component.times == 'even':
                if 1 in self.rows:
                    row1 = self.rows[1]
                    self.rows = {1: row1}
                else:
                    self.rows = {}
                self.rows['even'] = True
                self.rows[2] = component.components[0]
            else:
                self.rows = {}
                self.rows['odd'] = True
                self.rows[1] = component.components[0]
        elif component.__class__ == Repeat:
            if component.times is not None and type(component.times) is int:
                self.next_row_number = component.start + len(component.components) * component.times
            else: # restart row count after undefined repeat
                self.next_row_number = 1


    def get_row(self, number):
        try:
            return self.rows[number]
        except KeyError, e:
            if number % 2 == 1 and 'odd' in self.rows:
                return self.rows[1]
            if number % 2 == 0 and 'even' in self.rows:
                return self.rows[2]
            raise e

def is_valid_component(component):
    return component.__class__ in [Annotation, Reference, Repeat, Row]

def is_valid_row_component(component):
    return component.__class__ in [Annotation, InRowRepeat]

def is_and_all_repeat(component):
    return component.__class__ == Repeat and (component.times == 'even' or component.times == 'odd')

from annotation import *
from reference import *
from repeat import *
from row import *