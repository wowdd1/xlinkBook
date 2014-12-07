
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
import getopt

gen_bookmark = False
filter_keyword = ""
title = ""
count = 0
file_lines = 0

def Usage():
    print 'usage:'
    print '-h,--help: print help message.'
    print '-b,--bookmark: gen bookmark file'
    print '-f,--filter: keyword for filter course'

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hbf:', [])
except getopt.GetoptError, err:
    print str(err)
    Usage()
    sys.exit(2)

for o, a in opts:
    if o in ('-h', '--help'):
        Usage()
        sys.exit(1)
    elif o in ('-b', '--bookmark'):
        gen_bookmark = True
    elif o in ('-f', '--filter'):
        filter_keyword = str(a).strip()


db_dir = os.path.abspath('.') + "/db/"
bookmark_start = '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n\
<!-- This is an automatically generated file.\n\
     It will be read and overwritten.\n\
     DO NOT EDIT! -->\n\
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n\
<TITLE>Bookmarks</TITLE>\n\
<H1>Bookmarks</H1>\n\
<DL><p>\n\
    <DT><H3 ADD_DATE="" LAST_MODIFIED="" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Bar</H3>\n\
    <DL><p>\n\
        <DT><H3 ADD_DATE="" LAST_MODIFIED="">course</H3>\n\
        <DL><p>\n'
bookmark_end = '        </DL><p>\n\
    </DL><p>\n\
</DL><p>'


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
    if arg == "princeton":
        file_name_part = db_dir + "mathematics/math-course-princeton"
    
    if gen_bookmark == False:
        file_name = file_name_part + time.strftime("%Y")
    else:
        file_name = arg + "-bookmark" + time.strftime("%Y-%m-%d") + ".html"

    return file_name
    
def write_bookmark_head(f, folder_name):
    print "gen bookmark head"
    head = ""
    if filter_keyword != "":
        head = bookmark_start.replace("course", filter_keyword)
    else:
        head = bookmark_start.replace("course", folder_name)  
    
    f.write(head) 

def write_bookmark_body(f, link, title):
    if link == "":
        return
    f.write('            <DT><A HREF="' + link + '">' + title + "</A>\n")

def write_bookmark_footer(f):
    print "gen bookmark footer"
    f.write(bookmark_end)    

def write_db(f, data):
    f.write(data +  "\n")


def skip(data):
    if filter_keyword != "":
        if (data.lower().find(filter_keyword.lower()) == -1):
            return True
    return False
 
def truncateData(file_name):
    if os.path.exists(file_name):
        print "truncate " + file_name + " data"
        line_count = count = len(open(file_name,'rU').readlines())
        f = open(file_name, "w+")
        f.truncate()
        f.close()
        return line_count
    return 0
 
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

file_name = get_file_name("coursera")

file_lines = truncateData(file_name)

f = open(get_file_name("coursera"), "a")

if gen_bookmark == True:
   write_bookmark_head(f, "coursera") 


print "processing json and write data to file..."
for item in jobj["elements"]:
    title = item["name"].strip().replace('  ', ' ') + " (" + getPartnerName(item["partnerIds"][0]).strip() + ")"

    if skip(item["id"] + " " + title):
        continue
    count = count + 1
    if gen_bookmark == False:
        write_db(f, item["id"] + " " + title)
    else:
        write_bookmark_body(f,getHomeLink(item["id"], item["courseType"], item["slug"]), title)


if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()

print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""


#edx
#"""
print "downloading edx course info"
r = requests.get("https://www.edx.org/search/api/all")


print "loading data..."
jobj = json.loads(r.text)


file_name = get_file_name("edx")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "edx")
    
print "processing json and write data to file..."
for item in jobj:
    for subject in item["subjects"]:
        if subject == "Computer Science" or subject == "Electronics" or subject == "Statistics & Data Analysis":
            title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
            if skip(item["code"] + " " + title):
                continue
            count = count + 1
            if gen_bookmark == False:
                write_db(f, item["code"].strip() + " " + title)
            else:
                write_bookmark_body(f, item["url"], title)


