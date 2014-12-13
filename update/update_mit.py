#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
from spider import *

class MitSpider(Spider):
    
    def __init__(self):
        Spider.__init__(self)    
        self.school = "mit"
        self.subject = "eecs"
    
    def getMitCourseLink(self, links, course_num):
        if course_num == "":
            return course_num
        for link in links:
            if link.attrs.has_key("href") and link["href"].find(course_num) != -1 and link["href"].find("editcookie.cgi") == -1:
                return link["href"]
        return ""
        
    
    def processMitData(self, html, f):
        if self.need_update_subject(self.subject) == False:
            return
        soup = BeautifulSoup(html);
        links_all = soup.find_all("a")
        links = []
        for link in links_all:
            if link.attrs.has_key("href") and False == link["href"].startswith("editcookie.cgi") \
               and False == link["href"].startswith("/ent/cgi-bin") and False == link["href"].startswith("javascript:") \
               and False == link["href"].startswith("m"):
                links.append(link)
        content = []
        for tag in soup.find_all("h3"):
            content = tag.prettify().split("\n")
            self.count = self.count + 1
            course_num = content[1].strip()[0:content[1].strip().find(" ")]
            link = self.getMitCourseLink(links, course_num)
    
            self.write_db(f, course_num, content[1].strip()[content[1].strip().find(" "):], link)
    
    def do_work(self):
        #mit
        #"""
        print "downloading mit course info"
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
    
        r_a = requests.get("http://student.mit.edu/catalog/m6a.html")
        r_b = requests.get("http://student.mit.edu/catalog/m6b.html")
        r_c = requests.get("http://student.mit.edu/catalog/m6c.html")
    
    
        print "processing html and write data to file..."
        self.processMitData(r_a.text, f)
        self.processMitData(r_b.text, f)
        self.processMitData(r_c.text, f)
     
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        #"""
   
start = MitSpider()
start.do_work() 
