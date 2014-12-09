#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "coursera/"


#coursera
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

truncateUrlData(dir_name)

url_f = open_url_file(dir_name)

file_name = get_file_name(dir_name + "cs")

file_lines = countFileLineNum(file_name)

f = open_db(file_name + ".tmp")
count = 0

print "processing json and write data to file..."
for item in jobj["elements"]:
    title = item["name"].strip().replace('  ', ' ') + " (" + getPartnerName(item["partnerIds"][0]).strip() + ")"
    title = delZh(title)

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

close_url_file(url_f)

