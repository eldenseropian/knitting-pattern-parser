import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import reference_expander

sys.path.append(os.path.join('.', 'test_files'))
import scarf_beginner
import scarf_intermediate
import scarf_advanced

class TestExpandReferences(unittest.TestCase):
    """Test expanding references outside the context of a pattern."""

    def test_reference_with_row_number(self):
        reference = Reference(Row([Annotation('Knit')], 1), 4)
        expanded = Row([Annotation('Knit')], 4)
        self.assertEqual(expanded, reference_expander.expand_reference(reference))

    def test_reference_without_row_number(self):
        # references inside repeats may not have row numbers - should not be dereferenced
        reference = Reference(Row([Annotation('Purl')], 1))
        self.assertEqual(reference, reference_expander.expand_reference(reference))

class TestExpandPatterns(unittest.TestCase):
    """Test expanding references in an entire pattern."""

    def test_expand_scarf_beginner(self):
        self.assertEqual(
            scarf_beginner.EXPANDED_PATTERN,
            reference_expander.expand(scarf_beginner.PATTERN)
        )

    def test_expand_scarf_intermediate(self):
        self.assertEqual(
            scarf_intermediate.EXPANDED_PATTERN,
            reference_expander.expand(scarf_intermediate.PATTERN)
        )

    def test_expand_scarf_advanced(self):
        self.assertEqual(
            scarf_advanced.EXPANDED_PATTERN,
            reference_expander.expand(scarf_advanced.PATTERN)
        )

if __name__ == '__main__':
    unittest.main()