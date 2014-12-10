#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

school = "coursera"


#coursera


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

def getCategoriyUrl(subject_id):
    return "https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1%28homeLink,logo,name%29,instructors.v1%28firstName,lastName,middleName,prefixName,profileId,shortName,suffixName%29,specializations.v1%28logo,partnerIds,shortName%29,v1Details.v1%28upcomingSessionId%29,v1Sessions.v1%28durationWeeks,hasSigTrack%29&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1%28partnerIds%29,v1Details.v1%28upcomingSessionId%29&extraIncludes=_facets&q=search&languages=en&limit=500" + "&categories=" + subject_id


def getCourseraOnlineCourse(subject, url):
    if need_update_subject(subject) == False:
        return
    r = requests.get(url)
    jobj = json.loads(r.text)

    file_name = get_file_name(subject.strip(), school)
    print "subject " + subject.strip() + " ----> " + file_name
    file_lines = countFileLineNum(file_name)
    f = open_db(file_name + ".tmp")
    count = 0

    print "processing json and write data to file..."
    for item in jobj["elements"]:
        title = item["name"].strip().replace('  ', ' ') + " (" + getPartnerName(item["partnerIds"][0]).strip() + ")"
        title = delZh(title)

        count = count + 1
        link = getHomeLink(item["id"], item["courseType"], item["slug"])
        write_db(f, item["id"], title, link)

    close_db(f)
    if file_lines != count and count > 0:
        do_upgrade_db(file_name)
        print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
    else:
        cancel_upgrade(file_name)
        print "no need upgrade\n"

print "downloading coursera course info"
r = requests.get("https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1%28homeLink,logo,name%29,instructors.v1%28firstName,lastName,middleName,prefixName,profileId,shortName,suffixName%29,specializations.v1%28logo,partnerIds,shortName%29,v1Details.v1%28upcomingSessionId%29,v1Sessions.v1%28durationWeeks,hasSigTrack%29&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1%28partnerIds%29,v1Details.v1%28upcomingSessionId%29&extraIncludes=_facets&q=search&languages=en")


print "loading data..."
jobj = json.loads(r.text)



for subject in jobj["paging"]["facets"]["categories"]["facetEntries"]:
    getCourseraOnlineCourse(subject["name"], getCategoriyUrl(subject["id"]))
    #print subject["id"]
    #print subject["name"]



