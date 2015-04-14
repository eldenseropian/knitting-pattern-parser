import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):
    """Test row constructor constraints."""

    def test_initialize_empty_list(self):
        self.assertRaises(Exception, Row, [], 2)

    def test_initialize_with_non_list(self):
        self.assertRaises(Exception, Row, 'cat', 2)

    def test_initialize_with_non_number(self):
        self.assertRaises(Exception, Row, [Annotation('cat')], 'cat')

    def test_initialize_with_list_of_non_annotations(self):
        self.assertRaises(Exception, Row, ['cat', 'dog'], 2)

class TestUnitRowParsing(unittest.TestCase):
    """Test parsing individual rows outside of the context of a pattern."""

    def test_first_row(self):
        pattern = 'Row 1: Ooh here is a row!'
        row = Row([Annotation('Ooh here is a row!')], 1)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_nth_row(self):
        pattern = 'Row 5: Ooh here is a row!'
        row = Row([Annotation('Ooh here is a row!')], 5)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_first_round(self):
        pattern = 'Round 1: Ooh here is a row!'
        row = Row([Annotation('Ooh here is a row!')], 1)
        self.assertEquals(row, knitparser.parse_row(pattern))

    def test_nth_round(self):
        pattern = 'Round 25: Ooh here is a row!'
        row = Row([Annotation('Ooh here is a row!')], 25)
        self.assertEquals(row, knitparser.parse_row(pattern))

class TestE2ERowParsing(unittest.TestCase):
    """Test parsing rows within the context of a pattern."""

    def setUp(self):
        self.tree = Pattern('Test Pattern')
        self.tree += Annotation('Blah blah this is a pattern.')
        self.tree += Row([Annotation('Ooh here is a row!')], 1)
        self.tree += Row([Annotation('Wow, another one!')], 2)

    def test_no_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\n\nWoo more pattern.'
        
        tree = Pattern('Test Pattern')
        tree += Annotation('Blah blah this is a pattern.')
        tree += Annotation('Woo more pattern.')
        
        self.assertEqual(tree, knitparser.parse(pattern))

    def test_one_row(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRow 1: Ooh here is a row!'
        
        tree = Pattern('Test Pattern')
        tree += Annotation('Blah blah this is a pattern.')
        tree += Row([Annotation('Ooh here is a row!')], 1)

        self.assertEqual(tree, knitparser.parse(pattern))

    def test_multiple_rows(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRow 1: Ooh here is a row!\nRow 2: Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))

    def test_multiple_rounds(self):
        pattern = 'Test Pattern\nBlah blah this is a pattern.\nRound 1: Ooh here is a row!\nRound 2: Wow, another one!'
        self.assertEqual(self.tree, knitparser.parse(pattern))

if __name__ == '__main__':
    unittest.main()