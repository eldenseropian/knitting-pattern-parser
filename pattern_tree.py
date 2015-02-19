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

class Section:
    def __init__(self, components):
        if type(components) is not list:
            raise Exception('Patterns must be a list.')
        for component in components:
            if component.__class__ is not Row and component.__class__ is not Annotation:
                raise Exception('Each component of a Section must be a Row or Annotation.')
        self.components = components
    
    def __str__(self):
        return '\n'.join([component.__str__() for component in self.components])

    def __eq__(self, other):
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

class Row:
    def __init__(self):
        self.components = []
        self.number = None

    def __str__(self):
        return 'Row ' + self.number + ': ' + ' '.join([component.__str__() for component in self.components])

    def __eq__(self, other):
        if self.number != other.number:
            return False
        if len(self.components) != len(other.components):
            return False
        return reduce(lambda x, y: x and y, [self.components[i] == other.components[i] for i in range(len(self.components))])

class Annotation:
    def __init__(self, text):
        if not text:
            raise Exception('Empty Annotation')
        self.text = text
    
    def __str__(self):
        return '<annotation>' + self.text + '</annotation>'

    def __eq__(self, other):
        return self.text == other.text


'''
pattern := section[]
section := (annotation|row)[]
row := (annotation|stitch)[]

'''