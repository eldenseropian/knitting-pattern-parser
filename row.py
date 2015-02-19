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