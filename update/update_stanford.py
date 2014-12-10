#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

school = "stanford"
subject = "eecs"

#stanford
#"""
print "downloading stanford course info"

#for page in range(0, 2):
#    url = "https://explorecourses.stanford.edu/search?filter-term-Summer=on&filter-coursestatus-Active=on&filter-departmentcode-EE=on&filter-term-Spring=on&filter-term-Winter=on&filter-term-Autumn=on&page=" + str(page) + "&q=EE&filter-catalognumber-EE=on&view=catalog&academicYear=&collapse="

file_name = get_file_name(subject, school)
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0

def processStanfordDate(f, html):
    if need_update_subject(subject) == False:
        return
    soup = BeautifulSoup(html)
    th_set = soup.find_all("th")
    td_set_all = soup.find_all("td")
    td_set = []
    del th_set[0:5]

    i = 0
    for td in td_set_all:
        i = i + 1
        if i == 1:
            td_set.append(td.string)
        if i == 4:
            i = 0

    for index in range(0,len(th_set)):
        link = th_set[index].prettify()
        link = link[link.find("http"):link.find("EDU") + 3]
        title = th_set[index].string + " " + td_set[index]
        global count
        count = count + 1
        write_db(f, th_set[index].string, td_set[index], link)

url = "http://cs.stanford.edu/courses/schedules/2014-2015.autumn.php"
r = requests.get(url)
#print r.status_code
print "processing html and write data to file..."
processStanfordDate(f, r.text)

url = "http://cs.stanford.edu/courses/schedules/2014-2015.winter.php"
r = requests.get(url)
#print r.status_code
processStanfordDate(f, r.text)

url = "http://cs.stanford.edu/courses/schedules/2014-2015.spring.php"
r = requests.get(url)
#print r.status_code
processStanfordDate(f, r.text)

url = "http://cs.stanford.edu/courses/schedules/2013-2014.summer.php"
r = requests.get(url)
#print r.status_code
processStanfordDate(f, r.text)


close_db(f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
#"""




