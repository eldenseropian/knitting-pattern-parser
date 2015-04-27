"""Unit tests for the pattern class"""

import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestPatternInitialization(unittest.TestCase):
    """Test pattern constructor constraints."""

    def test_initialize_with_non_string_title(self):
        self.assertRaises(TypeError, Pattern, 2)

    def test_initialize_with_empty_title(self):
        self.assertRaises(ValueError, Pattern, '')

    def test_initialize_with_whitespace_title(self):
        self.assertRaises(ValueError, Pattern, '  ')

class TestPatternFunctions(unittest.TestCase):
    """Test the functions of the pattern class."""

    def setUp(self):
        self.pattern = Pattern('Test Pattern')
        self.annotation = Annotation('This is a test pattern.')
        self.row = Row([Annotation('This is the first row.')], 1)
        self.pattern += self.annotation
        self.pattern += self.row

        self.repeat = Repeat([self.annotation], 2)
        self.reference = Reference(self.row)

    def test_str(self):
        expected_str = '<pattern title="Test Pattern">' + self.annotation.__str__() + self.row.__str__() + '</pattern>'
        self.assertEquals(expected_str, self.pattern.__str__())

    def test_eq(self):
        self.assertTrue(self.pattern == self.pattern)

        same_pattern = Pattern('Test Pattern')
        same_pattern += Annotation('This is a test pattern.')
        same_pattern += Row([Annotation('This is the first row.')], 1)

        self.assertTrue(self.pattern == same_pattern)

        different_pattern = Pattern('Test Pattern')
        self.assertFalse(self.pattern == different_pattern)

    def test_get_row(self):
        self.assertEquals(self.row, self.pattern.get_row(1))
        self.assertRaises(ValueError, self.pattern.get_row, 2)

        # TODO: figure out multiple rows with the same number and test that

    def test_is_valid_component(self):
        self.assertTrue(is_valid_component(self.annotation))
        self.assertTrue(is_valid_component(self.row))
        self.assertTrue(is_valid_component(self.reference))
        self.assertTrue(is_valid_component(self.repeat))

        self.assertFalse(is_valid_component(self.pattern))
        self.assertFalse(is_valid_component(InRowRepeat([self.annotation])))

    def test_is_valid_row_component(self):
        self.assertTrue(is_valid_row_component(self.annotation))
        self.assertTrue(is_valid_row_component(InRowRepeat([self.annotation])))

        self.assertFalse(is_valid_row_component(self.pattern))
        self.assertFalse(is_valid_row_component(self.row))
        self.assertFalse(is_valid_row_component(self.reference))
        self.assertFalse(is_valid_row_component(self.repeat))

    def test_is_and_all_repeat(self):
        self.assertTrue(is_and_all_repeat(Repeat([self.annotation], 2, 'even')))
        self.assertTrue(is_and_all_repeat(Repeat([self.annotation], 2, 'odd')))

        self.assertFalse(is_and_all_repeat(Repeat([self.annotation], 2, 'end')))
        self.assertFalse(is_and_all_repeat(self.repeat))

        self.assertFalse(is_and_all_repeat(self.pattern))
        self.assertFalse(is_and_all_repeat(InRowRepeat([self.annotation])))
        self.assertFalse(is_and_all_repeat(self.row))
        self.assertFalse(is_and_all_repeat(self.reference))

    def test_is_annotation(self):
        self.assertTrue(is_annotation(self.annotation))

        self.assertFalse(is_annotation(self.pattern))
        self.assertFalse(is_annotation(InRowRepeat([self.annotation])))
        self.assertFalse(is_annotation(self.row))
        self.assertFalse(is_annotation(self.reference))
        self.assertFalse(is_annotation(self.repeat))

    def test_is_equal_pairwise(self):
        self.assertTrue(is_equal_pairwise([], []))
        self.assertTrue(is_equal_pairwise([self.row], [self.row]))
        self.assertTrue(is_equal_pairwise([self.row, self.annotation], [self.row, self.annotation]))

        self.assertFalse(is_equal_pairwise([self.row], []))
        self.assertFalse(is_equal_pairwise([self.row, self.annotation], [self.row]))
        self.assertFalse(is_equal_pairwise([self.row, self.annotation], [self.annotation, self.row]))
        self.assertFalse(is_equal_pairwise([self.annotation], [self.row]))

#########################################
# See parser_tests.py for parsing tests #
#########################################

if __name__ == '__main__':
    unittest.main()