import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from annotation import *
from pattern import *
from reference import *
from repeat import *
from row import *
from section import *


sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):
    pass

class TestRowParsing(unittest.TestCase):

    def setUp(self):
        pass

    def test_single_repeat(self):
        pattern = 'Rows 9 and 10: Rep Rows 7 and 8 once more.'
        tree = Repeat([
            Reference(Row([Annotation('a')], 7)),
            Reference(Row([Annotation('a')], 8)),
        ], 9, 1)
        parsed_tree = knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern), {
            7: Row([Annotation('a')], 7),
            8: Row([Annotation('a')], 8)
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
            16: Row([Annotation('a')], 16)
        })
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()