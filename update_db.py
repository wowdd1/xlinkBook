#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07


import requests
import json
from bs4 import BeautifulSoup;
import os,sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

title = ""
count = 0
file_lines = 0
file_name = ""
google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
baidu = "http://www.baidu.com/s?word="
bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="
db_dir = os.path.abspath('.') + "/db/"
local_url_file = db_dir + ".urls"


def get_file_name(arg):
    file_name_part = ""
    if arg == "coursera":
        file_name_part = db_dir + "eecs/cs-course-coursera"
    if arg == "edx":
        file_name_part = db_dir + "eecs/eecs-course-edx"
    if arg == "stanford":
        file_name_part = db_dir + "eecs/cs-course-stanford"
    if arg == "mit":
        file_name_part = db_dir + "eecs/eecs-course-mit"
    if arg == "berkeley":
        file_name_part = db_dir + "eecs/eecs-course-berkeley"
    if arg == "ocw":
        file_name_part = db_dir + "eecs/eecs-course-mit-ocw"
    if arg == "harvard":
        file_name_part = db_dir + "eecs/cs-course-harvard"
    if arg == "harvard-online":
        file_name_part = db_dir + "eecs/cs-course-open-harvard"
    if arg == "princeton":
        file_name_part = db_dir + "mathematics/math-course-princeton"
    if arg == "163-ocw":
        file_name_part = db_dir + "163/all-course-163-ocw" 
    return file_name_part + time.strftime("%Y")


def open_db(file_name):
    if os.path.exists(file_name) == False:
        index = 0
        for i in range(0, len(file_name)):
            if file_name[i] == "/":
                index = i
        if os.path.exists(file_name[0:index]) == False:
            os.makedirs(file_name[0:index])

    try:
        f = open(file_name, "a")
    except IOError, err:
        print str(err)
    return f

def do_upgrade_db(file_name):
    if os.path.exists(file_name) and os.path.exists(file_name + ".tmp"):
        print "upgrading..."
        print "remove " + file_name[file_name.find("db"):]
        os.remove(file_name)
        print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(file_name + ".tmp", file_name)
        print "upgrade done"
    elif os.path.exists(file_name + ".tmp"):
        print "upgrading..."
        print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(file_name + ".tmp", file_name)
        print "upgrade done"
    else:
        print "upgrade error"
def cancel_upgrade(file_name):
    if os.path.exists(file_name + ".tmp"):
        os.remove(file_name + ".tmp")

def close_db(f):
    f.close()
    

def write_db(f, data):
    f.write(data +  "\n")

def write_db_url(url_f, course_num, url, course_name):
    if url == "":
        url = google + course_num + " " + course_name

    url_f.write(course_num + " | " + url.strip() + " | " + course_name +  "\n")

 
def countFileLineNum(file_name):
    if os.path.exists(file_name):
        line_count = count = len(open(file_name,'rU').readlines())
        #f = open(file_name, "w+")
        #f.truncate()
        #f.close()
        return line_count
    return 0

def truncateUrlData():
    global local_url_file
    print "truncateUrlData ...."
    f = open(local_url_file, "w+")
    f.truncate()
    f.close


url_f = open(local_url_file, "a") 


#coursera
#"""
print "downloading coursera course info"
r = requests.get("https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1(homeLink,logo,name),instructors.v1(firstName,lastName,middleName,prefixName,profileId,shortName,suffixName),specializations.v1(logo,partnerIds,shortName),v1Details.v1(upcomingSessionId),v1Sessions.v1(durationWeeks,hasSigTrack)&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1(partnerIds),v1Details.v1(upcomingSessionId)&extraIncludes=_facets&q=search&categories=cs-ai,cs-programming,cs-systems,cs-theory,stats&languages=en&limit=1000")

print "loading data..."
jobj = json.loads(r.text)


def getPartnerName(id):
    for partner in jobj["linked"]["partners.v1"]:
        if partner["id"] == id:
            return partner["name"]
    return "Unknow"

def getHomeLink(id, type, slug):
    if type == "v1.session":
        for session in jobj["linked"]["v1Sessions.v1"]:
            if session["courseId"] == id:
                return session["homeLink"]
    return "https://www.coursera.org/course/" + slug

truncateUrlData()

file_name = get_file_name("coursera")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")


print "processing json and write data to file..."
for item in jobj["elements"]:
    title = item["name"].strip().replace('  ', ' ') + " (" + getPartnerName(item["partnerIds"][0]).strip() + ")"

    count = count + 1
    link = getHomeLink(item["id"], item["courseType"], item["slug"])
    write_db(f, item["id"] + " " + title)
    write_db_url(url_f, item["id"], link, title)


