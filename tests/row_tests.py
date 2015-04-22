import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestRowInitialization(unittest.TestCase):
    """Test row constructor constraints."""

    def test_initialize_empty_list(self):
        self.assertRaises(ValueError, Row, [], 2)

    def test_initialize_with_non_list(self):
        self.assertRaises(TypeError, Row, 'Knit', 2)

    def test_initialize_with_non_number(self):
        self.assertRaises(Exception, Row, [Annotation('Knit')], 'Knit')

    def test_initialize_with_list_of_non_annotations(self):
        self.assertRaises(TypeError, Row, ['Knit', 'Purl'], 2)

    def test_initialize_with_not_str_side(self):
        self.assertRaises(ValueError, Row, [Annotation('Knit')], 2, 2)

    def test_initialize_with_illegal_str_side(self):
        self.assertRaises(ValueError, Row, [Annotation('Knit')], 2, 'Knit')

class TestRowFunctions(unittest.TestCase):
    """Test the functions of the row class."""

    def setUp(self):
        self.annotation_1 = Annotation('Knit.')
        self.test_row_1 = Row([self.annotation_1], 1, 'RS')

        self.annotation_2 = Annotation('Purl.')
        self.in_row_repeat = InRowRepeat(Annotation('K1, P1.'))
        self.test_row_2 = Row([self.annotation_2, self.in_row_repeat], 2)

    def test_str(self):
        expected_str = '<row number="1" side="RS">' + self.annotation_1.__str__() + '</row>'
        self.assertEquals(expected_str, self.test_row_1.__str__())

        expected_str = '<row number="2">' + self.annotation_2.__str__() + self.in_row_repeat.__str__() + '</row>'
        self.assertEquals(expected_str, self.test_row_2.__str__())

    def test_eq(self):
        self.assertTrue(self.test_row_1 == self.test_row_1)
        self.assertTrue(self.test_row_1 == Row([self.annotation_1], 1, 'RS'))
        self.assertFalse(self.test_row_1 == self.test_row_2)

class TestRowParsing(unittest.TestCase):
    """Test parsing individual rows outside of the context of a pattern."""

    def test_first_row(self):
        pattern = 'Row 1: Knit 7.'
        row = Row([Annotation('Knit 7.')], 1)
        self.assertEquals(row, knitparser.parse_row(pattern))

        pattern = 'Round 1: Knit 7.'
        row = Row([Annotation('Knit 7.')], 1)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_nth_row(self):
        pattern = 'Row 5: P3, K4'
        row = Row([Annotation('P3, K4')], 5)
        self.assertEquals(row, knitparser.parse_row(pattern))

        pattern = 'Round 25: P3, K4'
        row = Row([Annotation('P3, K4')], 25)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_row_with_multiple_components(self):
        pattern = 'Row 3: K2, *K1, P1*, rep between * to end.'
        row = Row([Annotation('K2'), InRowRepeat(Annotation('K1, P1'), 'end')], 3)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_row_with_side(self):
        pattern = 'Row 5[WS]: Knit.'
        row = Row([Annotation('Knit.')], 5, 'WS')

        pattern = 'Row 6(RS): Purl.'
        row = Row([Annotation('Purl.')], 6, 'RS')

if __name__ == '__main__':
    unittest.main()