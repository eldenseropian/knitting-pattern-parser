import os
import re
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import unroller

class TestUnrollRepeats(unittest.TestCase):

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
        repeat = Repeat([Reference(Row([Annotation('Purl.')], 1), 2)], 3, 2)

        expected_unrolled_pattern = [
            Row([Annotation('Purl.')], 3),
            Row([Annotation('Purl.')], 4)
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

    def test_repeat_multiple_rows(self):
        repeat = Repeat([
            Row([Annotation('K5')], 1, 'WS'),
            Row([Annotation('P5')], 2),
            Row([Annotation('K2, P3')], 3)
        ], 1, 3)

        # TODO: calculate side for all rows
        # for now, don't use side unless explicitly stated

        expected_unrolled_pattern = [
            Row([Annotation('K5')], 1, 'WS'),
            Row([Annotation('P5')], 2),
            Row([Annotation('K2, P3')], 3),
            Row([Annotation('K5')], 4),
            Row([Annotation('P5')], 5),
            Row([Annotation('K2, P3')], 6),
            Row([Annotation('K5')], 7),
            Row([Annotation('P5')], 8),
            Row([Annotation('K2, P3')], 9)
        ]

        actual_unrolled_pattern = unroller.unroll_repeat(repeat)
        self.assertEqual(expected_unrolled_pattern, actual_unrolled_pattern)

class TestUnrollInRowRepeats(unittest.TestCase):
    pass

    #TODO: version 2.0


#TODO: unroll parsed patterns

if __name__ == '__main__':
    unittest.main()