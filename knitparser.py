import os
import re
import sys

sys.path.append(os.path.join('.', 'classes'))
from annotation import *
from pattern import *
from row import *
from section import *

LABEL_REGEX = '(Row(s)?\s|Round(s)?\s)'
SIDE_REGEX = '(\s\(WS\)|\s\(RS\))?'
NUMBER_REGEX = '\d+'
END_REGEX = '[\.:]?'
ROW_REGEX = re.compile(LABEL_REGEX + NUMBER_REGEX + SIDE_REGEX + END_REGEX)

def parse(pattern):
    pattern = pattern.splitlines()
    lines = []
    title = pattern[0]
    for line in pattern[1:]:
        if line:
            match = re.match(ROW_REGEX, line)
            if match:
                lines.append(parse_row(line, match))
            else:
                lines.append(Annotation(line))

    pattern_section = Section(lines)
    pattern = Pattern(title, [pattern_section])
    print pattern
    return pattern

def parse_row(line, match):
    start, length = match.span()
    header = line[start : start + length]
    header = re.sub(LABEL_REGEX, '', header)
    header = re.sub(END_REGEX, '', header)
    header = header.split()
    text = line[start + length + 1 :]
    return Row([Annotation(text)], int(header[0]))

def unroll():
    pass

def expand_reference():
    pass

if __name__ == '__main__':
    # pat = open('tests/test_files/scarf-beginner.txt', 'r')
    pat = open('tests/test_files/scarf-intermediate.txt', 'r')
    # pat = open('tests/test_files/scarf-advanced.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    parse(pat_lines)