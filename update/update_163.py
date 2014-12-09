#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *
dir_name = "163-ocw/"

#163 ocw
#"""
def process163Data(f, soup):
    for div in soup.find_all("div", class_ = "g-cell1 g-card1"):
        global count
        count = count + 1
        course_num = "163-ocw-" + str(count)
        for a in div.find_all("a"):
            if a.attrs.has_key("class") == False:
                #print a.h5.string
                #print a["href"]
                title = ""
                if a.h5.string == None:
                    pos = str(a.h5).find(">", 3)
                    title = str(a.h5)[pos + 1: str(a.h5).find("<" , pos)]
                else:
                    title = a.h5.string
                write_db(f, course_num + " " + title)
                write_db_url(url_f, course_num, str(a["href"]), title)


truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "eecs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0


print "downloading 163 ocw info"
r = requests.get("http://open.163.com/ocw/")
soup = BeautifulSoup(r.text)


process163Data(f, soup)


close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"

