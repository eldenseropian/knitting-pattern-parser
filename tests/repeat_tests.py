import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):
    pass

class TestRowRepeatParsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_single_repeat(self):
        pattern = 'Rows 9 and 10: Rep Rows 7 and 8 once more.'
        tree = [
            Reference(Row([Annotation('a')], 7)),
            Reference(Row([Annotation('a')], 8)),
        ]
        parsed_tree = knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern), {
            7: Row([Annotation('a')], 7),
            8: Row([Annotation('a')], 8),
            'next_row': 9
        })
        self.assertEqual(tree, parsed_tree)

    def test_multiple_repeat(self):
        pattern = 'Rows 17 - 22: Rep Rows 15 and 16 three times more.'
        tree = Repeat([
            Reference(Row([Annotation('a')], 15)),
            Reference(Row([Annotation('a')], 16)),
        ], 17, 3)
        parsed_tree = knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern), {
            15: Row([Annotation('a')], 15),
            16: Row([Annotation('a')], 16),
            'next_row': 17
        })
        self.assertEqual(tree, parsed_tree)

class TestInRowRepeatParsing(unittest.TestCase):

    def test_repeat(self):
        pattern = 'Row 1: *[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso. Repeat from * to last 4 sts, repeat 4st panel.'
        tree = Row([
            InRowRepeat([Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso')], 'last 4 sts'),
            InRowRepeat([Annotation('4st panel.')])
        ], 1)
        parsed_tree = knitparser.parse_in_row_repeat(pattern, re.match(knitparser.IN_ROW_REPEAT_REGEX, pattern))

        self.assertEqual(tree, parsed_tree)

    def test_rep(self):
        pattern = 'Row 2: *K2tog, yo, rep from * across; end k1.'
        tree = Row([InRowRepeat([Annotation('K2tog, yo')], 'across'), Annotation('end k1')], 2)
        parsed_tree = knitparser.parse_in_row_repeat(pattern, re.match(knitparser.IN_ROW_REPEAT_REGEX, pattern))
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()