if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
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
        if skip(content[1].strip()):
            continue
        global count
        count = count + 1
        if gen_bookmark == False:
            write_db(f, content[1].strip())
        else:
            write_bookmark_body(f, getMitCourseLink(links, content[1].strip()[0:content[1].strip().find(" ")]), content[1].strip())



r_a = requests.get("http://student.mit.edu/catalog/m6a.html")
r_b = requests.get("http://student.mit.edu/catalog/m6b.html")
r_c = requests.get("http://student.mit.edu/catalog/m6c.html")


file_name = get_file_name("mit")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "mit")

print "processing html and write data to file..."
processMitData(r_a.text, f)
processMitData(r_b.text, f)
processMitData(r_c.text, f)

if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""


#ocw
#"""
print "downloading ocw course info"
r = requests.get("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/")

soup = BeautifulSoup(r.text);
i = 0

file_name = get_file_name("ocw")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "ocw")

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
        if skip(title):
            ref = ""
            title = ""
            continue
        count = count + 1
        if gen_bookmark == False:
            write_db(f, title)
        else:
            write_bookmark_body(f, ref, title)
        
        ref = ""
        title = ""
    if i >= 3:
        i = 0


if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
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
        if skip(title):
            continue
        global count
        count = count + 1
        if gen_bookmark == False:
            write_db(f, title)
        else:
            write_bookmark_body(f, link, title)


file_name = get_file_name("stanford")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "stanford")


 
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

if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""






#berkeley
#"""
print "downloading berkeley course info"
r = requests.get("http://www-inst.eecs.berkeley.edu/classes-cs.html")
soup = BeautifulSoup(r.text)


file_name = get_file_name("berkeley")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "berkeley")


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
        if skip(title):
            return
        global count
        count = count + 1
        if gen_bookmark == False:
            write_db(f, title)
        else:
            write_bookmark_body(f, link, title)


print "processing html and write data to file..."
for table in soup.find_all("table", attrs={"class": "column"}):
    tr =  table.tr
    processBerkeleyData(f, tr)

    for next_tr in tr.next_siblings:
        if next_tr.string == None:
            processBerkeleyData(f, next_tr)


if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""

#harvard
#"""
print "downloading harvard course info"
r = requests.get("http://www.registrar.fas.harvard.edu/courses-exams/courses-instruction/computer-science")
soup = BeautifulSoup(r.text)
sys.setrecursionlimit(1400)


file_name = get_file_name("harvard")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "harvard")

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

    if skip(text):
        continue
    count = count + 1
    if gen_bookmark == False:
        write_db(f, text)
    else:
        write_bookmark_body(f, link, text)    


if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""





#princeton
#"""
def processPrincetonData(f, soup):
    for title in soup.find_all("h5", class_="course-title"):
        if skip(title.span.a.string):
            continue
        global count
        count = count + 1
        if gen_bookmark == False:
            write_db(f, title.span.a.string)
        else:
            write_bookmark_body(f, "http://www.math.princeton.edu" + title.span.a["href"], title.span.a.string)



file_name = get_file_name("princeton")

file_lines = truncateData(file_name)

f = open(file_name, "a")

if gen_bookmark == True:
   write_bookmark_head(f, "princeton")


print "downloading princeton info"
r = requests.get("http://www.math.princeton.edu/undergraduate/courses")
soup = BeautifulSoup(r.text)

print "processing html and write data to file..."
processPrincetonData(f, soup)

r = requests.get("http://www.math.princeton.edu/graduate/courses")
soup = BeautifulSoup(r.text)

processPrincetonData(f, soup)

if gen_bookmark == True:
    write_bookmark_footer(f)

f.close()
print "before lines: " + str(file_lines) + " after update: " + str(count) + " Done!!!\n\n"
count = 0
#"""
