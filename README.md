usage:  ./list.sh filename or dirname [column_num] ['keyword or regexp'] [is_online_course] [is_align_course_name]

filename or dirname: the course file or dir

column_num: from 1 to 3

keyword or regexp: the keyword for filter course

keyword suggest(to list keyword, please run ./list.sh help filename):

     1	 205 cs
     2	  54 and
     3	  38 computer
     4	  35 in
     5	  31 a
     6	  21 systems
     7	  20 b
     8	  18 topics
     9	  17 to
    10	  17 project
    11	  15 programming
    12	  13 for
    13	  13 algorithms
    14	  12 of
    15	  12 introduction
    16	  11 advanced
    17	  10 software
    18	  10 music
    19	  10 computing
    20	   9 the
    21	   9 science
    22	   9 n
    23	   9 human
    24	   9 design
    25	   9 computational
    26	   8 vision
    27	   8 research
    28	   8 interaction
    29	   8 data
    30	   7 c
    31	   7 biomedin
    32	   7 analysis
    33	   6 x
    34	   6 w
    35	   6 theory
    36	   6 seminar
    37	   6 linguist
    38	   6 information
    39	   6 e
    40	   6 d
    41	   5 with
    42	   5 robotics
    43	   5 principles
    44	   5 practical
    45	   5 p
    46	   5 learning
    47	   5 laboratory
    48	   5 l
    49	   5 independent
    50	   5 graphics
    51	   5 from
    52	   5 educ
    53	   5 distributed
    54	   5 digital
    55	   4 web
    56	   4 training
    57	   4 technology
    58	   4 techniques
    59	   4 security
    60	   4 s
    61	   4 networks
    62	   4 mining
    63	   4 me
    64	   4 language
    65	   4 intelligence
    66	   4 ee
    67	   4 curricular
    68	   4 computers
    69	   4 complexity
    70	   4 cme
    71	   4 biology
    72	   4 artificial
    73	   3 wim
    74	   3 statistical
    75	   3 social
    76	   3 sets
    77	   3 recognition
    78	   3 reading
    79	   3 processing
    80	   3 parallel
    81	   3 on
    82	   3 object
    83	   3 modeling
    84	   3 mathematical
    85	   3 massive
    86	   3 m
    87	   3 languages
    88	   3 ideas
    89	   3 i
    90	   3 h
    91	   3 great
    92	   3 game
    93	   3 ethics
    94	   3 engr
    95	   3 designing
    96	   3 database
    97	   3 beyond
    98	   3 applications
    99	   3 algorithmic

eg: ./list.sh db/eecs-course-all2014 2 'Machine learning'

    ./list.sh db/eecs-course-all2014 1 '^cs.*Cryptography'

    ./list.sh db/eecs/eecs-course-edx2014 2 '' n n | grep -i ""
    
    ./list.sh db/eecs/ 2 'data' y n
