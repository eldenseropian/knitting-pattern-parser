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

class TestInRowRepeatParsing(unittest.TestCase):

    def test_repeat(self):
        pattern = 'Row 1: *[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso. Repeat from * to last 4 sts, repeat 4st panel.'
        tree = Row([
            InRowRepeat(Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso'), 'last 4 sts'),
            InRowRepeat(Annotation('4st panel'))
        ], 1)
        parsed_tree = knitparser.parse_row(pattern)

        self.assertEqual(tree, parsed_tree)

    def test_rep(self):
        pattern = 'Row 2: *K2tog, yo, rep from * across; end k1.'
        tree = Row([InRowRepeat(Annotation('K2tog, yo'), 'across'), Annotation('end k1')], 2)
        parsed_tree = knitparser.parse_row(pattern)
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()