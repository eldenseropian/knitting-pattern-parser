import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestRepeatInitialization(unittest.TestCase):
    """Test repeat constructor constraints."""

    def test_initialize_with_non_list(self):
        self.assertRaises(TypeError, Repeat, 2, 1)

    def test_initialize_with_empty_list(self):
        self.assertRaises(ValueError, Repeat, [], 1)

    def test_intialize_with_list_with_illegal_components(self):
        self.assertRaises(TypeError, Repeat, [Annotation('yay'), 'boo'], 1)

    def test_initialize_with_non_int_start(self):
        self.assertRaises(TypeError, Repeat, [Annotation('yay')], 'cat')

    def test_intialize_with_negative_start(self):
        self.assertRaises(ValueError, Repeat, [Annotation('yay')], -5)

    def test_intialize_with_zero_start(self):
        self.assertRaises(ValueError, Repeat, [Annotation('yay')], 0)

    def test_initialize_with_non_int_or_string_times(self):
        self.assertRaises(TypeError, Repeat, [Annotation('yay')], 1, Annotation('boo'))

    def test_intialize_with_zero_times(self):
        self.assertRaises(ValueError, Repeat, [Annotation('yay')], 1, 0)

    def test_intialize_with_negative_times(self):
        self.assertRaises(ValueError, Repeat, [Annotation('yay')], 1, -5)

class TestRepeatParsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_single_repeat(self):
        pattern = 'Rows 9 and 10: Rep Rows 7 and 8 once more.'

        pattern_tree = Pattern('Test Pattern')
        pattern_tree += Row([Annotation('a')], 7)
        pattern_tree += Row([Annotation('a')], 8)

        tree = [
            Reference(Row([Annotation('a')], 7)),
            Reference(Row([Annotation('a')], 8)),
        ]

        parsed_tree = knitparser.parse_repeat(pattern, re.search(knitparser.REPEAT_ROWS_REGEX, pattern, re.IGNORECASE), pattern_tree)

        self.assertEqual(tree, parsed_tree)

    def test_multiple_repeat(self):
        pattern = 'Rows 17 - 22: Rep Rows 15 and 16 three times more.'

        pattern_tree = Pattern('Test Pattern')
        pattern_tree += Row([Annotation('a')], 15)
        pattern_tree += Row([Annotation('a')], 16)

        tree = Repeat([
            Reference(Row([Annotation('a')], 15)),
            Reference(Row([Annotation('a')], 16)),
        ], 17, 3)

        parsed_tree = knitparser.parse_repeat(pattern, re.search(knitparser.REPEAT_ROWS_REGEX, pattern, re.IGNORECASE), pattern_tree)
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()