import requests
import json
#from bs4 import BeautifulSoup;
import os,sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
import getopt

gen_bookmark = False
filter_keyword = ""
title = ""

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


#coursera
print "download coursera info"
r = requests.get("https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1(homeLink,logo,name),instructors.v1(firstName,lastName,middleName,prefixName,profileId,shortName,suffixName),specializations.v1(logo,partnerIds,shortName),v1Details.v1(upcomingSessionId),v1Sessions.v1(durationWeeks,hasSigTrack)&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1(partnerIds),v1Details.v1(upcomingSessionId)&extraIncludes=_facets&q=search&categories=cs-ai,cs-programming,cs-systems,cs-theory,stats&languages=en&limit=1000")

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

i = 0
if gen_bookmark == False:
    file_name = db_dir + "eecs/cs-course-coursera" + time.strftime("%Y")
else:
    file_name = "coursera-bookmark" + time.strftime("%Y-%m-%d %H:%M:%S") + ".html"
#f = open(file_name, "w+")
#f.truncate()
#f.close()

f = open(file_name, "a")
if gen_bookmark == True:
    print "processing json and gen bookmark"
    head = ""
    if filter_keyword != "":
        head = bookmark_start.replace("course", filter_keyword)
    else:
        head = bookmark_start.replace("course", "coursera")
        
    f.write(head)
else:
    print "processing json..."

for item in jobj["elements"]:
    i = i + 1
    title = item["name"].strip().replace('  ', ' ') + " (" + getPartnerName(item["partnerIds"][0]).strip() + ")"
    if filter_keyword != "":
        if (title.lower().find(filter_keyword.lower()) == -1):
            continue
    if gen_bookmark == False:
        f.write(item["id"] + " " + title +  "\n")
    else:
       f.write('            <DT><A HREF="' + getHomeLink(item["id"], item["courseType"], item["slug"]) + '">' + title + "</A>\n") 


if gen_bookmark == True:
    f.write(bookmark_end)
f.close()

#edx
print "download edx info"
r = requests.get("https://www.edx.org/search/api/all")

jobj = json.loads(r.text)


if gen_bookmark == False:
    file_name = db_dir + "eecs/eecs-course-edx" + time.strftime("%Y")
else:
    file_name = "edx-bookmark" + time.strftime("%Y-%m-%d %H:%M:%S") + ".html"
#f = open(file_name, "w+")
#f.truncate()
#f.close()

f = open(file_name, "a")

i = 0
if gen_bookmark == True:
    print "processing json and gen bookmark"
    head = ""
    if filter_keyword != "":
        head = bookmark_start.replace("course", filter_keyword)
    else:
        head = bookmark_start.replace("course", "edx")
        
    f.write(head)
else:
    print "processing json..."

for item in jobj:
    for subject in item["subjects"]:
        if subject == "Computer Science" or subject == "Electronics" or subject == "Statistics & Data Analysis":
            title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
            if filter_keyword != "":
                if (title.lower().find(filter_keyword.lower()) == -1) and (item["code"].lower().find(filter_keyword.lower()) == -1) :
                    continue

            if gen_bookmark == False:
                f.write(item["code"].strip() + " " + title  + "\n")
            else:
                f.write('            <DT><A HREF="' + item["url"] + '">' + title + "</A>\n")
            i = i + 1


if gen_bookmark == True:
    f.write(bookmark_end)

f.close()

