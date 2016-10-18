#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07


from spider import *


class UdacitySpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "udacity"

    def isCourseInSubject(self, key, keys):
        for k in keys:
            if k == key:
                return True
        return False

    def processUdacityData(self, subject, keys, courses):
        print "processing " + subject 
        print self.school
        file_name = self.get_file_name("eecs/udacity/" + subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for course in courses:
            if self.isCourseInSubject(course["key"], keys) == True:
                self.count += 1
                title = course["title"].strip()
                if course["project_name"] != None and len(course["project_name"].strip()) > 4:
                    title = title + " - " + course["project_name"]
                elif course['subtitle'] != None and len(course['subtitle'].strip()) > 4:
                    title = title + " - " + course['subtitle']
                remark = ""
                instructors = 'instructors:'
                project = ''
                if course['available'] == True:
                    remark = "available:yes "
                else:
                    remark = "available:no "
                for instructor in course['instructors']:
                    instructors += instructor['name'] + ', '
                instructors = instructors[0 : len(instructors) - 2]
                if course['project_name'] != '':
                    project = 'project:' + course['project_name'] +  ' '
                remark += "level:" + course['level'] + ' ' + instructors + project + ' description:' + course['summary'].replace('\n', '')
 
                self.write_db(f, course["key"], title, "https://www.udacity.com/course/" + course["key"], remark)
                print course["key"] + " " + title + " " + "https://www.udacity.com/course/" + course["key"]
                
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n" 

    def doWork(self):
        url = "https://www.udacity.com/public-api/v0/courses?projection=internal"
        print "downloading udacity course info"
        r = requests.get(url)

        print "loading data..."
        jobj = json.loads(r.text)

        for k,v in jobj.items():
            if k == "tracks":
                for item in v:
                    if item["name"] != "All" and item['name'] != None:
                        self.processUdacityData(item["name"], item["courses"], jobj["courses"])


start = UdacitySpider()
start.doWork()
#https://www.udacity.com/public-api/v0/courses?projection=internal
