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

class TestRepeatFunctions(unittest.TestCase):
    """Test the functions of the repeat class."""

    def setUp(self):
        self.annotation1 = Annotation('Knit 5')
        self.repeat1 = Repeat([self.annotation1], 1, 3)

        self.annotation2 = Annotation('Purl 5')
        self.repeat2 = Repeat([self.annotation2], 4)

    def test_str(self):
        str1 = '<repeat start="1" times="3">' + self.annotation1.__str__() + '</repeat>'
        self.assertEqual(str1, self.repeat1.__str__())

        str2 = '<repeat start="4">' + self.annotation2.__str__() + '</repeat>'
        self.assertEqual(str2, self.repeat2.__str__())

    def test_eq(self):
        self.assertTrue(self.repeat1 == self.repeat1)
        self.assertTrue(self.repeat1 == Repeat([self.annotation1], 1, 3))
        self.assertTrue(self.repeat2 == self.repeat2)
        self.assertTrue(self.repeat2 == Repeat([Annotation('Purl 5')], 4))

        self.assertFalse(self.repeat1 == self.repeat2)
        self.assertFalse(self.repeat1 == Repeat([self.annotation1], 1))

class TestRepeatParsing(unittest.TestCase):
    """Test parsing repeats out of the context of a pattern."""

    def setUp(self):
        self.pattern_tree = Pattern('Test Pattern')
        self.row7 = Row([Annotation('Knit')], 7)
        self.row8 = Row([Annotation('Purl')], 8)
        self.pattern_tree += self.row7
        self.pattern_tree += self.row8

        self.repeat_one_time_tree = [
            Reference(self.row7),
            Reference(self.row8),
        ]

    def test_repeat_one_time(self):
        pattern = 'Rows 9 and 10: Rep Rows 7 and 8 once more.'
        parsed_tree = knitparser.parse_repeat(pattern, self.pattern_tree)
        self.repeat_one_time_tree[0].number = 9
        self.repeat_one_time_tree[1].number = 10
        self.assertEqual(self.repeat_one_time_tree, parsed_tree)

        pattern = 'Rows 23 and 24: Rep Rows 7 and 8.'
        parsed_tree = knitparser.parse_repeat(pattern, self.pattern_tree)
        self.repeat_one_time_tree[0].number = 23
        self.repeat_one_time_tree[1].number = 24
        self.assertEqual(self.repeat_one_time_tree, parsed_tree)

        pattern = 'Next 2 Rows: Rep Rows 7 and 8.'
        self.pattern_tree.next_row_number = 9
        parsed_tree = knitparser.parse_repeat(pattern, self.pattern_tree)
        self.repeat_one_time_tree[0].number = 9
        self.repeat_one_time_tree[1].number = 10
        self.assertEqual(self.repeat_one_time_tree, parsed_tree)

    def test_multiple_repeat(self):
        pattern = 'Rows 17 - 22: Rep Rows 15 and 16 three times more.'

        pattern_tree = Pattern('Test Pattern')
        pattern_tree += Row([Annotation('a')], 15)
        pattern_tree += Row([Annotation('a')], 16)

        tree = Repeat([
            Reference(Row([Annotation('a')], 15)),
            Reference(Row([Annotation('a')], 16)),
        ], 17, 3)

        parsed_tree = knitparser.parse_repeat(pattern, pattern_tree)
        self.assertEqual(tree, parsed_tree)

    def test_repeat_every_other(self):
        pattern = 'Row 2 and all even-numbered rows: Purl all sts.'
        expected_tree = Repeat([Row([Annotation('Purl all sts')], 2)], 2, 'even')
        parsed_tree = knitparser.parse_repeat_every_other(pattern)

        self.assertEqual(expected_tree, parsed_tree)

        pattern = 'Row 1 and all odd # rows: K2, purl to last two sts, k2.'
        expected_tree = Repeat([Row([Annotation('K2, purl to last two sts, k2')], 1)], 1, 'odd')
        parsed_tree = knitparser.parse_repeat_every_other(pattern)
        self.assertEqual(expected_tree, parsed_tree)

        pattern = 'Row 1 and all wrong side rows: Purl.'
        expected_tree = Repeat([Row([Annotation('Purl')], 1)], 1, 'WS')
        parsed_tree = knitparser.parse_repeat_every_other(pattern)
        self.assertEqual(expected_tree, parsed_tree)

        pattern = 'Row 2 and all RS rows: Knit.'
        expected_tree = Repeat([Row([Annotation('Knit')], 2)], 2, 'RS')
        parsed_tree = knitparser.parse_repeat_every_other(pattern)
        self.assertEqual(expected_tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()