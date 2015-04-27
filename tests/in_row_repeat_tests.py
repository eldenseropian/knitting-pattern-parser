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

    def test_initialize_with_non_list(self):
        self.assertRaises(TypeError, InRowRepeat, 'Test Row')

    def test_intialize_with_non_string_until(self):
        self.assertRaises(TypeError, InRowRepeat, [Annotation('Test Row')], 5)

class TestInRowRepeatFunctions(unittest.TestCase):
    """Test the functions of the in-row repeat class."""

    def setUp(self):
        self.annotation1 = Annotation('k2, p2')
        self.in_row_repeat_1 = InRowRepeat([self.annotation1])

        self.annotation2 = Annotation('k2, p2, ssk')
        self.in_row_repeat_2 = InRowRepeat([self.annotation2], 'end of row')

    def test_str(self):
        str1 = '<repeat>' + self.annotation1.__str__() + '</repeat>'
        self.assertEquals(str1, self.in_row_repeat_1.__str__())

        str2 = '<repeat until="end of row">' + self.annotation2.__str__() + '</repeat>'
        self.assertEquals(str2, self.in_row_repeat_2.__str__())

    def test_eq(self):
        self.assertTrue(self.in_row_repeat_1 == self.in_row_repeat_1)
        self.assertTrue(self.in_row_repeat_1 == InRowRepeat([Annotation('k2, p2')]))
        self.assertTrue(self.in_row_repeat_2 == InRowRepeat([self.annotation2], 'end of row'))

        self.assertFalse(self.in_row_repeat_1 == self.in_row_repeat_2)
        self.assertFalse(self.in_row_repeat_2 == InRowRepeat([self.annotation2]))

class TestInRowRepeatParsing(unittest.TestCase):
    """Test parsing in-row repeats outside of the context of a pattern.

    Tests are still run in the context of a row because InRowRepeats cannot
    exist independently of a row and are parsed as such.
    """

    def test_repeat(self):
        # tests repeats with and without untils, with 'to'
        pattern = 'Row 1: *[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso. Repeat from * to last 4 sts, repeat 4st panel.'
        tree = Row([
            InRowRepeat([Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso')], 'last 4 sts'),
            Annotation('repeat 4st panel')
        ], 1)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

    def test_rep(self):
        # tests repeats with repeat abbreviated as 'rep', and with 'across'
        pattern = 'Row 2: *K2tog, yo, rep from * across; end k1.'
        tree = Row([InRowRepeat([Annotation('K2tog, yo')], 'across'), Annotation('end k1')], 2)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

    def test_more(self):
        # tests repeats with 'more', and with annotation before the repeat
        pattern = 'Row 5: With A, * k8, yo, sl next st purlwise, k1, rep from * twice more, k7.'
        tree = Row([
            Annotation('With A'),
            InRowRepeat([Annotation('k8, yo, sl next st purlwise, k1')], 'twice more'),
            Annotation('k7')
        ], 5)
        parsed_tree = knitparser.parse_row(pattern)

        self.assertEquals(tree, parsed_tree)

    def test_bracket_repeat(self):
        pattern = 'Round 1: [k2tog, sl 1, yo] repeat 4 times'
        tree = Row([
            InRowRepeat([Annotation('k2tog, sl 1, yo')], '4 times')
        ], 1)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEquals(tree, parsed_tree)

        pattern = 'Round 2: [k2tog, sl 1, yo] repeat once, k2tog, k3tog'
        tree = Row([
            InRowRepeat([Annotation('k2tog, sl 1, yo')], 'once'),
            Annotation('k2tog, k3tog')
        ], 2)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEquals(tree, parsed_tree)

    def test_no_further_instructions(self):
        pattern = 'Row 3: *K1, P1*, rep between * to end.'
        tree = Row([
            InRowRepeat([Annotation('K1, P1')], 'end')
        ], 3)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEquals(tree, parsed_tree)

    def test_multiple_in_row(self):
        pass
    # def test_nested(self):
    #     pattern = 'Crown round 1 (dark yarn): *[k2tog, sl 1, yo] repeat 4 times, k2tog, k3tog (the next sl stitch, yo, and the following stitch - knit all 3 stitches through the front of their loops, starting with the 3rd one), sl 1, yo, k3tog (slide the next sl stitch and its yo and return them on the left needle turning them around, knit 3 stitches through the back of their loops starting with the 1st one), [k2tog, sl 1, yo] repeat 4 times*; repeat from * to * on the next 3 needles.'
    #     tree = Row([
    #         InRowRepeat([
    #             InRowRepeat([Annotation('k2tog, sl 1, yo')], '4 times'),
    #             Annotation('k2tog, k3tog (the next sl stitch, yo, and the following stitch - knit all 3 stitches through the front of their loops, starting with the 3rd one), sl 1, yo, k3tog (slide the next sl stitch and its yo and return them on the left needle turning them around, knit 3 stitches through the back of their loops, starting with the 1st one)'),
    #             InRowRepeat([Annotation('k2tog, sl 1, yo')], '4 times')
    #         ], 'on the next 3 needles.')
    #     ], 1)
    #     parsed_tree = knitparser.parse_row(pattern)
    #     self.assertEquals(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()