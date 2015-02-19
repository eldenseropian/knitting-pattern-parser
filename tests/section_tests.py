import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
import annotation
import pattern

sys.path.append(os.path.join('..', ''))
import knitparser


class TestIllegalInitialization(unittest.TestCase):

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, pattern.Section, 2)

    def test_initialize_with_list_of_non_rows_or_annotations(self):
        self.assertRaises(Exception, pattern.Section, [1,2,3])

    def test_initialize_with_empty_list(self):
        self.assertRaises(Exception, pattern.Section, [])

class TestLegalInitialization(unittest.TestCase):

    def test(self):
        self.assertEqual(knitparser.parse('test'), pattern.Pattern([pattern.Section([annotation.Annotation('test')])]))

if __name__ == '__main__':
    unittest.main()