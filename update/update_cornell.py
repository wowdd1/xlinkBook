#!/usr/bin/env python

from spider import *

class CornellSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'cornell'
        self.subject = 'eecs'

    def processData(self, url):
        print "downloading cornell course info"
        r = requests.get(url)

        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        url = ''
        for div in soup.find_all('div', class_='cs-course'):
            a = div.h2.a
            if a != None:
                url = a['href']
                course_num = a.text[0 : a.text.find(':')].replace(' ', '').strip()
                title = a.text[a.text.find(':') + 1 :].strip()
                sp = BeautifulSoup(div.prettify())
                course_semesters = sp.find('ul', class_='cs-course-semesters')
                if course_semesters != None:
                    for a in sp.find_all('a'):
                        url = a['href']
            else:
                course_num = div.h2.text[0 : div.h2.text.find(':')].replace(' ', '').strip()
                title = div.h2.text[div.h2.text.find(':') + 1 :].strip()

            print course_num + ' ' + title 
            self.count += 1
            self.write_db(f, course_num, title, url)


        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def doWork(self):
        self.processData('http://www.cs.cornell.edu/courseinfo/listofcscourses')

start = CornellSpider()
start.doWork()

