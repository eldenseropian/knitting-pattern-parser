import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from annotation import *
from pattern import *
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

    def test(self):
        pattern = 'Rows 9 and 10: Rep Rows 7 and 8 once more.'
        tree = Repeat([
            Row(None, 9, 7),
            Row(None, 10, 8),
        ], 1)
        self.assertEqual(tree, knitparser.parse_repeat(pattern, re.match(knitparser.REPEAT_REGEX, pattern)))

if __name__ == '__main__':
    unittest.main()