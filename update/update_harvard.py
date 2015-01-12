#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *


class HarvardSpider(Spider):    
    #harvard
    
    def __init__(self):
        Spider.__init__(self)
        self.school = "harvard"
        self.url = "http://www.registrar.fas.harvard.edu"

    def formatCourseNum(self, subject, oldTitle):
        title = oldTitle[0 : oldTitle.find(".")]
        if title.find("(") != -1:
            title = title[0 : title.find("(")].strip()
        title = title.replace("*", "").replace("[", "")
        if title.find(subject) != -1:
            course_num = title[len(subject) : ].strip()
            if subject.find(" ") != -1:
                words = re.compile("[A-Za-z]+").findall(subject) 
                pre = ""
                for word in words:
                    pre += word[0 : 1]
                return pre + "-" + course_num
            else:
                return subject + "-" + course_num
        return title

    def getHarvardCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        sys.setrecursionlimit(3000)
        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0 
    
        print "\n\nprocessing " + subject + " html and write data to file..."
        for node in soup.find_all("strong"):
            text = ""
            link = ""
            if node.string == None:
                if node.a != None and node.a.string != None:
                    text = node.a.string.replace("\n", "")
                    link = node.a["href"]
                else:
                    if node.a != None:
                        link = node.a["href"]
                    text = node.prettify()
                    if text.find("href=") > 0 :
                        text = text[text.find(">", 8) + 1 : text.find("<", text.find(">", 8)) - 1]
                    else:
                        text = text[text.find(">", 2) + 1 : text.find("<", 8) - 1]
                    text = text.replace("\n", "").strip()
            else:
                text = node.string.replace("\n", "")
    
            self.count = self.count + 1
            #print text

            self.write_db(f, self.formatCourseNum(subject, text), text[text.find(".") + 2:].replace("]", ""), link)
        if self.count == 0:
            print subject + " can not get the data, check the html and python code"
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def doWork(self): 
        print "downloading harvard course info"
        r = requests.get("http://www.registrar.fas.harvard.edu/courses-exams/courses-instruction")
        soup = BeautifulSoup(r.text)
    
        for span in soup.find_all("span", class_="field-content"):
            #print span.a.string
            self.getHarvardCourse(span.a.string, self.url + str(span.a["href"]))
    
start = HarvardSpider()
start.doWork()
