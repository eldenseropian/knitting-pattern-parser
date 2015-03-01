import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
import annotation
import pattern
import section

sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, pattern.Pattern, 'title', 2)

    def test_initialize_with_list_of_non_rows_or_annotations(self):
        self.assertRaises(Exception, pattern.Pattern, 'title', [1,2,3])

    def test_initialize_with_empty_list(self):
        self.assertRaises(Exception, pattern.Pattern, 'title', [])

    def test_initialize_with_non_string_title(self):
        self.assertRaises(Exception, pattern.Pattern, 2, [section.Section([annotation.Annotation('test')])])

class TestLegalInitialization(unittest.TestCase):

    def test(self):
        self.assertEqual(knitparser.parse('Test Pattern\ntest'),
            pattern.Pattern('Test Pattern', [section.Section([annotation.Annotation('test')])]))

if __name__ == '__main__':
    unittest.main()