#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "harvard/"


#harvard
#"""
print "downloading harvard course info"
r = requests.get("http://www.registrar.fas.harvard.edu/courses-exams/courses-instruction/computer-science")
soup = BeautifulSoup(r.text)
sys.setrecursionlimit(1400)

truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "cs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0


print "processing html and write data to file..."
for node in soup.find_all("strong"):
    text = ""
    link = ""
    if node.string == None:
        if node.a != None and node.a.string != None:
            text = node.a.string.replace("\n", "")
            link = node.a["href"]
        else:
            if node.a != None:
                link = node.a["href"]
            text = node.prettify()
            if text.find("href=") > 0 :
                text = text[text.find(">", 8) + 1 : text.find("<", text.find(">", 8)) - 1]
            else:
                text = text[text.find(">", 2) + 1 : text.find("<", 8) - 1]
            text = text.replace("\n", "").strip()
    else:
        text = node.string.replace("\n", "")

    count = count + 1
    write_db(f, text)
    write_db_url(url_f, text[0:text.find(".")], link, text[text.find(".") + 2:])



close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
#"""

