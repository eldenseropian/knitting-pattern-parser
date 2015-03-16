import os
import re
import sys

sys.path.append(os.path.join('.', 'classes'))
from annotation import *
from pattern import *
from repeat import *
from row import *
from section import *

LABEL_REGEX = '(Row(s)?\s|Round(s)?\s)'
SIDE_REGEX = '(\s\(WS\)|\s\(RS\))?'
NUMBER_REGEX = '\d+'
END_REGEX = '[\.:]?'
ROW_REGEX = re.compile(LABEL_REGEX + NUMBER_REGEX + SIDE_REGEX + END_REGEX)
REPEAT_REGEX = re.compile('.*Rep|Repeat')

def parse(pattern):
    pattern = pattern.splitlines()
    components = []
    title = pattern[0]
    for line in pattern[1:]:
        if line:
            match = re.match(REPEAT_REGEX, line)
            if match:
                components.append(parse_repeat(line, match))
            else:
                match = re.match(ROW_REGEX, line)
                if match:
                    components.append(parse_row(line, match))
                else:
                    components.append(Annotation(line))

    pattern_section = Section(components)
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

def parse_repeat(line, match):
    start, length = match.span()
    nums_before = find_all_nums(line[start : start + length])
    nums_after = find_all_nums(line[start + length :])
    if len(nums_before) == len(nums_after):
        rows = [Row(None, nums_before[i], nums_after[i]) for i in range(len(nums_before))]
        # TODO: arbitrary number of times
        return Repeat(rows, 1)
    # TODO: figure out other cases
    return Repeat([Annotation('a')], 1)
    print line, match.span(), line[match.span()[0]:match.span()[1]], nums_before, nums_after
    

def unroll():
    pass

def expand_reference():
    pass

def find_all_nums(line):
    nums = [num for num in line.split(' ') if re.match(NUMBER_REGEX, num)]
    # removes curly quote
    # TODO: remove not-curly quote and inches etc.
    nums = [num for num in nums if '\xe2\x80\x9d' not in num]
    nums = [int(''.join([char for char in num if char.isdigit()])) for num in nums]
    return nums

if __name__ == '__main__':
    # pat = open('tests/test_files/scarf-beginner.txt', 'r')
    pat = open('tests/test_files/scarf-intermediate.txt', 'r')
    # pat = open('tests/test_files/scarf-advanced.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    parse(pat_lines)