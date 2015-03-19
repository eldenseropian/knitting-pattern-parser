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
        row5 = Row([Annotation('With A'), InRowRepeat([Annotation('k8, yo, sl next st purlwise, k1')], 'twice more'), Annotation('k7')], 5)
        row6 = Row([Annotation('With A, p8'), InRowRepeat([Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once (this adds a new yo on top of previous yo), p9')], 'once more'), Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p8.')], 6)
        row7 = Row([Annotation('With A'), InRowRepeat([Annotation('k8, yo, sl next st and yo\'s purlwise')], 'twice more'), Annotation('k7')], 7)
        row8 = Row([Annotation('With A, p8'), InRowRepeat([Annotation('sl next st and all yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'once more'), Annotation('slip next st and all yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p8.')], 8)
        row11 = Row([Annotation('With B, knit across, knitting all yo\'s together with corresponding slipped sts.')], 11)
        row12 = Row([Annotation('With B, purl.')], 12)
        row15 = Row([
            Annotation('With A, k3'),
            InRowRepeat([Annotation('yo, sl next st and all yo\'s purlwise, k9')], 'twice more'),
            Annotation('yo, sl next st and all yo\'s purlwise, k3.')
        ], 15)
        row16 = Row([
            Annotation('With A, p3'),
            InRowRepeat([Annotation('sl next st and all previous yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'twice more'),
            Annotation('sl next st purlwise, wrap yarn counterclockwise around RH needle once, p3.')
        ], 16)

        pattern_tree = Pattern('CHAKNA', [
            Annotation('Skill Level:'),
            Annotation('Intermediate'),
            Annotation('Project Type:'),
            Annotation('Scarves/Shawls/Cowls'),
            Annotation('Designer:'),
            Annotation('Amanda Keep Williams'),
            Annotation('Chakna'),
            Annotation('A contrast in yarn weights as well as color adds major interest to this fun scarf.'),
            Annotation('Finished Measurements'),
            Annotation('Approximately 8 1/2" wide x 71" long'),
            Annotation('Materials'),
            Annotation('1 Hank Berroco Ultra Alpaca Fine (100 grs), #1207 Salt & Pepper (A)'),
            Annotation('1 Hank Berroco Peruvia (100 grs), #7100 Blanco (B)'),
            Annotation('Straight knitting needles, size 8 (5.00 mm) OR SIZE TO OBTAIN GAUGE'),
            Annotation('Crochet hook, size 3.75 mm (F-5)'),
            Annotation('Gauge'),
            Annotation('18 sts = 4"; 19 rows = 4" in Pat St'),
            Annotation('TO SAVE TIME, TAKE TIME TO CHECK GAUGE'),
            Annotation('Note'),
            Annotation('When B is not in use, carry yarn up side of work. Twist A and B together at beg of every RS row to prevent long loops.'),
            Annotation('Scarf'),
            Annotation('With straight needles, using A, cast on 37 sts.'),
            Row([Annotation('(WS): Knit.')], 1),
            Row([Annotation('Knit. Join B.')], 2),
            Row([Annotation('With B and knit.')], 3),
            Row([Annotation('With B, purl.')], 4),
            row5,
            row6,
            row7,
            row8,
            Reference(row7, 9),
            Reference(row8, 10),
            row11,
            row12,
            Row([Annotation('With A, k3'), InRowRepeat([Annotation('yo, sl next st purlwise, k9')], 'twice more'), Annotation('yo, sl next st purlwise, k3.')], 13),
            Row([Annotation('With A, p3'), InRowRepeat([Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'twice more'), Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p3.')], 14),
            row15,
            row16,
            Repeat([Reference(row15), Reference(row16)], 17, 3),
            Reference(row11, 23),
            Reference(row12, 24),
            Reference(row5, 25),
            Reference(row6, 26),
            Repeat([Reference(row7), Reference(row8)], 27, 4),
            Annotation('From here, rep Rows 11 - 34 for Pat St until piece measures approximately 70" from beg, end on Row 16 of Pat St. Rep Rows 15 and 16 once more.'),
            Reference(row11, 35),
            Reference(row12, 36),
            Row([Annotation('With A, knit. Using A, bind off.')], 37),
            Annotation('Finishing'),
            Annotation('Weave in all ends.'),
            Annotation('Side Edgings: With RS facing, using crochet hook and A, work in sc along each side edge of scarf.')
        ])

        with open('test_files/scarf-intermediate.txt') as pattern_file:
            pattern = pattern_file.read()
        parsed_pattern = knitparser.parse(pattern)
 
        self.assertEqual(pattern_tree, parsed_pattern)

    def test_advanced_pattern(self):
        pass

if __name__ == '__main__':
    unittest.main()