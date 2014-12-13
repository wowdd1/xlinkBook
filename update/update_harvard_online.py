#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
    
class HarvardOnlineSpider(Spider):

    def __init__(self):
       Spider.__init__(self)
       self. school = "harvard-online"
       self.url = "http://www.extension.harvard.edu/courses"
    #harvard online
    #"""
    
    
    def getHarvardOnlineLink(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        span = soup.find("span", class_ = "syllabi-bullet-hide")
    
        if span != None and span.a != None:
            if span.a.string.lower().find("Course website".lower()) != -1 :
                return str(span.a["href"])
        return url
    
    def getHarvardOnlineCourse(self, subject, url):
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
        print "processing html and write data to file..."
        if len(soup.find_all("li", class_ = "views-row")) > 0:
            for li in soup.find_all("li", class_ = "views-row"):
                if li.span != None:
                    course_num = li.span.span.string
                else:
                    course_num = li.prettify().split("\n")[1].strip()
                course_num = course_num[course_num.find("E-"):]
                title = li.a.string.strip()
                link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
                #link = getHarvardOnlineLink(link)
                count = count + 1
                self.write_db(f, course_num, title, link)
        else:
            for li in soup.find_all("li"):
                if li.attrs.has_key("class"):
                    if li.prettify().find("E-") != -1 and str(li.a["href"]).startswith("/courses"):
                        for item in li.prettify().split("\n"):
                            if item.find("E-") != -1:
                                course_num = item.strip()
                                course_num = course_num[course_num.find("E-"):]
                        #print course_num + " " + li.a.string
                        count = count + 1
                        title = li.a.string.strip()
                        link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
                        #link = getHarvardOnlineLink(link)
                        self. write_db(f, course_num, title, link)
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
    
    def do_work(self):
        print "downloading harvard online course info"
        #r = requests.get("http://www.extension.harvard.edu/courses/subject/computer-science")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
    
    
        for li in soup.find_all("li", class_ = "is-more-items"):
            self.getHarvardOnlineCourse(li.a.string, "http://www.extension.harvard.edu" + str(li.a["href"]))
        
start = HarvardOnlineSpider()
start.do_work() 
