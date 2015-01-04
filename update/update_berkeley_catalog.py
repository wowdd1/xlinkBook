#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

class BerkeleyCatalogSpider(Spider):
    

    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.subject = "eecs"
    
    
    def processBerkeleyData(self, f, url, prefix):
        if self.need_update_subject(self.subject) == False:
            return
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        pre_line = ""
        for p in soup.find_all('p'):
            if p.b != None and pre_line != p.b.text[0: p.b.text.find(".")]:
                pre_line = p.b.text[0: p.b.text.find(".")]
                course_num = prefix + p.b.text[0: p.b.text.find(".")]
                course_name = p.b.text[p.b.text.find(".") + 1 : p.b.text.find(".", p.b.text.find(".") + 1)].strip()
                print course_num + " " + course_name
                self.count = self.count + 1
                self.write_db(f, course_num, course_name, "")
    
    def doWork(self):
        #berkeley
        print "downloading berkeley catalog course info"
        file_name = self.get_file_name(self.subject + "/" + "eecs-catalog", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        self.processBerkeleyData(f, "http://general-catalog.berkeley.edu/catalog/gcc_list_crse_req?p_dept_name=Electrical+Engineering&p_dept_cd=EL+ENG&p_path=l", "EE")
        self.processBerkeleyData(f, "http://general-catalog.berkeley.edu/catalog/gcc_list_crse_req?p_dept_name=Computer+Science&p_dept_cd=COMPSCI&p_path=l", "CS")

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = BerkeleyCatalogSpider();
start.doWork() 
