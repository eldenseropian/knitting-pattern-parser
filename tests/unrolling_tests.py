import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import unroller

sys.path.append(os.path.join('.', 'test_files'))
import scarf_beginner
import scarf_intermediate
import scarf_advanced

class TestUnrollRepeats(unittest.TestCase):
    """Test unrolling repeats outside the context of a pattern."""

    def test_repeat_first_row(self):
        repeat = Repeat([Row([Annotation('Knit 7.')], 1)], 1, 4)

        expected_unrolled_pattern = [
            Row([Annotation('Knit 7.')], 1),
            Row([Annotation('Knit 7.')], 2),
            Row([Annotation('Knit 7.')], 3),
            Row([Annotation('Knit 7.')], 4)
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_repeat_middle_row(self):
        repeat = Repeat([Row([Annotation('Knit 2, Purl 2.')], 4)], 4, 2)

        expected_unrolled_pattern = [
            Row([Annotation('Knit 2, Purl 2.')], 4),
            Row([Annotation('Knit 2, Purl 2.')], 5)
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_repeat_with_references(self):
        repeat = Repeat([Reference(Row([Annotation('Purl.')], 1), 3)], 3, 2)

        expected_unrolled_pattern = [
            Reference(Row([Annotation('Purl.')], 1), 3),
            Reference(Row([Annotation('Purl.')], 1), 4),
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_repeat_with_unnumbered_references(self):
        repeat = Repeat([
            Reference(Row([Annotation('Knit.')], 1)),
            Reference(Row([Annotation('Purl.')], 2))
        ], 3, 2)

        expected_unrolled_pattern = [
            Reference(Row([Annotation('Knit.')], 1), 3),
            Reference(Row([Annotation('Purl.')], 2), 4),
            Reference(Row([Annotation('Knit.')], 1), 5),
            Reference(Row([Annotation('Purl.')], 2), 6)
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_repeat_multiple_rows(self):
        repeat = Repeat([
            Row([Annotation('K5')], 1, 'WS'),
            Row([Annotation('P5')], 2),
            Row([Annotation('K2, P3')], 3)
        ], 1, 3)

        expected_unrolled_pattern = [
            Row([Annotation('K5')], 1, 'WS'),
            Row([Annotation('P5')], 2, 'RS'),
            Row([Annotation('K2, P3')], 3, 'WS'),
            Row([Annotation('K5')], 4, 'RS'),
            Row([Annotation('P5')], 5, 'WS'),
            Row([Annotation('K2, P3')], 6, 'RS'),
            Row([Annotation('K5')], 7, 'WS'),
            Row([Annotation('P5')], 8, 'RS'),
            Row([Annotation('K2, P3')], 9, 'WS')
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_indefinite_repeat(self):
        # Unrolling an indefinite repeat shouldn't do anything

        repeat = Repeat([
            Row([Annotation('K')], 1),
            Row([Annotation('P')], 2),
        ], 1)
        self.assertEqual([repeat], unroller.unroll_repeat(repeat))

    def test_indefinite_repeat_with_str_times(self):
        repeat = Repeat([
            Row([Annotation('K')], 1),
            Row([Annotation('P')], 2),
        ], 1, 'WS')
        self.assertEqual([repeat], unroller.unroll_repeat(repeat))

class TestUnrollInRowRepeats(unittest.TestCase):
    pass

    #TODO: version 2.0

class TestUnrollPatterns(unittest.TestCase):
    """Test unrolling an entire pattern."""

    def test_unroll_scarf_beginner(self):
        self.assertEqual(
            scarf_beginner.UNROLLED_PATTERN,
            unroller.unroll(scarf_beginner.PATTERN)
        )

    def test_unroll_scarf_intermediate(self):
        self.assertEqual(
            scarf_intermediate.UNROLLED_PATTERN,
            unroller.unroll(scarf_intermediate.PATTERN)
        )

    def test_unroll_scarf_advanced(self):
        self.assertEqual(
            scarf_advanced.UNROLLED_PATTERN,
            unroller.unroll(scarf_advanced.PATTERN)
        )

if __name__ == '__main__':
    unittest.main()