import unittest
import pattern_tree
import parser
import annotation

class TestIllegalInitialization(unittest.TestCase):

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, pattern_tree.Section, 2)

    def test_initialize_with_list_of_non_rows_or_annotations(self):
        self.assertRaises(Exception, pattern_tree.Section, [1,2,3])

    def test_initialize_with_empty_list(self):
        self.assertRaises(Exception, pattern_tree.Section, [])

class TestLegalInitialization(unittest.TestCase):

    def test(self):
        self.assertEqual(parser.parse('test'), pattern_tree.PatternTree([pattern_tree.Section([annotation.Annotation('test')])]))

if __name__ == '__main__':
    unittest.main()