#!/usr/bin/env python

from spider import *

class CaltechSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'caltech'
        self.subject = 'eecs'

    def doWork(self):
        print "downloading caltech course info"
        r = requests.get('http://www.cms.caltech.edu/academics/course_desc')
        soup = BeautifulSoup(r.text)


        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        print "processing html and write data to file..."
        for li in soup.find_all('li'):
            data = li.text.strip()
            if data == 'Graduate Programs':
                break
            course_num = ''
            title = ''
            description = 'description:'
            instructors = ''
            prereq = ''
            link = ''
            i = 0
            if li.strong != None and li.strong.a != None:
                link = li.strong.a['href']

            for item in data.split('.'):
                i += 1
                if i == 1:
                    course_num = item.strip().replace(' ', '')
                elif i == 2:
                    title = item.strip()
                elif item.strip().startswith('Instructor'):
                    instructors = item.strip().replace('Instructor: ', 'instructors:').replace('Instructors: ', 'instructors:')
                elif item.strip().startswith('Prerequisites'):
                    prereq = item.strip().replace('Prerequisites: ', 'prereq:')
                else:
                    description += item.strip() + ' '    

            print course_num + ' ' + title + ' ' + link
            if prereq != '':
                description = prereq + ' ' + description
            if instructors != '':
                description = instructors + ' ' + description
            self.count += 1
            self.write_db(f, course_num, title, link, description)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


start = CaltechSpider()
start.doWork()
