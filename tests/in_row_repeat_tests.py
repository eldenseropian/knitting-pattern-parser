import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestInRowRepeatInitialization(unittest.TestCase):
    """Test in-row repeat constructor constraints."""

    def test_initialize_with_non_annotation(self):
        self.assertRaises(TypeError, InRowRepeat, 'Test Row')

    def test_intialize_with_non_string_until(self):
        self.assertRaises(TypeError, InRowRepeat, Annotation('Test Row'), 5)

class TestInRowRepeatFunctions(unittest.TestCase):
    """Test the functions of the in-row repeat class."""

    def setUp(self):
        self.annotation1 = Annotation('k2, p2')
        self.in_row_repeat_1 = InRowRepeat(self.annotation1)

        self.annotation2 = Annotation('k2, p2, ssk')
        self.in_row_repeat_2 = InRowRepeat(self.annotation2, 'end of row')

    def test_str(self):
        str1 = '<repeat>' + self.annotation1.__str__() + '</repeat>'
        self.assertEquals(str1, self.in_row_repeat_1.__str__())

        str2 = '<repeat until="end of row">' + self.annotation2.__str__() + '</repeat>'
        self.assertEquals(str2, self.in_row_repeat_2.__str__())

    def test_eq(self):
        self.assertTrue(self.in_row_repeat_1 == self.in_row_repeat_1)
        self.assertTrue(self.in_row_repeat_1 == InRowRepeat(Annotation('k2, p2')))
        self.assertTrue(self.in_row_repeat_2 == InRowRepeat(self.annotation2, 'end of row'))

        self.assertFalse(self.in_row_repeat_1 == self.in_row_repeat_2)
        self.assertFalse(self.in_row_repeat_2 == InRowRepeat(self.annotation2))

class TestInRowRepeatParsing(unittest.TestCase):
    """Test parsing in-row repeats outside of the context of a pattern.

    Tests are still run in the context of a row because InRowRepeats cannot
    exist independently of a row and are parsed as such.
    """

    def test_repeat(self):
        # tests repeats with and without untils, with 'to'
        pattern = 'Row 1: *[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso. Repeat from * to last 4 sts, repeat 4st panel.'
        tree = Row([
            InRowRepeat(Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso'), 'last 4 sts'),
            InRowRepeat(Annotation('4st panel'))
        ], 1)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

    def test_rep(self):
        # tests repeats with repeat abbreviated as 'rep', and with 'across'
        pattern = 'Row 2: *K2tog, yo, rep from * across; end k1.'
        tree = Row([InRowRepeat(Annotation('K2tog, yo'), 'across'), Annotation('end k1')], 2)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

    def test_more(self):
        # tests repeats with 'more'
        pattern = 'Row 5: With A, * k8, yo, sl next st purlwise, k1, rep from * twice more, k7.'
        tree = Row([
            Annotation('With A'),
            InRowRepeat(Annotation('k8, yo, sl next st purlwise, k1'), 'twice more'),
            Annotation('k7')
        ], 5)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()