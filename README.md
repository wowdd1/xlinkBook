usage:  

    ./list.py -i filename or dirname -c column_num -f 'keyword or regexp' -s -d -w 100 -r 5

-i: file name or dir name

-c: column_num, from 1 to 3

-f: filter keyword
    
    if you input keyword, like -f 'instructors:someone', it will search only the instructors field that contain someone,
    
    otherwise, it will search only in title that contain keyword

-s: output with color

-d: output the description

-w: custom the cell length

-r: the rows of the description

-t: the top rows for display

keyword or regexp: the keyword for filter course


eg: 

    ./list.py -i db/eecs-course-all2014 -c 2 -f 'Machine learning'

    ./list.py -i db/eecs-course-all2014 -c 1 -f '^cs.*Cryptography'

    ./list.py -i db/eecs/eecs-course-edx2014 -c 2 | grep -i ""
    
    ./list.py -i db/eecs/ -c 1 -f 'data' -s -d -w 130

    /list.py -i db/eecs/ -f 'data' -l 1

the output would looks like this:

    +-----------+----------------------------------+---------+------------+---------+---------------------------+
    |id         |title                             |id       |title       |id       |title                      |
    +-----------+----------------------------------+---------+------------+---------+---------------------------+
    |17830-3603 | docker                           |2216-49  | pup        |1302-186 | gorp                      |
    |10176-895  | lime                             |2187-290 | web        |1290-135 | tsuru                     |
    |5990-374   | syncthing                        |2160-197 | godropbox  |1268-52  | delve                     |
    |5971-582   | martini                          |2136-291 | goread     |1266-82  | otto                      |
    |5504-860   | kubernetes                       |2100-511 | Heartbleed |1229-96  | goconvey                  |
    |5160-1976  | build-web-application-with-gol...|2087-243 | gocode     |1214-62  | bleve                     |
    |5043-541   | etcd                             |2081-94  | ga-beacon  |1210-127 | gorm                      |
    |5005-472   | hub                              |2035-70  | alpaca     |1191-117 | confd                     |
    |4974-343   | cayley                           |2029-141 | cli        |1188-179 | pq                        |
    |4939-390   | gogs                             |2026-99  | vegeta     |1184-144 | raft                      |
    |4901-227   | go                               |1960-70  | peco       |1182-76  | packetbeat                |
    |4541-681   | revel                            |1931-226 | vitess     |1166-102 | qml                       |
    |4182-412   | drone                            |1894-77  | gopherjs   |1149-110 | camlistore                |
    |3950-297   | influxdb                         |1887-106 | gor        |1143-125 | goquery                   |
    |3873-268   | ngrok                            |1862-111 | goji       |1112-55  | goagain                   |
    |3715-375   | nsq                              |1817-207 | terraform  |1102-258 | mysql                     |
    |3532-867   | beego                            |1813-88  | ui         |1096-37  | elvish                    |
    |3481-144   | websocketd                       |1809-164 | gin        |1073-152 | blackfriday               |
    |3428-629   | packer                           |1769-136 | swarm      |1071-90  | tiedot                    |
    |3219-284   | groupcache                       |1769-213 | heka       |1064-90  | go-json-rest              |
    |3041-185   | flynn                            |1733-99  | negroni    |1056-40  | inspeqtor                 |
    |3010-266   | shipyard                         |1703-91  | boom       |1053-157 | redigo                    |
    |2935-191   | rocket                           |1647-261 | codis      |1047-178 | mux                       |
    |2910-97    | textql                           |1622-74  | bolt       |1043-64  | httprouter                |
    |2680-399   | hugo                             |1616-141 | cadvisor   |1041-386 | the-way-to-go_ZH_CN       |
    |2657-195   | serf                             |1577-131 | golearn    |1037-29  | roshi                     |
    |2599-164   | zeus                             |1513-111 | GoSublime  |1001-137 | skynet                    |
    |2576-116   | weave                            |1482-80  | libchan    |989-52   | goworker                  |
    |2574-98    | pgweb                            |1462-101 | godep      |930-259  | logstash-forwarder        |
    |2559-172   | cockroach                        |1434-149 | fleet      |919-288  | go-fundamental-programm...|
    |2516-225   | consul                           |1388-199 | freegeoip  |911-81   | streamtools               |
    |2250-194   | doozerd                          |1325-205 | cow        |904-40   | coop                      |
    +-----------+----------------------------------+---------+------------+---------+---------------------------+

    Total 96 records, File: db/eecs/github/go-github2014

if you provide the -d option, it will output the describe info:

    +---------+------------------------------------------------------------------------------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------+
    |id       |title                                                                                                                   |id       |title                                                                                                                   |
    +---------+------------------------------------------------------------------------------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------+
    |3000-940 | otp                                                                                                                    |1177-303 | mochiweb                                                                                                               |
    |         | Erlang/OTP (author:erlang stars:3000 forks:940 watchers:3000)                                                          |         | MochiWeb is an Erlang library for building lightweight HTTP servers. (author:mochi stars:1177 forks:303 watchers:1177) |
    |         |                                                                                                                        |         |                                                                                                                        |
    |1852-503 | cowboy                                                                                                                 |1035-267 | rebar                                                                                                                  |
    |         | Small, fast, modular HTTP server written in Erlang. (author:ninenines stars:1852 forks:503 watchers:1852)              |         | ATTENTION: Please find the canonical repository here:  (author:basho stars:1035 forks:267 watchers:1035)               |
    |         |                                                                                                                        |         |                                                                                                                        |
    |1360-451 | ejabberd                                                                                                               |1023-186 | disco                                                                                                                  |
    |         | Robust and scalable Jabber / XMPP Instant Messaging platform (author:processone stars:1360 forks:451 watchers:1360)    |         | a Map/Reduce framework for distributed computing (author:discoproject stars:1023 forks:186 watchers:1023)              |
    |         |                                                                                                                        |         |                                                                                                                        |
    |1182-233 | ChicagoBoss                                                                                                            |1014-212 | webmachine                                                                                                             |
    |         | Erlang web MVC, now featuring Comet (author:ChicagoBoss stars:1182 forks:233 watchers:1182)                            |         | A REST-based system for building web applications.  (author:basho stars:1014 forks:212 watchers:1014)                  |
    |         |                                                                                                                        |         |                                                                                                                        |
    +---------+------------------------------------------------------------------------------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------+

    Total 8 records, File: db/eecs/github/erlang-github2014


upgrade db: 

    cd update/

    run ./upgrade_db.py


browse course in browser: 

    run ./goto.py -c "course number" or ./goto.py "course number"
        ./goto.py -q 'keyword'

ex: 

     ./goto.py -c "6.001"
     ./goto.py -c "E-100" -e 'yaohoo'
     ./goto.py -c '6.001' -e 'youtube'
     ./goto.py -q 'data mining'

display one course info:

    ./about_course.py 'course number'

ex:

     ./about_course.py '6.001'


find the instructor:

    ./find_professor "faculty name"

ex:
    
    ./find_professor "Andrew Ng"
