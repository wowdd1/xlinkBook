#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

class PrincetonMathSpider(Spider):

    def __init__(self):    
        Spider.__init__(self)
        self.school = "princeton"
        self.subject = "math"
    
    #princeton
    #"""
    def processPrincetonData(self, f, soup):
        if self.need_update_subject(self.subject) == False:
            return
        for title in soup.find_all("h5", class_="course-title"):
            self.count = self.count + 1
            link = "http://www.math.princeton.edu" + title.span.a["href"]
            self.write_db(f, title.span.a.string[0:title.span.a.string.find(" ")], title.span.a.string[title.span.a.string.find(" "):], link)
    
    def doWork(self):
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
    
        print "downloading princeton course info"
        r = requests.get("http://www.math.princeton.edu/undergraduate/courses")
        soup = BeautifulSoup(r.text)
    
        print "processing html and write data to file..."
        self.processPrincetonData(f, soup)
    
        r = requests.get("http://www.math.princeton.edu/graduate/courses")
        soup = BeautifulSoup(r.text)
    
        self.processPrincetonData(f, soup)
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        #"""
    
start = PrincetonMathSpider()
start.doWork()
