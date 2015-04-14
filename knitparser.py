from os.path import join
import re
from sys import path

path.append(join('.', 'classes'))
from annotation import *
from pattern import *
from repeat import *
from row import *

CHARS_TO_STRIP = '.,;: '

####################
# Regex's for rows #
####################

ROW_REGEX = '(row|round) \d+( [\(\[](ws|rs)[\)\]])?:'
IN_ROW_REPEAT_REGEX = '.*\*.*rep(eat)? from \*'

#######################
# Regex's for repeats #
#######################

REPEAT_ROWS_REGEX = 'rep(eat)? rows'
EVERY_OTHER_REGEX = 'row \d+ and all'
REPEAT_REGEX = REPEAT_ROWS_REGEX + '|' + EVERY_OTHER_REGEX


def parse(pattern_text):
    pattern_text = pattern_text.splitlines()
    pattern_tree = Pattern(pattern_text[0])

    for line in pattern_text[1:]:
        if line.strip():
            pattern_tree += parse_line(line, pattern_tree)

    return pattern_tree

def parse_line(line, pattern_tree):
    if re.search(REPEAT_REGEX, line, re.IGNORECASE):
        return parse_repeat_dispatcher(line, pattern_tree)

    if re.search(ROW_REGEX, line, re.IGNORECASE):
        return parse_row(line)

    return Annotation(line)

def parse_row(line):
    row_instructions = line[line.index(':') + 2 :]

    number = find_first_num(line)

    side = None
    if re.search('rs|right side', line, re.IGNORECASE):
        side = 'RS'
    elif re.search('ws|wrong side', line, re.IGNORECASE):
        side = 'WS'

    row = Row([Annotation(row_instructions)], number, side)

    if re.search(IN_ROW_REPEAT_REGEX, line, re.IGNORECASE):
        return parse_in_row_repeat(row_instructions, number)

    return row

def parse_in_row_repeat(line, row_number):
    row_components = []

    instructions_before_repeat = line[: line.index('*')].strip(CHARS_TO_STRIP)
    if instructions_before_repeat:
        row_components.append(Annotation(instructions_before_repeat))

    rep_start = line.index('*') + 1
    rep_end = line.lower().index('rep')
    repeated_section = line[rep_start : rep_end].strip(CHARS_TO_STRIP)

    instructions_after_repeat = line[line.rindex('*') + 1 :].strip(CHARS_TO_STRIP)
    final_component = None
    until = None

    if instructions_after_repeat.startswith('to'):
        until = instructions_after_repeat[len('to') :]
        if 'repeat' in until:
            split_index = until.index('repeat')

            instructions_after_repeat = until[split_index + len('repeat') :]
            instructions_after_repeat = instructions_after_repeat.strip(CHARS_TO_STRIP)

            until = until[: split_index]

            final_component = InRowRepeat(Annotation(instructions_after_repeat))

    elif instructions_after_repeat.startswith('across'):
        until = 'across'

        instructions_after_repeat = instructions_after_repeat[len('across') :]
        instructions_after_repeat = instructions_after_repeat.lstrip(CHARS_TO_STRIP)
        instructions_after_repeat = instructions_after_repeat.strip(CHARS_TO_STRIP)

        final_component = Annotation(instructions_after_repeat)

    elif 'more' in instructions_after_repeat:
        split_index = instructions_after_repeat.index('more') + len('more')

        until = instructions_after_repeat[: split_index]

        instructions_after_repeat = instructions_after_repeat[split_index :]
        instructions_after_repeat = instructions_after_repeat.lstrip(CHARS_TO_STRIP)
        instructions_after_repeat = instructions_after_repeat.strip(CHARS_TO_STRIP)

        final_component = Annotation(instructions_after_repeat)

    else:
        until = instructions_after_repeat

    until = until.strip(CHARS_TO_STRIP)

    row_components.append(InRowRepeat(Annotation(repeated_section), until))

    if final_component:
        row_components.append(final_component)

    return Row(row_components, row_number)

