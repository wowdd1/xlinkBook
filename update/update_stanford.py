#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

class StanfordSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
    
    
    def processStanfordDate(self, f, html):
        if self.need_update_subject(self.subject) == False:
            return
        soup = BeautifulSoup(html)
        th_set = soup.find_all("th")
        td_set_all = soup.find_all("td")
        td_set = []
        del th_set[0:5]
    
        i = 0
        for td in td_set_all:
            i = i + 1
            if i == 1:
                td_set.append(td.string)
            if i == 4:
                i = 0
    
        for index in range(0,len(th_set)):
            link = th_set[index].prettify()
            link = link[link.find("http"):link.find("EDU") + 3]
            title = th_set[index].string + " " + td_set[index]
            self.count = self.count + 1
            self.write_db(f, th_set[index].string, td_set[index], link)
    
    def do_work(self):
        #stanford
        #"""
        print "downloading stanford course info"

        file_name = self.get_file_name("eecs/" + "computer-science", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")

        url = "http://cs.stanford.edu/courses/schedules/2014-2015.autumn.php"
        r = requests.get(url)
        #print r.status_code
        print "processing html and write data to file..."
        self.processStanfordDate(f, r.text)
    
        url = "http://cs.stanford.edu/courses/schedules/2014-2015.winter.php"
        r = requests.get(url)
        #print r.status_code
        self.processStanfordDate(f, r.text)
    
        url = "http://cs.stanford.edu/courses/schedules/2014-2015.spring.php"
        r = requests.get(url)
        #print r.status_code
        self.processStanfordDate(f, r.text)
    
        url = "http://cs.stanford.edu/courses/schedules/2013-2014.summer.php"
        r = requests.get(url)
        #print r.status_code
        self.processStanfordDate(f, r.text)
    
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        #"""
    
    
start = StanfordSpider()
start.do_work()    
