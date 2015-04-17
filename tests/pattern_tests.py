"""Unit tests for the pattern class"""

import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestIllegalInitialization(unittest.TestCase):
    """Test pattern constructor constraints."""

    def test_initialize_with_non_string_title(self):
        self.assertRaises(TypeError, Pattern, 2)

    def test_initialize_with_empty_title(self):
        self.assertRaises(ValueError, Pattern, '')

    def test_initialize_with_whitespace_title(self):
        self.assertRaises(ValueError, Pattern, '  ')

class TestLegalInitialization(unittest.TestCase):
    """Test that a basic pattern can be constructed."""

    def test(self):
        pattern = Pattern('Test Pattern')
        pattern += Annotation('test')
        self.assertEqual(knitparser.parse('Test Pattern\ntest'), pattern)

if __name__ == '__main__':
    unittest.main()