#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

class BerkeleySpider(Spider):
    

    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.subject = "eecs"
    
    
    def processBerkeleyData(self, f, tr):
        if self.need_update_subject(self.subject) == False:
            return
        i = 0
        title = ""
        link = ""
        for td in tr.children:
           if i == 3:
               title = title + td.a.string + " "
           if i == 5:
               title = title + td.u.string
               link = "http://www-inst.eecs.berkeley.edu" + td.a["href"]
           i = i + 1
        if i > 4:
            self.count = self.count + 1
            self.write_db(f, title[0:title.find(" ")], title[title.find(" "):], link)
    
    def doWork(self):
        #berkeley
        #"""
        print "downloading berkeley course info"
        r = requests.get("http://www-inst.eecs.berkeley.edu/classes-cs.html")
        soup = BeautifulSoup(r.text)
    
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
    
        print "processing html and write data to file..."
        for table in soup.find_all("table", attrs={"class": "column"}):
            tr =  table.tr
            self.processBerkeleyData(f, tr)
    
            for next_tr in tr.next_siblings:
                if next_tr.string == None:
                    self.processBerkeleyData(f, next_tr)
    
    
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
start = BerkeleySpider();
start.doWork() 
