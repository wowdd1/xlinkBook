#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *
school = "163-ocw"
subject = "163-ocw"
#163 ocw
#"""
def process163Data(soup):
    if need_update_subject(subject) == False:
        return
    file_name = get_file_name(subject, school)
    file_lines = countFileLineNum(file_name)
    f = open_db(file_name + ".tmp")
    count = 0
    for div in soup.find_all("div", class_ = "g-cell1 g-card1"):
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
                write_db(f, course_num, title, str(a["href"]))

    close_db(f)
    if file_lines != count and count > 0:
        do_upgrade_db(file_name)
        print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
    else:
        cancel_upgrade(file_name)
        print "no need upgrade\n"


print "downloading 163 ocw info"
r = requests.get("http://open.163.com/ocw/")
soup = BeautifulSoup(r.text)


process163Data(soup)



