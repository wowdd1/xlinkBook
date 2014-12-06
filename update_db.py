import requests
import json
#from bs4 import BeautifulSoup;
import os,sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

db_dir = os.path.abspath('.') + "/db/"
#coursera
print "download coursera info"
r = requests.get("https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1(homeLink,logo,name),instructors.v1(firstName,lastName,middleName,prefixName,profileId,shortName,suffixName),specializations.v1(logo,partnerIds,shortName),v1Details.v1(upcomingSessionId),v1Sessions.v1(durationWeeks,hasSigTrack)&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1(partnerIds),v1Details.v1(upcomingSessionId)&extraIncludes=_facets&q=search&categories=cs-ai,cs-programming,cs-systems,cs-theory,stats&languages=en&limit=1000")

jobj = json.loads(r.text)


def getPartnerName(id):
    for partner in jobj["linked"]["partners.v1"]:
        if partner["id"] == id:
            return partner["name"]
    return "Unknow"

i = 0
file_name = db_dir + "eecs/cs-course-coursera" + time.strftime("%Y")
f = open(file_name, "w+")
f.truncate()
f.close()

print "processing json..."
f = open(file_name, "a")
for item in jobj["elements"]:
    i = i + 1
    f.write(getPartnerName(item["partnerIds"][0]).strip() + " " + item["name"].strip().replace('  ', ' ') + "\n")


f.close()

#edx
print "download edx info"
r = requests.get("https://www.edx.org/search/api/all")

jobj = json.loads(r.text)



file_name = db_dir + "eecs/eecs-course-edx" + time.strftime("%Y")
f = open(file_name, "w+")
f.truncate()
f.close()

f = open(file_name, "a")

i = 0
print "processing json..."
for item in jobj:
    for subject in item["subjects"]:
        if subject == "Computer Science" or subject == "Electronics":
            f.write(item["schools"][0].strip() + " " + item["code"].strip() + " " +item["l"].strip() + "\n")
            i = i + 1


f.close()