def parse_repeat_dispatcher(line, pattern_tree):
    match = re.search(EVERY_OTHER_REGEX, line, re.IGNORECASE)
    if match:
        return parse_repeat_every_other(line, match)

    match = re.search(REPEAT_ROWS_REGEX, line, re.IGNORECASE)
    if match:
        return parse_repeat(line, match, pattern_tree)

    return None

def parse_repeat(line, match, pattern_tree):
    start, end = match.span()
    nums_before = find_all_nums(line[: start])
    nums_after = find_all_nums(line[end :])

    if len(nums_before) == 2 and len(nums_after) == 2:
        repeat_start, repeat_end = nums_before
        ref_start, ref_end = nums_after
        num_in_repeat = repeat_end - repeat_start + 1
        num_in_ref = ref_end - ref_start + 1

        times = num_in_repeat/num_in_ref
        
        if times == 1:
            parsed_rows = [Reference(pattern_tree.get_row(i), pattern_tree.next_row_number + i - ref_start) for i in range(ref_start, ref_end + 1)]
            return parsed_rows
        
        parsed_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
        return Repeat(parsed_rows, repeat_start, num_in_repeat/num_in_ref)
    
    elif len(nums_before) == 1 and nums_after[-1] - nums_after[0] + 1 == nums_before[0]:
        ref_start, ref_end = nums_after[0], nums_after[-1]
        times = nums_before[0]/(ref_end - ref_start + 1)
        if times == 1:
            parsed_rows = [Reference(pattern_tree.get_row(i), pattern_tree.next_row_number + i - ref_start) for i in range(ref_start, ref_end + 1)]
            return parsed_rows

        repeated_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
        return Repeat(repeated_rows, pattern_tree.next_row_number - nums_before[0], times)

    elif len(nums_before) == 0 and len(nums_after) == 2:
        ref_start, ref_end = nums_after[0], nums_after[-1]
        repeated_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
        return [Repeat(repeated_rows, ref_start), Annotation(line[line.index('for') :].strip('.;,:'))]

    return Repeat([Annotation(line)], pattern_tree.next_row_number)
    
def parse_repeat_every_other(line, match):
    # TODO: add rs/ws
    header, body = line[:line.index(':')], line[line.index(':') + 1 :].strip('.,:;')
    number = find_all_nums(header)[0]
    row = Row([Annotation(body)], number)

    if 'odd' in line:
        return Repeat([row], row.number, 'odd')
    if 'even' in line:
        return Repeat([row], row.number, 'even')
    if 'rs' in line or 'right side' in line:
        return Repeat([row], row.number, 'RS')
    if 'ws' in line or 'wrong side' in line:
        return Repeat([row], row.number, 'WS')
    return Repeat([Annotation(line)], row.number)

def unroll():
    pass

def expand_reference():
    pass

def find_all_nums(line):
    nums = [num for num in line.replace('-', ' ').split(' ') if re.search('\d+', num)]
    # removes curly quote
    # TODO: remove not-curly quote and inches etc.
    nums = [num for num in nums if '\xe2\x80\x9d' not in num]
    nums = [int(''.join([char for char in num if char.isdigit()])) for num in nums]
    return nums

def find_first_num(line):
    for num in line.replace('-', ' ').split(' '):
        num = num.strip(':,;."')
        if re.match('\d+', num):
            return int(num)

    raise Exception('Line does not contain number:', line)

if __name__ == '__main__':
    # pat = open('tests/test_files/scarf-beginner.txt', 'r')
    # pat = open('tests/test_files/scarf-intermediate.txt', 'r')
    # pat = open('tests/test_files/scarf-advanced.txt', 'r')
    # pat_lines = pat.read()
    # pat.close()
    # print pat_lines
    # TODO: take file specified by command line arg
    parse(pat_lines)