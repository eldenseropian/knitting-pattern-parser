import unittest
import pattern_tree
import parser

class TestIllegalInitialization(unittest.TestCase):

    def test_initialize_empty(self):
        self.assertRaises(TypeError, pattern_tree.PatternTree)

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, pattern_tree.PatternTree, 2)

    def test_initialize_with_list_of_non_rows_or_annotations(self):
        self.assertRaises(Exception, pattern_tree.PatternTree, [1,2,3])

class TestLegalInitialization(unittest.TestCase):

    def test(self):
        self.assertEqual(parser.parse('test'), pattern_tree.PatternTree([pattern_tree.Section([pattern_tree.Annotation('test')])]))

if __name__ == '__main__':
    unittest.main()