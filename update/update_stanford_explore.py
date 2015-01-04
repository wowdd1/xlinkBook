#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *

class StanfordExploreSpider(Spider):
    include_unoffered_courses = True
    
    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"


    def processData(self, f, url):
        print "processing " + url

        r = requests.get(url)
        soup = soup = BeautifulSoup(r.text); 
        course_num_list = []
        course_name_list = []
        course_description_list = []

        for span in soup.find_all("span", attrs={"class": "courseNumber"}):
            course_num_list.append(span.text[0:len(span.text) - 1])

        for span in soup.find_all("span", attrs={"class": "courseTitle"}):
            course_name_list.append(span.text.strip())

        for div in soup.find_all("div", attrs={"class": "courseDescription"}):
            course_description_list.append(div.text.strip()) 

        for i in range(0, len(course_num_list)):
            print course_num_list[i] + " " + course_name_list[i]
            self.write_db(f, course_num_list[i], course_name_list[i], "https://explorecourses.stanford.edu/search?q=" + course_num_list[i], course_description_list[i])
            self.count += 1

    def doWork(self):
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        if self.include_unoffered_courses == True:
            self.processData(f, "https://explorecourses.stanford.edu/print?page=0&q=EE&catalog=&filter-coursestatus-Active=on&descriptions=on&collapse=&academicYear=&catalog=")
            self.processData(f, "https://explorecourses.stanford.edu/print?filter-term-Autumn=off&filter-term-Summer=off&page=0&q=CS&filter-coursestatus-Active=on&descriptions=on&filter-term-Spring=off&filter-departmentcode-CS=on&filter-term-Winter=off&filter-catalognumber-CS=on&collapse=&academicYear=&catalog=")
        else:
            # not included unoffered courses
            self.processData(f, "https://explorecourses.stanford.edu/print?filter-term-Autumn=on&filter-term-Summer=on&page=0&q=EE&filter-coursestatus-Active=on&filter-catalognumber-EE=on&filter-departmentcode-EE=on&descriptions=on&filter-term-Spring=on&collapse=&academicYear=&filter-term-Winter=on&catalog=")
            self.processData(f, "https://explorecourses.stanford.edu/print?filter-term-Autumn=on&filter-term-Summer=on&page=0&q=CS&filter-coursestatus-Active=on&descriptions=on&filter-term-Spring=on&filter-departmentcode-CS=on&filter-catalognumber-CS=on&collapse=&filter-term-Winter=on&academicYear=&catalog=")

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = StanfordExploreSpider()
start.doWork()
