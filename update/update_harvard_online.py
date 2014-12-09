#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "harvard-online/"




#harvard online
#"""


def getHarvardOnlineLink(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    span = soup.find("span", class_ = "syllabi-bullet-hide")

    if span != None and span.a != None:
        if span.a.string.lower().find("Course website".lower()) != -1 :
            return str(span.a["href"])
    return url

def getHarvardOnlineCourse(subject, url):
    print "processing " + subject + " url " + url
    file_name = get_file_name(dir_name + subject)

    file_lines = countFileLineNum(file_name)
    count = 0
    f = open_db(file_name + ".tmp")

    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    course_num = ""
    title = ""
    link = ""
    print "processing html and write data to file..."
    if len(soup.find_all("li", class_ = "views-row")) > 0:
        for li in soup.find_all("li", class_ = "views-row"):
            if li.span != None:
                course_num = li.span.span.string
            else:
                course_num = li.prettify().split("\n")[1].strip()
            course_num = course_num[course_num.find("E-"):]
            title = li.a.string.strip()
            link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
            #link = getHarvardOnlineLink(link)
            count = count + 1
            write_db(f, course_num + " " + title)
            write_db_url(url_f, course_num, link, title)
    else:
        for li in soup.find_all("li"):
            if li.attrs.has_key("class"):
                if li.prettify().find("E-") != -1 and str(li.a["href"]).startswith("/courses"):
                    for item in li.prettify().split("\n"):
                        if item.find("E-") != -1:
                            course_num = item.strip()
                            course_num = course_num[course_num.find("E-"):]
                    #print course_num + " " + li.a.string
                    count = count + 1
                    title = li.a.string.strip()
                    link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
                    #link = getHarvardOnlineLink(link)
                    write_db(f, course_num + " " + title)
                    write_db_url(url_f, course_num, link, title)
    close_db(f)
    if file_lines != count and count > 0:
        do_upgrade_db(file_name)
        print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
    else:
        cancel_upgrade(file_name)
        print "no need upgrade\n"



print "downloading harvard online course info"
#r = requests.get("http://www.extension.harvard.edu/courses/subject/computer-science")
r = requests.get("http://www.extension.harvard.edu/courses")
soup = BeautifulSoup(r.text)

truncateUrlData(dir_name)

url_f = open_url_file(dir_name)

for li in soup.find_all("li", class_ = "is-more-items"):
    getHarvardOnlineCourse(li.a.string, "http://www.extension.harvard.edu" + str(li.a["href"]))
    

close_url_file(url_f)

