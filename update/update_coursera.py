#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *


class CourseraSpider(Spider):

    def __init__(self):
        Spider.__init__(self)    
        self.school = "coursera"
    
    
    #coursera
    
    
    def getPartnerName(self, id, jobj):
        for partner in jobj["linked"]["partners.v1"]:
            if partner["id"] == id:
                return partner["name"]
        return "Unknow"
    
    def getHomeLink(self, id, type, slug, jobj):
        if type == "v1.session":
            for session in jobj["linked"]["v1Sessions.v1"]:
                if session["courseId"] == id:
                    return session["homeLink"]
        return "https://www.coursera.org/course/" + slug
    
    def getCategoriyUrl(self, subject_id):
        return "https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1%28homeLink,logo,name%29,instructors.v1%28firstName,lastName,middleName,prefixName,profileId,shortName,suffixName%29,specializations.v1%28logo,partnerIds,shortName%29,v1Details.v1%28upcomingSessionId%29,v1Sessions.v1%28durationWeeks,hasSigTrack%29&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1%28partnerIds%29,v1Details.v1%28upcomingSessionId%29&extraIncludes=_facets&q=search&languages=en&limit=500" + "&categories=" + subject_id
    
    
    def getCourseraOnlineCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        r = requests.get(url)
        jobj = json.loads(r.text)
    
        file_name = self.get_file_name(subject.strip(), self.school)
        print "subject " + subject.strip() + " ----> " + file_name
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        count = 0
    
        print "processing json and write data to file..."
        for item in jobj["elements"]:
            title = item["name"].strip().replace('  ', ' ') + " (" + self.getPartnerName(item["partnerIds"][0], jobj).strip() + ")"
            title = self.delZh(title)
    
            count = count + 1
            link = self.getHomeLink(item["id"], item["courseType"], item["slug"], jobj)
            self.write_db(f, item["id"], title, link)
    
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
    def do_work(self):
        print "downloading coursera course info"
        r = requests.get("https://www.coursera.org/api/courses.v1?fields=certificates,instructorIds,partnerIds,photoUrl,specializations,startDate,v1Details,partners.v1%28homeLink,logo,name%29,instructors.v1%28firstName,lastName,middleName,prefixName,profileId,shortName,suffixName%29,specializations.v1%28logo,partnerIds,shortName%29,v1Details.v1%28upcomingSessionId%29,v1Sessions.v1%28durationWeeks,hasSigTrack%29&includes=instructorIds,partnerIds,specializations,v1Details,specializations.v1%28partnerIds%29,v1Details.v1%28upcomingSessionId%29&extraIncludes=_facets&q=search&languages=en")
    
    
        print "loading data..."
        jobj = json.loads(r.text)
    
    
    
        for subject in jobj["paging"]["facets"]["categories"]["facetEntries"]:
            self.getCourseraOnlineCourse(subject["name"], self.getCategoriyUrl(subject["id"]))
        #print subject["id"]
        #print subject["name"]
    
   

start = CourseraSpider()
start.do_work() 
