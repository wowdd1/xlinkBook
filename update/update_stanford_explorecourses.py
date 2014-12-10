#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "stanford/"


#stanford
"""
print "downloading stanford course info"

#for page in range(0, 2):
#    url = "https://explorecourses.stanford.edu/search?filter-term-Summer=on&filter-coursestatus-Active=on&filter-departmentcode-EE=on&filter-term-Spring=on&filter-term-Winter=on&filter-term-Autumn=on&page=" + str(page) + "&q=EE&filter-catalognumber-EE=on&view=catalog&academicYear=&collapse="

truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "cs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0



close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
"""




