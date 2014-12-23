usage:  

./list.py -i filename or dirname -c column_num -f 'keyword or regexp'] -r -s 

filename or dirname: the file or dir

column_num: from 1 to 3

keyword or regexp: the keyword for filter course

keyword suggest(to list keyword, please run ./list.py -k filename):

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

eg: 

    ./list.py -i db/eecs-course-all2014 -c 2 -f 'Machine learning'

    ./list.py -i db/eecs-course-all2014 -c 1 -f '^cs.*Cryptography'

    ./list.py -i db/eecs/eecs-course-edx2014 -c 2 | grep -i ""
    
    ./list.py -i db/eecs/ -c 2 -f 'data' -r -s

the output would looks like this:

    +----------+----------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------+
    |id        |title                                                                       |id        |title                                                                        |
    +----------+----------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------+
    |6572-1996 | FlappySwift                                                                |1437-214  | iOS8-day-by-day                                                             |
    |5876-576  | Alamofire                                                                  |1325-61   | Surge                                                                       |
    |2764-190  | Design-Patterns-In-Swift                                                   |1289-100  | animated-tab-bar                                                            |
    |2631-288  | SwiftyJSON                                                                 |1232-92   | ExSwift                                                                     |
    |1771-95   | Dollar.swift                                                               |1209-92   | hamburger-button                                                            |
    |1724-137  | Quick                                                                      |1073-134  | Swifter                                                                     |
    |1618-122  | LTMorphingLabel                                                            |1043-94   | SCLAlertView-Swift                                                          |
    |1537-416  | swift-2048                                                                 |1017-195  | Chats                                                                       |
    |1505-121  | swiftz                                                                     |1010-301  | SwiftWeather                                                                |
    |1475-62   | Cartography                                                                |990-267   | SwiftGuide                                                                  |
    +----------+----------------------------------------------------------------------------+----------+-----------------------------------------------------------------------------+

    Total 20 records, File: db/eecs/github/swift-github2014

upgrade db: 

    cd update/

    run ./upgrade_db.py

gen bookmark:


    run ./gen_bookmark.py  -b -f "keyword"

ex:  

    ./gen_bookmark.py  -b -f "computer"


browse course in browser: 

    run ./search_web.py -s "course number"

ex: 

     ./search_web.py -s "6.001"
     ./search_web.py -s "E-100" -e yaohoo
