import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *
from section import *
from row import *
from annotation import *

sys.path.append(os.path.join('..', ''))
import knitparser

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

    def setUp(self):
        self.tree = Pattern('Test Pattern', [
            Section([
                Annotation('Blah blah this is a pattern.'),
                Row([Annotation('Ooh here is a row!')], 1),
                Row([Annotation('Wow, another one!')], 2)
            ])
        ])

    def test_no_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n\nWoo more pattern.'
        tree = Pattern('Test Pattern', [
            Section([
                Annotation('Blah blah this is a pattern.'),
                Annotation('Woo more pattern.')
            ])
        ])
        self.assertEqual(tree, knitparser.parse(pattern))

    def test_one_row(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n1. Ooh here is a row!'
        tree = Pattern('Test Pattern', [
            Section([
                Annotation('Blah blah this is a pattern.'),
                Row([Annotation('Ooh here is a row!')], 1),
            ])
        ])
        self.assertEqual(tree, knitparser.parse(pattern))

    def test_multiple_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n1. Ooh here is a row!\n2. Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n1: Ooh here is a row!\n2: Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))

    def test_labelled_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRow 1. Ooh here is a row!\nRow 2. Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRow 1: Ooh here is a row!\nRow 2: Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))

    def test_labelled_rounds(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRound 1. Ooh here is a row!\nRound 2. Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRound 1: Ooh here is a row!\nRound 2: Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))

if __name__ == '__main__':
    unittest.main()