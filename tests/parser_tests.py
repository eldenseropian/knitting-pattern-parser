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
            Row([InRowRepeat([Annotation('K2tog, yo')], 'across'), Annotation('end k1')], 2),
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
 
        with open('tempOff', 'w') as off:
            off.write(pattern_tree.__str__())
        with open('tempParsed', 'w') as parsed:
            parsed.write(parsed_pattern.__str__())

        self.assertEqual(pattern_tree, parsed_pattern)

    def test_intermediate_pattern(self):
        row5 = Row([Annotation('With A'), InRowRepeat([Annotation('k8, yo, sl next st purlwise, k1')], 'twice more'), Annotation('k7')], 5)
        row6 = Row([Annotation('With A, p8'), InRowRepeat([Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once (this adds a new yo on top of previous yo), p9')], 'once more'), Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p8')], 6)
        row7 = Row([Annotation('With A'), InRowRepeat([Annotation('k8, yo, sl next st and yo\'s purlwise, k1')], 'twice more'), Annotation('k7')], 7)
        row8 = Row([Annotation('With A, p8'), InRowRepeat([Annotation('sl next st and all yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'once more'), Annotation('slip next st and all yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p8')], 8)
        row11 = Row([Annotation('With B, knit across, knitting all yo\'s together with corresponding slipped sts.')], 11)
        row12 = Row([Annotation('With B, purl.')], 12)
        row15 = Row([
            Annotation('With A, k3'),
            InRowRepeat([Annotation('yo, sl next st and all yo\'s purlwise, k9')], 'twice more'),
            Annotation('yo, sl next st and all yo\'s purlwise, k3')
        ], 15)
        row16 = Row([
            Annotation('With A, p3'),
            InRowRepeat([Annotation('sl next st and all previous yo\'s purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'twice more'),
            Annotation('sl next st purlwise, wrap yarn counterclockwise around RH needle once, p3')
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
            Row([Annotation('Knit.')], 1, 'WS'),
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
            Row([Annotation('With A, k3'), InRowRepeat([Annotation('yo, sl next st purlwise, k9')], 'twice more'), Annotation('yo, sl next st purlwise, k3')], 13),
            Row([Annotation('With A, p3'), InRowRepeat([Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p9')], 'twice more'), Annotation('sl next st and yo from previous row purlwise, wrap yarn counterclockwise around RH needle once, p3')], 14),
            row15,
            row16,
            Repeat([Reference(row15), Reference(row16)], 17, 3),
            Reference(row11, 23),
            Reference(row12, 24),
            Reference(row5, 25),
            Reference(row6, 26),
            Repeat([Reference(row7), Reference(row8)], 27, 4),
            Repeat([Annotation('From here, rep Rows 11 - 34 for Pat St until piece measures approximately 70" from beg, end on Row 16 of Pat St. Rep Rows 15 and 16 once more.')], 35),
            Reference(row11, 36),
            Reference(row12, 37),
            Row([Annotation('With A, knit. Using A, bind off.')], 38),
            Annotation('Finishing'),
            Annotation('Weave in all ends.'),
            Annotation('Side Edgings: With RS facing, using crochet hook and A, work in sc along each side edge of scarf.')
        ])

        with open('test_files/scarf-intermediate.txt') as pattern_file:
            pattern = pattern_file.read()
        parsed_pattern = knitparser.parse(pattern)

        self.assertEqual(pattern_tree, parsed_pattern)

    def test_advanced_pattern(self):
        leavesRow1 = Row([
            InRowRepeat([
                Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('repeat 4st panel')
            ])
        ], 1)
        
        leavesRow2 = Row([
            Annotation('Purl all sts EXCEPT: knit all sts that were purled the previous row')
        ], 2)
        
        leavesRow3 = Row([
            InRowRepeat([
                Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, k4, yo, k1, yo, k5, [yo, k1] twice, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('4st panel')
            ])
        ], 3)

        leavesRow5 = Row([
            InRowRepeat([
                Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k3, yo, k1, yo, k7, yo, k1, yo, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('4st panel')
            ])
        ], 5)

        leavesRow7 = Row([
            InRowRepeat([
                Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, k2, yo, k1, yo, k3, yo, k1, yo, k5, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('4st panel')
            ])
        ], 7)

        leavesRow9 = Row([
            InRowRepeat([
                Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, [k1, yo] twice, k5, yo, k1, yo, k4, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('4st panel')
            ])
        ], 9)

        leavesRow11 = Row([
            InRowRepeat([
                Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, yo, k1, yo, k7, yo, k1, yo, k3, sl 1-k2tog-psso')
            ], 'last 4 sts'),
            InRowRepeat([
                Annotation('4st panel')
            ])
        ], 11)

        wavesRow1 = Row([
            Annotation('K2, purl to last two sts, k2')
        ], 1)
        
        wavesRow2 = Row([
            Annotation('Sl1, k3, yo, k5, yo, k2tog, yo, k2.')
        ], 2)
        
        wavesRow4 = Row([
            Annotation('Sl1, k4, sl1-k2tog-psso, k2, [yo, k2tog] twice, k1.')
        ], 4)
        
        wavesRow6 = Row([
            Annotation('Sl1, k3, ssk, k2, [yo, k2tog] twice, k1.')
        ], 6)
        
        wavesRow8 = Row([
            Annotation('Sl1, k2, ssk, k2, [yo, k2tog] twice, k1. ')
        ], 8)
        
        wavesRow10 = Row([
            Annotation('Sl1, k1, ssk, k2, [yo, k2tog] twice, k1. ')
        ], 10)
        
        wavesRow12 = Row([
            Annotation('Sl1, ssk, k2, yo, k1, yo, k2tog, yo, k2.')
        ], 12)
        
        wavesRow14 = Row([
            Annotation('Sl1, [k3, yo] twice, k2tog, yo, k2.')
        ], 14)

        pattern_tree = Pattern('Leaves and waves', [
            Annotation('I was thinking of fall and how we all like to return to dark colors after the brightness of summer and I wanted the shawl to be large but not heavy.'),
            Annotation('Lace-weight mohair is so light and airy; the shawl can easily be worn as a long scarf, or even a sarong.'),
            Annotation('I like the surprising asymmetry of the colors and shapes of this shawl, as it often looks different than expected. The construction is fairly simple but previous lace knitting is recommended'),
            Annotation('The edging pattern is from Barbara Walker\'s Second Treasury of Knitting Patterns. The leaf pattern is from Susanna Lewis\'s Knitting Lace.'),
            Annotation('model: Ann Marie Boyle  photos: Kat Coyle'),
            Annotation('SIZE'),
            Annotation('One'),
            Annotation('FINISHED MEASUREMENTS'),
            Annotation('Height: 34 inches approx'),
            Annotation('Width: 77 inches approx'),
            Annotation('MATERIALS'),
            Annotation('[MC] Mondial Prestigio [80% Super Kid Mohair, 20% Nylon; 272yd/245m per 25g skein]; color: #12; 4 skeins'),
            Annotation('[CC] Mondial Prestigio [80% Super Kid Mohair, 20% Nylon; 272yd/245m per 25g skein]; color: #815; 2 skeins'),
            Annotation('1 set US #10/6mm straight needles '),
            Annotation('1 29 inch US #10/6mm circular needle'),
            Annotation('tapestry needle'),
            Annotation('waste yarn - use a smooth, mercerized cotton yarn'),
            Annotation('GAUGE'),
            Annotation('12 sts/23 rows = 4" in stockinette stitch'),
            Annotation('STITCH PATTERNS'),
            Annotation('[Knitty\'s list of standard abbreviations can be found here]'),
            Annotation('Leaves (Multiple of 22 sts)'),
            Annotation('The first 4 sts of each pattern repeat, in braces, form the undulating columns of yarnovers which divide each leaf panel. This will be referred to as the 4st panel.'),
            Annotation('The right leaning double decrease which starts each leaf panel is worked as follows: ssk, return st just worked to L needle, pass next st over, return st to R needle. (ssk-L-pnso-R).'),
            leavesRow1,
            Repeat([
                leavesRow2
            ], 2, 'even'),
            leavesRow3,
            leavesRow5,
            leavesRow7,
            leavesRow9,
            leavesRow11,
            Repeat([
                Reference(leavesRow1),
                Reference(leavesRow2),
                Reference(leavesRow3),
                Reference(leavesRow2),
                Reference(leavesRow5),
                Reference(leavesRow2),
                Reference(leavesRow7),
                Reference(leavesRow2),
                Reference(leavesRow9),
                Reference(leavesRow2),
                Reference(leavesRow11),
                Reference(leavesRow2)
            ], 1),
            Annotation('for Leaves pattern'),
            Annotation('Wave Edging'),
            Annotation('NOTE: Number of sts will vary between 10 and 15 sts.'),
            Annotation('CO 13 sts.'),
            Repeat([
                wavesRow1
            ], 1, 'odd'),
            wavesRow2,
            wavesRow4,
            wavesRow6,
            wavesRow8,
            wavesRow10,
            wavesRow12,
            wavesRow14,
            Repeat([
                Reference(wavesRow1),
                Reference(wavesRow2),
                Reference(wavesRow1),
                Reference(wavesRow4),
                Reference(wavesRow1),
                Reference(wavesRow6),
                Reference(wavesRow1),
                Reference(wavesRow8),
                Reference(wavesRow1),
                Reference(wavesRow10),
                Reference(wavesRow1),
                Reference(wavesRow12),
                Reference(wavesRow1),
                Reference(wavesRow14)
            ], 1),
            Annotation('for Wave Edging'),
            Annotation('Notes on casting on '),
            Annotation('This pattern is written using a provisional cast on for the main panels, such as an invisible cast on, or a crochet chain cast on. If you are unfamiliar or uncomfortable with these techniques, try casting on and working a few rows with waste yarn, then switching to the main yarn and starting the pattern. The waste yarn rows can be removed later in the same way as other provisional cast ons.'),
            Annotation('DIRECTIONS'),
            Annotation('Color Panel'),
            Annotation('Using straight needle, CC, waste yarn, and a provisional cast on, CO 92 sts.'),
            Annotation('Work 12 rows of Leaves patt 11 times -- 132 rows in total.'),
            Annotation('Put all sts on hold on waste yarn. Set aside.'),
            Annotation('Black Panel'),
            Annotation('Using straight needle, CC, waste yarn, and a provisional cast on, CO 133 sts.'),
            Row([
                Annotation('K1, OMITTING FIRST INSTANCE OF 4ST PANEL work 6 repeats of Leaves patt.')
            ], 1, 'RS'),
            Repeat([
                Annotation('Cont in patt as set until the 12 rows of Leaves patt have been worked twice')
            ], 2, 24),
            Repeat([
                Annotation('Cont in stockinette st until panel measures same as color panel.')
            ], 25),
            Annotation('156 rows worked in total.'),
            Annotation('Top Edge'),
            Annotation('Beg with k2, work across all sts of black panel in 2x2 rib, sl held sts of color panel onto working needle with black panel (so both WS are facing), work across sts of color panel in 2x2 rib to last 2 sts, p2tog. 224 sts'),
            Repeat([
                Annotation('Cont in rib')
            ], 26, 3),
            Annotation('Loosely BO all sts in patt.'),
            Annotation('Bottom Edge'),
            Annotation('Carefully remove waste yarn from CO edges of both panels, and place all resulting live sts onto circular needle. '),
            Annotation('With RS facing and CC, cast 13 sts onto needle at end of black panel.'),
            Annotation('K 1 row -- new sts are now on end of needle next to color panel. Turn work.'),
            Annotation('Beg with Row 1, work Wave edging.'),
            Annotation('At the end of each WS row, k the last st tog with 1 st from shawl.'),
            Annotation('Cont in this way until all sts from both panels have been worked tog with edging -- 32 repeats of Wave Edging have been worked.'),
            Annotation('BO after row 14 of final repeat.'),
            Annotation('FINISHING'),
            Annotation('Join Panels'),
            Annotation('With Tapestry needle and MC, join black panel to color panel using mattress st.'),
            Annotation('Side Edging'),
            Annotation('With MC, CO 13 sts. Work Wave Edging for 14 repeats. BO all sts.'),
            Annotation('With CC, pick up 20 sts from cast on edge of this piece, and work in 2x2 rib for 3 rows. BO all sts.'),
            Annotation('Sew side edging to shawl along side of color panel, placing ribbed sections next to each other.'),
            Annotation('Weave in all ends. Because of the sheer nature of the fabric, weave ends along seams wherever possible.'),
            Annotation('Wash in cool water and block lightly.'),
            Annotation('Wear with flair!'),
            Annotation('ABOUT THE DESIGNER'),
            Annotation('Kat\'s latest knitting project is her son Felix. Felix loves to pull on the shawls as Kat knits them. Someday, she thinks he may be a knitter too.'),
            Annotation('Pattern & images c 2004 Kat Coyle. Contact Kat.')
        ])

if __name__ == '__main__':
    unittest.main()