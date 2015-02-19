from pattern_tree import *
from section import *
from row import *
from annotation import *

def parse(pattern):
    pattern = pattern.splitlines()
    lines = [Annotation(line) for line in pattern if line]
    pattern_section = Section(lines)
    pattern = PatternTree([pattern_section])
    return pattern

def unroll():
    pass

def expand_reference():
    pass

if __name__ == '__main__':
    pat = open('../scarf-beginner.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    parse(pat_lines)