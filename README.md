usage:  ./list.sh filename or dirname [column_num] ['keyword or regexp'] [isAlignCourseName]

filename or dirname: the course file or dir

column_num: from 1 to 3

keyword or regexp: the keyword for filter course

keyword suggest(to list keyword, please run ./list.sh help filename):

     1	 106 university
     2	  78 of
     3	  30 and
     4	  20 stanford
     5	  19 the
     6	  18 to
     7	  14 programming
     8	  14 at
     9	  13 introduction
    10	  12 urbana
    11	  12 illinois
    12	  12 champaign
    13	   9 washington
    14	   9 part
    15	   9 for
    16	   9 computer
    17	   9 cole
    18	   9 algorithms
    19	   8 princeton
    20	   8 in
    21	   7 security
    22	   7 rale
    23	   7 polytechnique
    24	   7 lausanne
    25	   7 f
    26	   7 de
    27	   7 data
    28	   7 d
    29	   7 california
    30	   7 analysis
    31	   6 technology
    32	   6 processing
    33	   6 park
    34	   6 networks
    35	   6 maryland
    36	   6 computing
    37	   6 college
    38	   5 systems
    39	   5 software
    40	   5 science
    41	   5 san
    42	   5 mining
    43	   5 institute
    44	   5 information
    45	   5 game
    46	   5 digital
    47	   5 diego
    48	   5 computational
    49	   5 cloud
    50	   5 c
    51	   4 rice
    52	   4 principles
    53	   4 new
    54	   4 mobile
    55	   4 michigan
    56	   4 logic
    57	   4 learning
    58	   4 language
    59	   4 georgia
    60	   4 design
    61	   4 columbia
    62	   4 applications
    63	   4 android
    64	   4 an
    65	   3 with
    66	   3 toronto
    67	   3 theory
    68	   3 state
    69	   3 programmation
    70	   3 program
    71	   3 melbourne
    72	   3 machine
    73	   3 london
    74	   3 la
    75	   3 interactive
    76	   3 ii
    77	   3 i
    78	   3 handheld
    79	   3 fundamentals
    80	   3 en
    81	   3 edinburgh
    82	   3 discrete
    83	   3 cryptography
    84	   3 british
    85	   3 bioinformatics
    86	   3 arts
    87	   2 york
    88	   2 web
    89	   2 video
    90	   2 vanderbilt
    91	   2 tokyo
    92	   2 text
    93	   2 social
    94	   2 services
    95	   2 school
    96	   2 risk
    97	   2 python
    98	   2 pennsylvania
    99	   2 pattern

eg: ./list.sh db/eecs-course-all2014 2 'Machine learning'

    ./list.sh db/eecs-course-all2014 1 '^cs.*Cryptography'

    ./list.sh db/eecs/eecs-course-edx2014 2 '' no | sort  -k1 -n -r
===========
