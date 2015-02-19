import unittest
import parser
from pattern_tree import *
from section import *
from row import *
from annotation import *

class TestIllegalInitialization(unittest.TestCase):
    def test_initialize_empty_list(self):
        self.assertRaises(Exception, Row, [], 2)

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, Row, 'cat', 2)

    def test_initialize_with_non_number(self):
        self.assertRaises(Exception, Row, [Annotation('cat')], 'cat')

    def test_initialize_with_list_of_non_annotations(self):
        self.assertRaises(Exception, Row, ['cat', 'dog'], 2)

class TestRowParsing(unittest.TestCase):

    def test_no_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n\nWoo more pattern.'
        tree = PatternTree([
            Section([
                Annotation('Test Pattern'),
                Annotation('Blah blah this is a pattern.'),
                Annotation('Woo more pattern.')
            ])
        ])
        self.assertEqual(tree, parser.parse(pattern))

    def test_one_row(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n1. Ooh here is a row!'
        tree = PatternTree([
            Section([
                Annotation('Test Pattern'),
                Annotation('Blah blah this is a pattern.'),
                Row([Annotation('Ooh here is a row!')], 1),
            ])
        ])
        self.assertEqual(tree, parser.parse(pattern))

    def test_multiple_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n1. Ooh here is a row!\n2. Wow, another one!'
        tree = PatternTree([
            Section([
                Annotation('Test Pattern'),
                Annotation('Blah blah this is a pattern.'),
                Row([Annotation('Ooh here is a row!')], 1),
                Row([Annotation('Wow, another one!')], 2)
            ])
        ])
        self.assertEqual(tree, parser.parse(pattern))

if __name__ == '__main__':
    unittest.main()