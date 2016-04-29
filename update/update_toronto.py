#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *
sys.path.append("..")
from utils import Utils

class TorontoSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "toronto"
        self.subject = "computer-science"

    def doWork(self):
        utils = Utils()
        r = requests.get('http://www.cdf.toronto.edu/cs_courses/current_course_web_pages.html')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            if li.a != None:
                line = utils.removeDoubleSpace(li.text.replace('\n', ''))
                line = line.replace('CSC ', 'CSC')
                course_id = line[0 : line.find(' ')]
                if course_id.startswith('CSC') == False:
                    continue
                title = line[line.find(' ') : ].strip()
                print course_id + ' ' + title
                self.count += 1
                self.write_db(f, course_id, title, li.a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = TorontoSpider()
start.doWork()
