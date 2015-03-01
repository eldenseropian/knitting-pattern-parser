import os
import re
import sys

sys.path.append(os.path.join('.', 'classes'))
from annotation import *
from pattern import *
from row import *
from section import *

ROW_REGEX = re.compile('(Row\s|Round\s)?\d+[\.:]')

def parse(pattern):
    pattern = pattern.splitlines()
    lines = []
    title = pattern[0]
    for line in pattern[1:]:
        match = re.match(ROW_REGEX, line)
        if match:
            start, length = match.span()
            number = line[start : start + length - 1]
            if number.startswith('Row'):
                number = number[3:].strip()
            if number.startswith('Round'):
                number = number[5:].strip()
            number = int(number)
            text = line[start + length + 1 :]
            lines.append(Row([Annotation(text)], number))
        elif line:
            lines.append(Annotation(line))
    pattern_section = Section(lines)
    pattern = Pattern(title, [pattern_section])
    # print pattern
    return pattern

def unroll():
    pass

def expand_reference():
    pass

if __name__ == '__main__':
    pat = open('../scarf-beginner.txt', 'r')
    # pat = open('../scarf-intermediate.txt', 'r')
    # pat = open('../scarf-advanced.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    parse(pat_lines)