from section import *

class PatternTree:
    def __init__(self, sections):
        if type(sections) is not list:
            raise Exception('Patterns must be a list.')
        for section in sections:
            if section.__class__ is not Section:
                raise Exception('Each component of a pattern must be a Section.')
        self.sections = sections
    
    def __str__(self):
        return '<pattern>' + '\n'.join([section.__str__() for section in self.sections]) + '</pattern>'

    def __eq__(self, other):
        if len(self.sections) != len(other.sections):
            return False
        return reduce(lambda x, y: x and y, [self.sections[i] == other.sections[i] for i in range(len(self.sections))])

'''
pattern := section[]
section := (annotation|row)[]
row := (annotation|stitch)[]

'''