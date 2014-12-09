#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "berkeley/"

#berkeley
#"""
print "downloading berkeley course info"
r = requests.get("http://www-inst.eecs.berkeley.edu/classes-cs.html")
soup = BeautifulSoup(r.text)

truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "eecs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0


def processBerkeleyData(f, tr):
    i = 0
    title = ""
    link = ""
    for td in tr.children:
       if i == 3:
           title = title + td.a.string + " "
       if i == 5:
           title = title + td.u.string
           link = "http://www-inst.eecs.berkeley.edu" + td.a["href"]
       i = i + 1
    if i > 4:
        global count
        count = count + 1
        write_db(f, title)
        write_db_url(url_f, title[0:title.find(" ")], link, title[title.find(" "):])


print "processing html and write data to file..."
for table in soup.find_all("table", attrs={"class": "column"}):
    tr =  table.tr
    processBerkeleyData(f, tr)

    for next_tr in tr.next_siblings:
        if next_tr.string == None:
            processBerkeleyData(f, next_tr)



close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"


