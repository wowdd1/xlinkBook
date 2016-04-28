#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *

class UCLSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "ucl"
        self.subject = "computer-science"


    def doWork(self):
        urls = ['http://www.cs.ucl.ac.uk/students/syllabus/ug/', 'http://www.cs.ucl.ac.uk/students/syllabus/pg/']

        file_name = self.get_file_name("eecs/" + self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            for li in soup.find_all('li'):
                if li.a != None and li.a.text.find(' -') != -1:
                    print li.a.text
                    text_list = li.a.text.strip().split('-')
                    self.count += 1
                    course_id = text_list[0]
                    if text_list[0].startswith('ENGS') == False:
                        course_id = 'COMP' + course_id 
                    self.write_db(f, course_id, text_list[1], 'http://www.cs.ucl.ac.uk/' + li.a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = UCLSpider()
start.doWork()
