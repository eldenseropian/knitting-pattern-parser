from pattern import *

PATTERN = Pattern('Pattern: Easy-Eyes scarf for carry-around knitting - by Alison Hyde')
PATTERN += [
    Annotation('This is the perfect scarf for peaceful knitting. The stitch pattern is so simple, you\'ll likely memorize it even before you start knitting.'),
    Annotation('Cast on an odd number of stitches in a yarn and needle size that you like together. The sample shown here and on my website, spindyeknit.com was made with Soft Baby from Rowan. I cast on 13 stitches using size 11 (6.5 mm) needles. I made a second version in a variegated color of Suri Dream from Knit Picks that shows the versatility of this easy pattern, but unfortunately blogger ate the only photo.'),
    Annotation('Exact gauge is not important, but the fabric should be light and airy, not tight and stiff.'),
    Repeat([Row([Annotation('Purl')], 1)], 1, 'WS'),
    Row([InRowRepeat([Annotation('K2tog, yo')], 'across'), Annotation('end k1')], 2),
    Row([Annotation('K1'), InRowRepeat([Annotation('yo, ssk')], 'end of row')], 4),
    Annotation('Bind off loosely and block to open up the lace.'),
    Annotation('(Note: See this month\'s knitting lessons for a stretchy bind off and tips on blocking lace.)'),
    Annotation('Posted by Donna at 7:53 AM'),
    Annotation('Categories: Patterns')
]

UNROLLED_PATTERN = PATTERN
EXPANDED_PATTERN = PATTERN
EXPANDED_AND_UNROLLED_PATTERN = PATTERN