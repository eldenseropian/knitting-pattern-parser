import re

from annotation import *
from pattern_tree import *
from row import *
from section import *

ROW_REGEX = re.compile('\d+\.')

def parse(pattern):
    pattern = pattern.splitlines()
    lines = []
    for line in pattern:
        match = re.match(ROW_REGEX, line)
        if match:
            start, length = match.span()
            number = int(line[start : start + length - 1])
            text = line[start + length + 1 :]
            lines.append(Row([Annotation(text)], number))
        elif line:
            lines.append(Annotation(line))
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