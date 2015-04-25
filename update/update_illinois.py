#!/usr/bin/env python



from spider import *

class IllinoisSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'illinois'

    def doWork(self):

        file_name = self.get_file_name('eecs', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        r = requests.get('http://ws.engr.illinois.edu/courses/list.asp?mode=timetable&unit=1434&profile=/courses/profile/&groupby=term&term=120151&type=~ind')
        text = r.text
        text = text.replace("document.write('", '').replace("');", '').replace("\\", '')
        soup = BeautifulSoup(text)
        for div in soup.find_all('div', class_='extCourse'):
            sp = BeautifulSoup(div.prettify())
            courseNum = sp.find('div', class_='extCourseRubric').text.replace(' ', '').strip()
            title = sp.find('div', class_='extCourseTitle').text.strip()
            link = 'http://cs.illinois.edu/courses/profile/' + courseNum
            print courseNum + ' ' + title
            self.count += 1
            self.write_db(f, courseNum, title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = IllinoisSpider()
start.doWork()
