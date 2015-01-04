#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *


class MitOcwSpider(Spider):

    def __init__(self):
        Spider.__init__(self)    
        self.school = "mit-ocw"
        self.url = "http://ocw.mit.edu"
    #ocw
    #"""
    
    
    def getMitOcwCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        print "processing " + subject + " url " + url
        file_name = self.get_file_name(subject, self.school)
    
        file_lines = self.countFileLineNum(file_name)
        count = 0
        f = self.open_db(file_name + ".tmp")
    
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        course_num = ""
        title = ""
        link = ""
        i = 0
        print "processing html and write data to file..."
        for a in soup.find_all("a", class_="preview"):
            i = i + 1
            if i == 1:
                title += a.string.replace("\n", "").strip() + " "
                link = self.url + str(a["href"])
            if i == 2:
                title += a.string.replace("\n", "").replace("               ", "").strip()
                count = count + 1
                self.write_db(f, title[0:title.find(" ")], title[title.find(" "):], link)
    
                link = ""
                title = ""
            if i >= 3:
                i = 0
    
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
    def doWork(self):
 
        print "downloading ocw course info"
        #r = requests.get("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/")
        r = requests.get("http://ocw.mit.edu/courses/find-by-department")
        soup = BeautifulSoup(r.text);
    
    
        for li in soup.find_all("li"):
            if li.a != None and str(li.a["href"]).startswith("/courses") and str(li.a["href"]).find("find") == -1:
                subject = str(li.a.string).strip()
                if subject.startswith("Audio") or subject.startswith("Find") or subject.startswith("Online Textbooks") \
                    or subject.startswith("New Courses") or subject.startswith("Most Visited Courses") or subject.startswith("OCW Scholar Courses") \
                    or subject.startswith("This Course at MIT") or subject.startswith("Translated Courses"):
                    continue;
                self.getMitOcwCourse(subject, self.url + str(li.a["href"]).strip())
                #print li.a.string
    
start = MitOcwSpider();
start.doWork()
