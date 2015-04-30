from pattern import *

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

PATTERN = Pattern('CHAKNA')
sections = [
    [
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
        row16
    ],
    Repeat([Reference(row15), Reference(row16)], 17, 3),
    [
        Reference(row11, 23),
        Reference(row12, 24),
        Reference(row5, 25),
        Reference(row6, 26)
    ],
    Repeat([Reference(row7), Reference(row8)], 27, 4),
    [
        Annotation('From here, rep Rows 11 - 34 for Pat St until piece measures approximately 70" from beg, end on Row 16 of Pat St. Rep Rows 15 and 16 once more.'),
        Reference(row11, 1),
        Reference(row12, 2),
        Annotation('Following Row: With A, knit. Using A, bind off.'),
        Annotation('Finishing'),
        Annotation('Weave in all ends.'),
        Annotation('Side Edgings: With RS facing, using crochet hook and A, work in sc along each side edge of scarf.')
    ]
]

for section in sections:
    PATTERN += section

UNROLLED_PATTERN = Pattern('CHAKNA')
UNROLLED_PATTERN += sections[0]
UNROLLED_PATTERN += [
    Reference(row15, 17),
    Reference(row16, 18),
    Reference(row15, 19),
    Reference(row16, 20),
    Reference(row15, 21),
    Reference(row16, 22)
]
UNROLLED_PATTERN += sections[2]
UNROLLED_PATTERN += [
    Reference(row7, 27),
    Reference(row8, 28),
    Reference(row7, 29),
    Reference(row8, 30),
    Reference(row7, 31),
    Reference(row8, 32),
    Reference(row7, 33),
    Reference(row8, 34)
]
UNROLLED_PATTERN += sections[4]