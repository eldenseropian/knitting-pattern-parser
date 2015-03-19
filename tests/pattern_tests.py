import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, Pattern, 'title', 2)

    def test_initialize_with_list_of_non_rows_or_annotations(self):
        self.assertRaises(Exception, Pattern, 'title', [1,2,3])

    def test_initialize_with_empty_list(self):
        self.assertRaises(Exception, Pattern, 'title', [])

    def test_initialize_with_non_string_title(self):
        self.assertRaises(Exception, Pattern, 2, [Annotation('test')])

class TestLegalInitialization(unittest.TestCase):

    def test(self):
        self.assertEqual(knitparser.parse('Test Pattern\ntest'),
            Pattern('Test Pattern', [Annotation('test')]))

if __name__ == '__main__':
    unittest.main()