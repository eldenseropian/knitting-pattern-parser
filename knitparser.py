from os.path import join
import re
from sys import path, argv

path.append(join('.', 'classes'))
from annotation import *
from pattern import *
from repeat import *
from row import *

CHARS_TO_STRIP = '.,;:* '

####################
# Regex's for rows #
####################

ROW_REGEX = '(row|round) \d+.*:'
ASTERISK_REPEAT = '\*.*rep(eat)?.*\*'
BRACKET_REPEAT = '\[.*\] rep(eat)?'
IN_ROW_REPEAT_REGEX = ASTERISK_REPEAT + '|' + BRACKET_REPEAT

#######################
# Regex's for repeats #
#######################

# 1 or 2 numbers before repeat, two numbers after repeat
NOT_DIGITS = '[^\d]*'
_BEFORE_REPEAT = '^' + NOT_DIGITS + '\d*' + NOT_DIGITS + '\d+' + NOT_DIGITS
_AFTER_REPEAT = NOT_DIGITS + '\d+' + NOT_DIGITS + '\d+' + NOT_DIGITS + '$'
REPEAT_ROWS_REGEX = _BEFORE_REPEAT + 'rep(eat)? rows' + _AFTER_REPEAT

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

    if re.search(REPEAT_REGEX, line, re.IGNORECASE):
        return parse_repeat_dispatcher(line, pattern_tree)

    if re.search(ROW_REGEX, line, re.IGNORECASE):
        return parse_row(line)

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
        return Row(parse_in_row_repeat(row_instructions), number, side)

    return row

def parse_in_row_repeat(line):
    """Parse text that contains a repeated section.

    Recursively parses nested repeats.

    Keyword arguments:
    line -- the line to parse (a string)

    Returns a list of parsed components.
    """

    line = line.replace(';', ',') #TODO: handle better

    match = re.search(IN_ROW_REPEAT_REGEX, line, re.IGNORECASE)
    if not match:
        return [Annotation(line.strip(CHARS_TO_STRIP))]

    start = match.span()[0]
    components = []
    if start != 0:
        for component in parse_in_row_repeat(line[:start]):
            components.append(component)
        line = line[start:]

    asterisk = False
    if re.search(ASTERISK_REPEAT, line, re.IGNORECASE):
        asterisk = True
        # Asterisk repeats cannot have siblings
        # Bracket repeats cannot have nesting

    end = None
    if asterisk:
        end = line[:line.rindex('*')].lower().rindex('rep')
    else:
        end = line.index(']')

    # TODO: delims standardization
    true_end = len(line)
    if ',' in line[end:]:
        true_end = len(line[:end]) + line[end:].index(',')

    if asterisk:
        until = line[end:true_end].strip(CHARS_TO_STRIP)
        if 'across' in until:
            until = 'across'
        elif 'to' in until:
            until = until[until.index('to') + 3 :]
        elif 'more' in until:
            until = until[until.index('*') :].strip(CHARS_TO_STRIP)
        if until is not None and not until.strip():
            until = None
    else:
        strip = len(' rep')
        if 'eat' in line[end:]:
            strip += 4
        until = line[end + strip:true_end].strip(CHARS_TO_STRIP)
        
    inner = parse_in_row_repeat(line[1: end])
    components.append(InRowRepeat(inner, until))

    if len(line[true_end:].strip(CHARS_TO_STRIP)) > 0:
        for component in parse_in_row_repeat(line[true_end:].strip(CHARS_TO_STRIP)):
            components.append(component)
    return components

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

    if re.search(EVERY_OTHER_REGEX, line, re.IGNORECASE):
        return parse_repeat_every_other(line)

    if re.search(REPEAT_ROWS_REGEX, line, re.IGNORECASE):
        return parse_repeat(line, pattern_tree)

    raise RuntimeError('Failed to parse repeat: ' + line)

def parse_repeat(line, pattern_tree):
    """Parse an instruction to repeat rows that is not in an every-other-row fashion.

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

    split_index = line.lower().index('rep')
    nums_before = _find_all_nums(line[: split_index])
    nums_after = _find_all_nums(line[split_index :])

    ref_start, ref_end = nums_after
    num_in_ref = ref_end - ref_start + 1

    # Next n rows: Rep Rows a - b
    num_in_repeat = nums_before[0]
    if len(nums_before) == 2:
        # Rows x - y: Rep Rows a - b
        num_in_repeat = nums_before[1] - nums_before[0] + 1

    times = num_in_repeat / num_in_ref

    if times == 1:
        # Repeats of the form 'Rows n and n+1: Repeat rows a and b'
        parsed_rows = []
        for i in range(ref_start, ref_end + 1):
            row_number = pattern_tree.next_row_number + i - ref_start
            parsed_rows.append(Reference(pattern_tree.get_row(i), row_number))
        return parsed_rows

    repeat_start = nums_before[0]
    parsed_rows = [Reference(pattern_tree.get_row(i)) for i in range(ref_start, ref_end + 1)]
    return Repeat(parsed_rows, repeat_start, times)

def parse_repeat_every_other(line):
    """Parse an instruction to repeat a row every other row.

    Keyword arguments:
    line -- the line to parse (a string)

    Returns a Repeat instance.
    """

    if type(line) is not str:
        raise TypeError('line must be a non-empty string.')
    if not line.strip():
        raise ValueError('line must be a non-empty string.')

    which_rows = line[:line.index(':')]
    instructions = line[line.index(':') + 1 :].strip(CHARS_TO_STRIP)

    number = _find_first_num(which_rows)
    row = Row([Annotation(instructions)], number)

    # Case matters: 'ws' will be in most of these lines (from 'rows')
    if 'odd' in line:
        return Repeat([row], row.number, 'odd')
    if 'even' in line:
        return Repeat([row], row.number, 'even')
    if 'RS' in line or 'right side' in line:
        return Repeat([row], row.number, 'RS')
    if 'WS' in line or 'wrong side' in line:
        return Repeat([row], row.number, 'WS')

    raise Exception('Failed to parse as repeated on every other row: ' + line)

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
    parsed = parse(pat_lines)
    import xml.dom.minidom
    print xml.dom.minidom.parseString(parsed.__str__().replace('&', '&amp;')).toprettyxml(indent='    ')
