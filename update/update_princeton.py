#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

school = "princeton"
subject = "math"


#princeton
#"""
def processPrincetonData(f, soup):
    if need_update_subject(subject) == False:
        return
    for title in soup.find_all("h5", class_="course-title"):
        global count
        count = count + 1
        link = "http://www.math.princeton.edu" + title.span.a["href"]
        write_db(f, title.span.a.string[0:title.span.a.string.find(" ")], title.span.a.string[title.span.a.string.find(" "):], link)

file_name = get_file_name(subject, school)
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0


print "downloading princeton course info"
r = requests.get("http://www.math.princeton.edu/undergraduate/courses")
soup = BeautifulSoup(r.text)

print "processing html and write data to file..."
processPrincetonData(f, soup)

r = requests.get("http://www.math.princeton.edu/graduate/courses")
soup = BeautifulSoup(r.text)

processPrincetonData(f, soup)

close_db(f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
#"""


