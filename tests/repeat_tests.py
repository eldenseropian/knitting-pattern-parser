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
    #TODO

class TestRowRepeatParsing(unittest.TestCase):

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

        parsed_tree = knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern), pattern_tree)
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

        parsed_tree = knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern), pattern_tree)
        self.assertEqual(tree, parsed_tree)

if __name__ == '__main__':
    unittest.main()