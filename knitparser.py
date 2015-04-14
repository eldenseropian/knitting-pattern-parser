from os.path import join
import re
from sys import path, argv

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
    """Parse a knitting pattern into an AST.

    Keyword arguments:
    pattern_text -- the text of the pattern to parse, as a single string

    Returns a Pattern instance.
    """

    if type(pattern_text) is not str:
        raise TypeError('pattern_text must be a non-empty string.')
    if not pattern_text.strip():
        raise ValueError('pattern_text must be a non-empty string.')

    pattern_text = pattern_text.splitlines()
    title = pattern_text[0]
    pattern_tree = Pattern(title)

    for line in pattern_text[1:]:
        if line.strip(): # ignore blank lines
            pattern_tree += parse_line(line, pattern_tree)

    return pattern_tree

def parse_line(line, pattern_tree):
    """Parse a single line of a knitting pattern.

    Keyword arguments:
    line -- the line to parse (a string)
    pattern_tree -- the pattern as parse up to line (a Pattern instance)

    Returns a leaf of the Pattern AST representing the given line.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')
    if pattern_tree.__class__ is not Pattern:
        raise TypeError('pattern_tree must be a Pattern instance.')

    if re.search(ROW_REGEX, line, re.IGNORECASE):
        return parse_row(line)

    if re.search(REPEAT_REGEX, line, re.IGNORECASE):
        return parse_repeat_dispatcher(line, pattern_tree)

    return Annotation(line)

def parse_row(line):
    """Parse a single line that represents a row.

    Keyword arguments:
    line -- the line to parse (a string)

    Returns a Row instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')

    row_instructions = line[line.index(':') + 2 :]

    number = _find_first_num(line)

    side = None
    if re.search('rs|right side', line, re.IGNORECASE):
        side = 'RS'
    elif re.search('ws|wrong side', line, re.IGNORECASE):
        side = 'WS'

    row = Row([Annotation(row_instructions)], number, side)

    if re.search(IN_ROW_REPEAT_REGEX, line, re.IGNORECASE):
        return parse_in_row_repeat(row_instructions, number, side)

    return row

def parse_in_row_repeat(line, row_number, side):
    """Parse a single line that represents a row that contains a repeated section.

    Keyword arguments:
    line -- the line to parse (a string)
    row_number -- the number of the row being parsed_rows
    side - the side of the piece the row is on ('RS', 'WS', or None)

    Returns a Row instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')
    if type(row_number) is not int:
        raise TypeError('row_number must be a positive integer.')
    if row_number <= 0:
        raise ValueError('row_number must be a positive integer.')
    if side not in ['RS', 'WS', None]:
        raise ValueError('side must be one of ["RS", "WS", None].')

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

    return Row(row_components, row_number, side)

def parse_repeat_dispatcher(line, pattern_tree):
    """Parse an instruction to repeat rows.

    Keyword arguments:
    line -- the line to parse (a string)
    pattern_tree -- the pattern as parse up to line (a Pattern instance)

    Returns a Repeat instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')
    if pattern_tree.__class__ is not Pattern:
        raise TypeError('pattern_tree must be a Pattern instance.')

    match = re.search(EVERY_OTHER_REGEX, line, re.IGNORECASE)
    if match:
        return parse_repeat_every_other(line, match)

    match = re.search(REPEAT_ROWS_REGEX, line, re.IGNORECASE)
    if match:
        return parse_repeat(line, match, pattern_tree)

    raise RuntimeError('Failed to parse repeat: ' + line)

def parse_repeat(line, match, pattern_tree):
    """Parse an instruction to repeat rows that is not in an every-other-row fashion.

    Keyword arguments:
    line -- the line to parse (a string)
    match -- the re.MatchObject returned by matching line with REPEAT_REGEX
    pattern_tree -- the pattern as parse up to line (a Pattern instance)

    Returns a Repeat instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')
    if match.__class__.__name__ != 'SRE_Match':
        raise TypeError('match must be an re.MatchObject.')
    if pattern_tree.__class__ is not Pattern:
        raise TypeError('pattern_tree must be a Pattern instance.')

    start, end = match.span()
    nums_before = _find_all_nums(line[: start])
    nums_after = _find_all_nums(line[end :])

    if len(nums_before) == 0 and len(nums_after) == 2:
        # Repeats of the form 'Rep Rows a through b indefinitely'
        ref_start, ref_end = nums_after
        parsed_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
        instructions_after_repeat = line[line.index('for') :].strip(CHARS_TO_STRIP)
        return [Repeat(parsed_rows, ref_start), Annotation(instructions_after_repeat)]
    
    if len(nums_after) == 2:
        # Repeats of the form 'Rep Rows a and b over a specified range'

        ref_start, ref_end = nums_after
        num_in_ref = ref_end - ref_start + 1

        # Next n rows: Rep Rows a and b
        num_in_repeat = nums_before[0]
        if len(nums_before) == 2:
            # Rows x - y: Rep Rows a and b
            num_in_repeat = nums_before[1] - nums_before[0] + 1

        times = num_in_repeat / num_in_ref

        if times == 1:
            # Repeats of the form 'Rows x - y: Repeat rows a and b'
            parsed_rows = []
            for i in range(ref_start, ref_end + 1):
                row_number = pattern_tree.next_row_number + i - ref_start
                parsed_rows.append(Reference(pattern_tree.get_row(i), row_number))
            return parsed_rows

        repeat_start = nums_before[0]
        parsed_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
        return Repeat(parsed_rows, repeat_start, times)

    return Repeat([Annotation(line)], pattern_tree.next_row_number)
    
def parse_repeat_every_other(line, match):
    """Parse an instruction to repeat a row every other row.

    Keyword arguments:
    line -- the line to parse (a string)
    match -- the re.MatchObject returned by matching line with REPEAT_REGEX

    Returns a Repeat instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')
    if match.__class__.__name__ != 'SRE_Match':
        raise TypeError('match must be an re.MatchObject.')

    which_rows = line[:line.index(':')]
    instructions = line[line.index(':') + 1 :].strip(CHARS_TO_STRIP)

    number = _find_first_num(which_rows)
    row = Row([Annotation(instructions)], number)

    if 'odd' in line:
        return Repeat([row], row.number, 'odd')
    if 'even' in line:
        return Repeat([row], row.number, 'even')
    if 'rs' in line or 'right side' in line:
        return Repeat([row], row.number, 'RS')
    if 'ws' in line or 'wrong side' in line:
        return Repeat([row], row.number, 'WS')

    raise Exception('Failed to parse as repeated on every other row: ' + line)

def unroll():
    pass

def expand_reference():
    pass

def _find_all_nums(line):
    """Return a list of all integers in a string.

    Returns an empty list if the string contains no integers.
    """

    if type(line) is not str:
        raise TypeError('line must be a string.')

    nums = [num for num in line.replace('-', ' ').split(' ') if re.search('\d+', num)]
    nums = [int(''.join([char for char in num if char.isdigit()])) for num in nums]
    return nums

def _find_first_num(line):
    """Return the first integer in a string.

    Raises an exception if the string contains no integers.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')

    for num in line.replace('-', ' ').split(' '):
        num = num.strip(':,;."')
        if re.match('\d+', num):
            return int(num)

    raise Exception('Line does not contain number:', line)

if __name__ == '__main__':
    """Parse a knitting pattern in a text file specified by the command-line argument."""

    if len(argv) != 2:
        raise Exception('knitparser must be called with the name of a pattern file to read')
    pat = open(argv[1])
    pat_lines = pat.read()
    pat.close()
    print parse(pat_lines)