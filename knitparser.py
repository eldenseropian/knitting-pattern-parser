import os
import re
import sys

sys.path.append(os.path.join('.', 'classes'))
from annotation import *
from pattern import *
from row import *
from section import *

LABEL_REGEX = '(Row\s|Round\s)'
SIDE_REGEX = '(\s\(WS\)|\s\(RS\))?'
NUMBER_REGEX = '\d+'
END_REGEX = '[\.:]?'
ROW_REGEX = re.compile(LABEL_REGEX + NUMBER_REGEX + SIDE_REGEX + END_REGEX)

def parse(pattern):
    pattern = pattern.splitlines()
    lines = []
    title = pattern[0]
    for line in pattern[1:]:
        match = re.match(ROW_REGEX, line)
        if match:
            start, length = match.span()
            header = line[start : start + length]
            header = header.replace('.', '')
            header = header.replace(':', '')
            header = header.replace('Row', '')
            header = header.replace('Round', '')
            header = header.split()
            text = line[start + length + 1 :]
            lines.append(Row([Annotation(text)], int(header[0])))
        elif line:
            lines.append(Annotation(line))
    pattern_section = Section(lines)
    pattern = Pattern(title, [pattern_section])
    print pattern
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