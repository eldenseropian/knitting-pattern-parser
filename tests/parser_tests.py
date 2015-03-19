"""E2E tests for the parser."""

import os
import sys
import unittest

sys.path.append(os.path.join('..', 'classes'))
from pattern import *

sys.path.append(os.path.join('..', ''))
import knitparser

class TestParser(unittest.TestCase):
    """Test the parser using real patterns."""

    def test_beginner_pattern(self):
        pattern_tree = Pattern('Pattern: Easy-Eyes scarf for carry-around knitting - by Alison Hyde', [
            Annotation('This is the perfect scarf for peaceful knitting. The stitch pattern is so simple, you\'ll likely memorize it even before you start knitting.'),
            Annotation('Cast on an odd number of stitches in a yarn and needle size that you like together. The sample shown here and on my website, spindyeknit.com was made with Soft Baby from Rowan. I cast on 13 stitches using size 11 (6.5 mm) needles. I made a second version in a variegated color of Suri Dream from Knit Picks that shows the versatility of this easy pattern, but unfortunately blogger ate the only photo.'),
            Annotation('Exact gauge is not important, but the fabric should be light and airy, not tight and stiff.'),
            Repeat([Row([Annotation('Purl.')], 1)], 1, 'WS'),
            Row([InRowRepeat([Annotation('K2tog, yo')], 'across'), Annotation('end k1.')], 2),
            Row([Annotation('K1'), InRowRepeat([Annotation('yo, ssk')], 'end of row')], 4),
            Annotation('Bind off loosely and block to open up the lace.'),
            Annotation('(Note: See this month\'s knitting lessons for a stretchy bind off and tips on blocking lace.)'),
            Annotation('Posted by Donna at 7:53 AM'),
            Annotation('Categories: Patterns')
        ])

        pattern = None
        with open('test_files/scarf-beginner.txt') as pattern_file:
            pattern = pattern_file.read()
        parsed_pattern = knitparser.parse(pattern)
 
        self.assertEqual(pattern_tree, parsed_pattern)

    def test_intermediate_pattern(self):
        pass

    def test_advanced_pattern(self):
        pass

if __name__ == '__main__':
    unittest.main()