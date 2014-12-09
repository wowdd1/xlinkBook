#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
from common import *

dir_name = "mit/"

#mit
#"""
print "downloading mit course info"
truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "eecs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0


def getMitCourseLink(links, course_num):
    if course_num == "":
        return course_num
    for link in links:
        if link.attrs.has_key("href") and link["href"].find(course_num) != -1 and link["href"].find("editcookie.cgi") == -1:
            return link["href"]
    return ""
    

def processMitData(html, f):
    soup = BeautifulSoup(html);
    links_all = soup.find_all("a")
    links = []
    for link in links_all:
        if link.attrs.has_key("href") and False == link["href"].startswith("editcookie.cgi") \
           and False == link["href"].startswith("/ent/cgi-bin") and False == link["href"].startswith("javascript:") \
           and False == link["href"].startswith("m"):
            links.append(link)
    content = []
    for tag in soup.find_all("h3"):
        content = tag.prettify().split("\n")
        global count
        count = count + 1
        course_num = content[1].strip()[0:content[1].strip().find(" ")]
        link = getMitCourseLink(links, course_num)

        write_db(f, content[1].strip())
        write_db_url(url_f, course_num, link, content[1].strip()[content[1].strip().find(" "):])



r_a = requests.get("http://student.mit.edu/catalog/m6a.html")
r_b = requests.get("http://student.mit.edu/catalog/m6b.html")
r_c = requests.get("http://student.mit.edu/catalog/m6c.html")


print "processing html and write data to file..."
processMitData(r_a.text, f)
processMitData(r_b.text, f)
processMitData(r_c.text, f)


close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
#"""

