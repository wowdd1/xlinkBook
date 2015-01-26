#!/usr/bin/env python

from spider import *


class BerkeleyUpcomingSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.subject = 'eecs'
        self.school = 'berkeley'
    def processData(self, f, url, subject):
        print 'processData ' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        title = ''
        course_num = ''
        link = ''
        instructors = ''
        for td in soup.find_all('td', attrs={"align": "center"}):
            if td.text.startswith(subject + ' '):
                course_num = td.text.replace(' ', '')
            if td.prettify().find('/Courses/Data') != -1:
                title = td.text
                link = 'http://www.eecs.berkeley.edu' + td.a['href']
            if td.prettify().find('/Faculty/Homepages') != -1:
                instructors = 'instructors:' + td.text + ' '
                print course_num + ' ' + title + ' ' + link
                self.count += 1
                self.write_db(f, course_num, title, link, instructors)

    def doWork(self):
        file_name = self.get_file_name(self.subject + '/eecs-upcoming', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        self.processData(f, 'http://www.eecs.berkeley.edu/Scheduling/EE/schedule-next.html', 'EE')
        self.processData(f, 'http://www.eecs.berkeley.edu/Scheduling/CS/schedule-next.html', 'CS') 

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = BerkeleyUpcomingSpider()
start.doWork()
