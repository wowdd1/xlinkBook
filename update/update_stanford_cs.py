#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

class StanfordSpider(Spider):
    course_num_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
    
    def isInCourseNumList(self, course_num):
        for item in self.course_num_list:
            if item == course_num:
                return True
        self.course_num_list.append(course_num)
        return False
    
    def processStanfordDate(self, f, url):
        print 'processing ' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        th_set = soup.find_all("th")
        td_set_all = soup.find_all("td")
        td_set = []
        td_set_2 = []
        del th_set[0:5]
    
        i = 0
        for td in td_set_all:
            i = i + 1
            if i == 1:
                td_set.append(td.string)
            if i == 2:
                td_set_2.append(td.string)
            if i == 4:
                i = 0
    
        for index in range(0,len(th_set)):
            link = th_set[index].prettify()
            link = link[link.find("http"):link.find("EDU") + 3]
            if self.isInCourseNumList(th_set[index].string) == True:
                continue
            self.count += 1
            self.write_db(f, th_set[index].string.upper(), td_set[index], link, 'instructors:' + td_set_2[index])
    
    def doWork(self):
        #stanford
        #"""
        print "downloading stanford course info"

        file_name = self.get_file_name("eecs/" + "cs.stanford", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
 
        r = requests.get('http://www-cs.stanford.edu/courses')
        soup = BeautifulSoup(r.text)
        print "processing html and write data to file..."
        for a in soup.find_all('a'):
            if a.attrs.has_key('href') and a['href'].find('http://cs.stanford.edu/courses/schedules/') != -1:
                self.processStanfordDate(f, a['href'])
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        #"""
    
    
start = StanfordSpider()
start.doWork() 
