from pattern import *

leavesRow1 = Row([
    InRowRepeat([
        Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k5, yo, k1, yo, k3, yo, k1, yo, k2, sl 1-k2tog-psso')
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
], 1)

leavesRow2 = Row([
    Annotation('Purl all sts EXCEPT: knit all sts that were purled the previous row')
], 2)

leavesRow3 = Row([
    InRowRepeat([
        Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, k4, yo, k1, yo, k5, [yo, k1] twice, sl 1-k2tog-psso'),
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
], 3)

leavesRow5 = Row([
    InRowRepeat([
        Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, k3, yo, k1, yo, k7, yo, k1, yo, sl 1-k2tog-psso'),
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
], 5)

leavesRow7 = Row([
    InRowRepeat([
        Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, k2, yo, k1, yo, k3, yo, k1, yo, k5, sl 1-k2tog-psso'),
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
], 7)

leavesRow9 = Row([
    InRowRepeat([
        Annotation('[p1, k2tog, yo, p1], ssk-L-pnso-R, [k1, yo] twice, k5, yo, k1, yo, k4, sl 1-k2tog-psso'),
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
], 9)

leavesRow11 = Row([
    InRowRepeat([
        Annotation('[p1, yo, ssk, p1], ssk-L-pnso-R, yo, k1, yo, k7, yo, k1, yo, k3, sl 1-k2tog-psso'),
    ], 'last 4 sts'),
    Annotation('repeat 4st panel')
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

PATTERN = Pattern('Leaves and waves')
PATTERN += [
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
    Annotation('Repeat rows 1-12 for Leaves pattern.'),
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
    Annotation('Repeat rows 1-14 for Wave Edging.'),
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
    Annotation('Cont in patt as set until the 12 rows of Leaves patt have been worked twice -- 24 rows in total.'),
    Annotation('Cont in stockinette st until panel measures same as color panel.'),
    Annotation('156 rows worked in total.'),
    Annotation('Top Edge'),
    Annotation('Beg with k2, work across all sts of black panel in 2x2 rib, sl held sts of color panel onto working needle with black panel (so both WS are facing), work across sts of color panel in 2x2 rib to last 2 sts, p2tog. 224 sts'),
    Annotation('Cont in rib for 3 rows more.'),
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
    Annotation('Pattern & images (c) 2004 Kat Coyle. Contact Kat.')
]