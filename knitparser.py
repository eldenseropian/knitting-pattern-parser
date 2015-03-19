import os
import re
import sys

sys.path.append(os.path.join('.', 'classes'))
from annotation import *
from pattern import *
from repeat import *
from row import *

LABEL_REGEX = '(Row(s)?\s|Round(s)?\s)'
SIDE_REGEX = '(\s\(WS\)|\s\(RS\))?'
NUMBER_REGEX = '\d+'
END_REGEX = '[\.:]?'
ROW_REGEX = re.compile(LABEL_REGEX + NUMBER_REGEX + SIDE_REGEX + END_REGEX)
REPEAT_REGEX = re.compile('.*[rR]ep\s[rR]ows|[rR]epeat\s[rR]ows')
EVERY_OTHER_REGEX = re.compile('.*and all.{,15}rows')
IN_ROW_REPEAT_REGEX = re.compile('.*\*.*[rR]ep(eat)? from \*')

def parse(pattern):
    pattern = pattern.splitlines()
    components = []
    rows = {
        'next_row': 1
    }
    title = pattern[0]
    for line in pattern[1:]:
        if line.strip():
            match = re.match(IN_ROW_REPEAT_REGEX, line)
            if match:
                new_row = parse_in_row_repeat(line, match)
                components.append(new_row)
                rows[new_row.number] = new_row
                rows['next_row'] = new_row.number + 1
            else:
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
                            rows['next_row'] = new_row.number + 1
                        elif 'row:' in line.lower():
                            new_row = Row([Annotation(line[line.lower().index('row:') + len('row:') :].strip())], rows['next_row'])
                            components.append(new_row)
                            rows[new_row.number] = new_row
                            rows['next_row'] = new_row.number + 1
                        else:
                            components.append(Annotation(line))

    pattern = Pattern(title, components)
    # print pattern
    return pattern

def parse_row(line, match):
    start, length = match.span()
    header = line[start : start + length]
    header = re.sub(LABEL_REGEX, '', header)
    header = re.sub(END_REGEX, '', header)
    header = header.split()
    text = line[start + length + 1 :]
    row_num = int(header[0])
    side = None
    if 'RS' in line.upper() or 'right side' in line.lower():
        side = 'RS'
    if 'WS' in line.upper() or 'wrong side' in line.lower():
        side = 'WS'
    row = Row([Annotation(text)], row_num, side)
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
            parsed_rows = [Reference(rows[i], rows['next_row'] + i - ref_start) for i in range(ref_start, ref_end + 1)]
            rows['next_row'] = repeat_end + 1
            return parsed_rows
        
        rows['next_row'] = repeat_end + 1
        parsed_rows = [Reference(rows[i]) for i in range(ref_start, ref_end + 1)]
        return Repeat(parsed_rows, repeat_start, num_in_repeat/num_in_ref)
    
    elif len(nums_before) == 1 and nums_after[-1] - nums_after[0] + 1 == nums_before[0]:
        ref_start, ref_end = nums_after[0], nums_after[-1]
        times = nums_before[0]/(ref_end - ref_start + 1)
        if times == 1:
            parsed_rows = [Reference(rows[i], rows['next_row'] + i - ref_start) for i in range(ref_start, ref_end + 1)]
            rows['next_row'] += nums_before[0]
            return parsed_rows

        rows['next_row'] += nums_before[0]
        repeated_rows = [Reference(rows[i]) for i in range(ref_start, ref_end + 1)]
        return Repeat(repeated_rows, rows['next_row'] - nums_before[0], times)
    rows['next_row'] += 1
    return Repeat([Annotation(line)], rows['next_row'] - 1)
    
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

"""
Row 5: With A, * k8, yo, sl next st purlwise, k1, rep from * twice more, k7.
"""

def parse_in_row_repeat(line, match):
    start, length = match.span()
    rep_start = line.index('*')
    beg = line[line.index(':') + 1 : line.index('*')].strip(',;:. ')
    row_number = find_all_nums(line[:rep_start])[0]
    subtract = len('rep from *')
    if 'repeat' in line.lower():
        subtract = len('repeat from *')
    repeated_section = line[rep_start + 1 : start + length - subtract].strip(',.:; ')
    end = line[start+length :]
    if 'rep' in end:
        until = end[: end.index('repeat')].strip().strip(',')

        if until.startswith('to'):
            until = until[2:].strip()
        return Row([
            InRowRepeat([Annotation(repeated_section)], until),
            InRowRepeat([Annotation(end[end.index('repeat') + len('repeat') :])])
        ], row_number)
    if 'across' in end:
        other_instructions = end[end.index('across') + len('across') :].lstrip(';:. ').strip(',:. ')
        return Row([
            InRowRepeat([Annotation(repeated_section)], 'across'),
            Annotation(other_instructions)],
        row_number)
    if 'to' in end:
        until = end[end.index('to') + len('to') :].strip(' .')
        if beg:
            return Row([
                Annotation(beg),
                InRowRepeat([Annotation(repeated_section)], until),
            ], row_number)
        return Row([
            InRowRepeat([Annotation(repeated_section)], until),
        ], row_number)
    if 'more' in end:
        until = end[: end.index('more') + len('more')].strip()
        other_instructions = end[end.index('more') + len('more') :].lstrip(' ,').strip('.')
        if beg:
            return Row([
                Annotation(beg),
                InRowRepeat([Annotation(repeated_section)], until),
                Annotation(other_instructions)
            ], row_number)
        return Row([
            InRowRepeat([Annotation(repeated_section)], until),
            Annotation(other_instructions)
        ], row_number)
    if beg:
        return Row([
            Annotation(beg),
            InRowRepeat([Annotation(repeated_section)], end)
        ], row_number)
    return Row([InRowRepeat([Annotation(repeated_section)], end)], row_number)


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
    # print pat_lines
    parse(pat_lines)