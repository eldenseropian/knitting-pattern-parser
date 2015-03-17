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
REPEAT_REGEX = re.compile('.*[rR]ep\s[rR]ows|[rR]epeat\s[rR]ows')
EVERY_OTHER_REGEX = re.compile('.*and all')

def parse(pattern):
    pattern = pattern.splitlines()
    components = []
    rows = {
        'count': 0
    }
    title = pattern[0]
    for line in pattern[1:]:
        if line.strip():
            match = re.match(EVERY_OTHER_REGEX, line)
            if match:
                components.append(parse_repeat_every_other(line, match))
            else:
                match = re.match(REPEAT_REGEX, line)
                if match:
                    repeated_rows = parse_repeat(line, match, rows)
                    if type(repeated_rows) == list:
                        components.extend(repeated_rows)
                    else:
                        components.append(repeated_rows)
                else:
                    match = re.match(ROW_REGEX, line)
                    if match:
                        new_row = parse_row(line, match)
                        components.append(new_row)
                        rows[new_row.number] = new_row
                        rows['count'] += 1
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
    row_num = int(header[0])
    row = Row([Annotation(text)], row_num)
    return row

def parse_repeat(line, match, rows):
    start, length = match.span()
    nums_before = find_all_nums(line[start : start + length])
    nums_after = find_all_nums(line[start + length :])
    
    if len(nums_before) == 2 and len(nums_after) == 2:
        repeat_start, repeat_end = nums_before
        ref_start, ref_end = nums_after
        num_in_repeat = repeat_end - repeat_start + 1
        num_in_ref = ref_end - ref_start + 1

        times = num_in_repeat/num_in_ref
        
        if times == 1:
            parsed_rows = [Reference(rows[i], rows['count'] + i - ref_start + 1) for i in range(ref_start, ref_end + 1)]
            rows['count'] = repeat_end
            return parsed_rows
        
        rows['count'] = repeat_end
        parsed_rows = [Reference(rows[i]) for i in range(ref_start, ref_end + 1)]
        return Repeat(parsed_rows, repeat_start, num_in_repeat/num_in_ref)
    
    elif len(nums_before) == 1 and nums_after[-1] - nums_after[0] + 1 == nums_before[0]:
        ref_start, ref_end = nums_after[0], nums_after[-1]
        times = nums_before[0]/(ref_end - ref_start + 1)
        if times == 1:
            parsed_rows = [Reference(rows[i], rows['count'] + i - ref_start + 1) for i in range(ref_start, ref_end + 1)]
            rows['count'] += nums_before[0]
            return parsed_rows

        rows['count'] += nums_before[0]
        repeated_rows = [Reference(rows[i]) for i in range(ref_start, ref_end + 1)]
        return Repeat(repeated_rows, rows['count'] - nums_before[0] + 1, times)
    # TODO: figure out other cases
    print 'OTHER:', line
    return Repeat([Annotation(line)], rows['count'])
    
def parse_repeat_every_other(line, match):
    header, body = line[:line.index(':')], line[line.index(':') + 1 :]
    number = find_all_nums(header)[0]
    row = Row([Annotation(body)], number)

    if 'odd' in line.lower():
        return Repeat([row], row.number, 'odd')
    if 'even' in line.lower():
        return Repeat([row], row.number, 'even')
    if 'rs' in line or 'right side' in line.lower():
        return Repeat([row], row.number, 'RS')
    if 'ws' in line or 'wrong side' in line.lower():
        return Repeat([row], row.number, 'WS')
    return Repeat([Annotation(line)], row.number)

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
    # pat = open('tests/test_files/scarf-intermediate.txt', 'r')
    pat = open('tests/test_files/scarf-advanced.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    # print pat_lines
    parse(pat_lines)