close_db(f)

if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""


#edx
#"""
print "downloading edx course info"
r = requests.get("https://www.edx.org/search/api/all")


print "loading data..."
jobj = json.loads(r.text)


file_name = get_file_name("edx")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")

    
print "processing json and write data to file..."
for item in jobj:
    for subject in item["subjects"]:
        if subject == "Computer Science" or subject == "Electronics" or subject == "Statistics & Data Analysis":
            title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
            count = count + 1
            write_db(f, item["code"].strip() + " " + title)
            write_db_url(url_f, item["code"].strip(), item["url"], title)

close_db(f)

if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""






#mit
#"""
print "downloading mit course info"

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


file_name = get_file_name("mit")

file_lines = countFileLineNum(file_name)

f  = open_db(file_name + ".tmp")


print "processing html and write data to file..."
processMitData(r_a.text, f)
processMitData(r_b.text, f)
processMitData(r_c.text, f)


close_db(f)

if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""


#ocw
#"""
print "downloading ocw course info"
r = requests.get("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/")

soup = BeautifulSoup(r.text);
i = 0

file_name = get_file_name("ocw")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")


print "processing html and write data to file..."

ref = ""
title = ""
for link in soup.find_all("a", class_="preview"):
    i = i + 1
    if i == 1:
        title += link.string.replace("\n", "").strip() + " "
        ref = "http://ocw.mit.edu" + link["href"]
    if i == 2:
        title += link.string.replace("\n", "").replace("               ", "").strip()
        count = count + 1
        write_db(f, title)
        write_db_url(url_f, title[0:title.find(" ")], ref, title[title.find(" "):])
        
        ref = ""
        title = ""
    if i >= 3:
        i = 0

close_db(f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""





#stanford
#"""
print "downloading stanford course info"

#for page in range(0, 2):
#    url = "https://explorecourses.stanford.edu/search?filter-term-Summer=on&filter-coursestatus-Active=on&filter-departmentcode-EE=on&filter-term-Spring=on&filter-term-Winter=on&filter-term-Autumn=on&page=" + str(page) + "&q=EE&filter-catalognumber-EE=on&view=catalog&academicYear=&collapse="

def processStanfordDate(f, html):
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
        write_db(f, title)
        write_db_url(url_f, th_set[index].string, link, td_set[index]) 


file_name = get_file_name("stanford")

file_lines = countFileLineNum(file_name)

f  = open_db(file_name + ".tmp")

 
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
count = 0
#"""






#berkeley
#"""
print "downloading berkeley course info"
r = requests.get("http://www-inst.eecs.berkeley.edu/classes-cs.html")
soup = BeautifulSoup(r.text)


file_name = get_file_name("berkeley")

file_lines = countFileLineNum(file_name)

f  = open_db(file_name + ".tmp")


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
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""




#harvard
#"""
print "downloading harvard course info"
r = requests.get("http://www.registrar.fas.harvard.edu/courses-exams/courses-instruction/computer-science")
soup = BeautifulSoup(r.text)
sys.setrecursionlimit(1400)


file_name = get_file_name("harvard")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")


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
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""


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

print "downloading harvard online course info"
r = requests.get("http://www.extension.harvard.edu/courses/subject/computer-science")
soup = BeautifulSoup(r.text)

file_name = get_file_name("harvard-online")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")

print "processing html and write data to file..."
for li in soup.find_all("li", class_ = "views-row"):
    course_num = li.prettify().split("\n")[1].strip()
    course_num = course_num[course_num.lower().find("e"):]
    title = li.a.string.strip()
    link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
    link = getHarvardOnlineLink(link)

    count = count + 1
    write_db(f, course_num + " " + title)
    write_db_url(url_f, course_num, link, title)

close_db(f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"
count = 0
#"""



#princeton
#"""
def processPrincetonData(f, soup):
    for title in soup.find_all("h5", class_="course-title"):
        global count
        count = count + 1
        link = "http://www.math.princeton.edu" + title.span.a["href"]
        write_db(f, title.span.a.string)
        write_db_url(url_f, title.span.a.string[0:title.span.a.string.find(" ")], link, title.span.a.string[title.span.a.string.find(" "):])


file_name = get_file_name("princeton")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")


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
count = 0
#"""


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


file_name = get_file_name("163-ocw")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")

print "downloading 163 ocw info"
r = requests.get("http://open.163.com/ocw/")
soup = BeautifulSoup(r.text)


process163Data(f, soup)


close_db(f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"

count = 0           
#"""



if url_f != None:
    url_f.close()

